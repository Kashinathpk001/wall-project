import os
import sqlite3
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database configuration (environment variables with local defaults)
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
DB_NAME = os.environ.get("DB_NAME", "wall_trust")
DB_PORT = int(os.environ.get("DB_PORT", 3306))


def get_db_connection():
    """Connect to MySQL if available, or fall back to SQLite for reviewers."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
        )
        return conn, "mysql"
    except Exception:
        # Fallback to local SQLite if MySQL is unreachable (e.g. for GitHub reviewers)
        conn = sqlite3.connect("wall_trust.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS walls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                age REAL NOT NULL,
                height REAL NOT NULL,
                thickness REAL NOT NULL,
                cracks INTEGER NOT NULL,
                dampness INTEGER NOT NULL,
                repairs INTEGER NOT NULL,
                score INTEGER NOT NULL,
                verdict TEXT NOT NULL,
                personality TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()
        return conn, "sqlite"


def init_db():
    """Ensure database and table exist in MySQL."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        cursor.execute(f"USE {DB_NAME};")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS walls (
                id INT AUTO_INCREMENT PRIMARY KEY,
                location VARCHAR(255) NOT NULL,
                age FLOAT NOT NULL,
                height FLOAT NOT NULL,
                thickness FLOAT NOT NULL,
                cracks INT NOT NULL,
                dampness INT NOT NULL,
                repairs INT NOT NULL,
                score INT NOT NULL,
                verdict VARCHAR(50) NOT NULL,
                personality VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        pass


# Initialize database on startup
init_db()


def calculate_score(age, cracks, dampness, repairs, thickness):
    score = 100

    # Age deduction: 10 years: -10, 20 years: -20
    if age >= 20:
        score -= 20
    elif age >= 10:
        score -= 10

    # Cracks deduction: 1-2: -10, 3-5: -20, 6+: -35
    if cracks >= 6:
        score -= 35
    elif cracks >= 3:
        score -= 20
    elif cracks >= 1:
        score -= 10

    # Dampness deduction: Yes: -15
    if dampness:
        score -= 15

    # Previous repairs: -5 for each repair
    score -= repairs * 5

    # Thickness deduction: <150 mm: -10
    if thickness < 150:
        score -= 10

    # Clamp score between 0 and 100
    return max(0, min(100, int(score)))


def get_verdict(score):
    if score >= 80:
        return "TRUSTWORTHY"
    elif score >= 60:
        return "MOSTLY TRUSTWORTHY"
    elif score >= 40:
        return "SUSPICIOUS"
    else:
        return "DO NOT TRUST"


def get_personality(score, cracks, dampness, repairs):
    if cracks >= 4 and dampness:
        return "The Walking Disaster"
    elif repairs >= 3:
        return "The Comeback Story"
    elif score >= 80:
        return "The Reliable One"
    elif score >= 50:
        return "It's Complicated"
    else:
        return "The Red Flag"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/inspect", methods=["GET", "POST"])
def inspect():
    if request.method == "POST":
        location = request.form.get("location", "Unknown Wall")
        try:
            age = float(request.form.get("age", 0) or 0)
        except ValueError:
            age = 0.0

        try:
            height = float(request.form.get("height", 0) or 0)
        except ValueError:
            height = 0.0

        try:
            thickness = float(request.form.get("thickness", 0) or 0)
        except ValueError:
            thickness = 0.0

        try:
            cracks = int(request.form.get("cracks", 0) or 0)
        except ValueError:
            cracks = 0

        try:
            dampness = int(request.form.get("dampness", 0) or 0)
        except ValueError:
            dampness = 0

        try:
            repairs = int(request.form.get("repairs", 0) or 0)
        except ValueError:
            repairs = 0

        score = calculate_score(age, cracks, dampness, repairs, thickness)
        verdict = get_verdict(score)
        personality = get_personality(score, cracks, dampness, repairs)

        # Store wall inspection into database
        conn, db_type = get_db_connection()
        cursor = conn.cursor()

        if db_type == "mysql":
            query = """
                INSERT INTO walls (location, age, height, thickness, cracks, dampness, repairs, score, verdict, personality)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                location,
                age,
                height,
                thickness,
                cracks,
                dampness,
                repairs,
                score,
                verdict,
                personality,
            )
            cursor.execute(query, values)
            conn.commit()
            wall_id = cursor.lastrowid
        else:
            query = """
                INSERT INTO walls (location, age, height, thickness, cracks, dampness, repairs, score, verdict, personality)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            values = (
                location,
                age,
                height,
                thickness,
                cracks,
                dampness,
                repairs,
                score,
                verdict,
                personality,
            )
            cursor.execute(query, values)
            conn.commit()
            wall_id = cursor.lastrowid

        cursor.close()
        conn.close()

        wall = {
            "id": wall_id,
            "location": location,
            "age": age,
            "height": height,
            "thickness": thickness,
            "cracks": cracks,
            "dampness": dampness,
            "repairs": repairs,
        }

        return render_template(
            "result.html",
            wall=wall,
            wall_id=wall_id,
            score=score,
            verdict=verdict,
            personality=personality,
        )

    return render_template("inspect.html")


@app.route("/database")
def database():
    conn, db_type = get_db_connection()
    if db_type == "mysql":
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM walls ORDER BY id DESC")
        walls = cursor.fetchall()
        cursor.close()
    else:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM walls ORDER BY id DESC")
        walls = [dict(row) for row in cursor.fetchall()]
        cursor.close()
    conn.close()
    return render_template("database.html", walls=walls)


@app.route("/leaderboard")
def leaderboard():
    conn, db_type = get_db_connection()
    if db_type == "mysql":
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM walls ORDER BY score DESC, id ASC LIMIT 10")
        top_walls = cursor.fetchall()
        cursor.execute("SELECT * FROM walls ORDER BY score ASC, id ASC LIMIT 5")
        shame_walls = cursor.fetchall()
        cursor.close()
    else:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM walls ORDER BY score DESC, id ASC LIMIT 10")
        top_walls = [dict(row) for row in cursor.fetchall()]
        cursor.execute("SELECT * FROM walls ORDER BY score ASC, id ASC LIMIT 5")
        shame_walls = [dict(row) for row in cursor.fetchall()]
        cursor.close()
    conn.close()
    return render_template("leaderboard.html", top_walls=top_walls, shame_walls=shame_walls)


if __name__ == "__main__":
    app.run(debug=True)