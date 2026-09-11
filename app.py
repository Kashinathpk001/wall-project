import os
import sqlite3
import tempfile
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database configuration (environment variables with local defaults)
DB_HOST = (os.environ.get("DB_HOST") or "").strip() or "localhost"
DB_USER = (os.environ.get("DB_USER") or "").strip() or "root"
DB_PASSWORD = (os.environ.get("DB_PASSWORD") or "").strip() or "root"
DB_NAME = (os.environ.get("DB_NAME") or "").strip() or "wall_trust"

raw_port = (os.environ.get("DB_PORT") or "").strip()
try:
    DB_PORT = int(raw_port) if raw_port else 3306
except (ValueError, TypeError):
    DB_PORT = 3306


def get_db_connection():
    """Connect to MySQL if available, or fall back to SQLite for reviewers/serverless."""
    is_vercel = bool(os.environ.get("VERCEL"))

    # Skip MySQL if on Vercel and host is default localhost to prevent startup timeouts
    if not (is_vercel and DB_HOST in ("localhost", "127.0.0.1", "")):
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                port=DB_PORT,
                connection_timeout=3,
            )
            return conn, "mysql"
        except Exception:
            pass

    # Fallback to local SQLite if MySQL is unreachable (e.g. for GitHub reviewers or Vercel)
    db_path = os.path.join(tempfile.gettempdir(), "wall_trust.db") if is_vercel else "wall_trust.db"
    conn = sqlite3.connect(db_path)
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

    # Seed initial demo walls if the SQLite database is fresh/empty
    try:
        cursor.execute("SELECT COUNT(*) FROM walls")
        count = cursor.fetchone()[0]
        if count == 0:
            demo_walls = [
                (
                    "The Great North Wall (Ancient Brick)",
                    35.0,
                    3.2,
                    230.0,
                    2,
                    0,
                    1,
                    65,
                    "SUSPICIOUS",
                    "The Resilient Veteran - Has seen empires fall and questionable posters hung.",
                ),
                (
                    "Library Quiet Wall (Reinforced Concrete)",
                    5.0,
                    2.8,
                    300.0,
                    0,
                    0,
                    0,
                    100,
                    "TRUSTWORTHY",
                    "The Stoic Monolith - Radiates pure architectural serenity.",
                ),
                (
                    "Basement Boiler Wall (Damp Plaster)",
                    18.0,
                    2.4,
                    120.0,
                    7,
                    1,
                    4,
                    10,
                    "BETRAYAL IMMINENT",
                    "The Structural Crybaby - One firm sneeze away from spontaneous failure.",
                ),
                (
                    "Cafeteria Snack Corner Wall",
                    8.0,
                    3.0,
                    200.0,
                    1,
                    0,
                    0,
                    85,
                    "TRUSTWORTHY",
                    "The Gravy Sponge - Absorbs gossip and lukewarm samosa steam with pride.",
                ),
            ]
            cursor.executemany(
                """
                INSERT INTO walls (location, age, height, thickness, cracks, dampness, repairs, score, verdict, personality)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                demo_walls,
            )
            conn.commit()
    except Exception:
        pass

    return conn, "sqlite"


def init_db():
    """Ensure database and table exist in MySQL if configured, or SQLite."""
    is_vercel = bool(os.environ.get("VERCEL"))
    if is_vercel and DB_HOST in ("localhost", "127.0.0.1", ""):
        try:
            conn, _ = get_db_connection()
            conn.close()
        except Exception:
            pass
        return

    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            connection_timeout=3,
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
        try:
            conn, _ = get_db_connection()
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


def get_verdict_info(score):
    if score >= 80:
        return "TRUSTWORTHY", "verdict-trustworthy", "#A6DA95"
    elif score >= 60:
        return "MOSTLY TRUSTWORTHY", "verdict-mostly", "#8BD5CA"
    elif score >= 40:
        return "SUSPICIOUS", "verdict-suspicious", "#EED49F"
    else:
        return "DO NOT TRUST", "verdict-danger", "#ED8796"


def get_personality_details(score, cracks, dampness, repairs, location=""):
    loc_lower = location.lower()
    
    # Campus specific easter egg personality overlays
    if "canteen" in loc_lower or "pazhampori" in loc_lower or "pazham" in loc_lower or "pori" in loc_lower or "sulaimani" in loc_lower or "chaya" in loc_lower or "thattukada" in loc_lower or "cafeteria" in loc_lower:
        return (
            "The Pazhampori Sentry",
            "Infused with 12 years of sizzling coconut oil fumes, strong tea steam, and crisp Pazhampori splatters. Vibrates rhythmically during the 4 PM Sulaimani rush.",
            "☕ Chayakada Advisory: Never lean with a white shirt or mundu; coconut oil betrayal is guaranteed."
        )
    elif "admin" in loc_lower or "fee" in loc_lower or "counter" in loc_lower:
        return (
            "The Bureaucratic Stonewall",
            "Impenetrable, emotionless, and requires Form 4-B in triplicate just to hang a calendar. 0% structural empathy.",
            "🏛️ Admin Clearance: So unyielding that Wi-Fi signals bounce right off it."
        )
    elif "cricket" in loc_lower or "hostel" in loc_lower or "dorm" in loc_lower:
        return (
            "The Comeback Story",
            "Constructed from 40% drywall and 60% emergency spackle. Has stopped 34 leather cricket balls and an errant chair.",
            "🏏 Sports Advisory: Do not bowl spin deliveries into the third-floor joint."
        )
    elif "library" in loc_lower or "study" in loc_lower:
        return (
            "The Silent Confessor",
            "Has quietly absorbed over 85,000 student existential groans the night before calculus midterms. Deeply traumatized.",
            "📚 Library Protocol: Speak in hushed tones; this wall has emotional PTSD."
        )
    elif "washroom" in loc_lower or "bathroom" in loc_lower or "stall" in loc_lower:
        return (
            "The Walking Disaster",
            "A razor-thin 45mm partition bearing the philosophical musings and emergency heartbreak poetry of 40 batches.",
            "🚽 Stall Warning: One heavy kick and this partition enters the next postal code."
        )
    elif "chem" in loc_lower or "lab" in loc_lower:
        return (
            "The Blast Shield",
            "Chemical staining suggests it survived an unauthorized potassium experiment in 2022. Smells faintly of sulfur.",
            "🧪 Lab Hazard: Touch only with heat-resistant tongs and protective goggles."
        )

    # Standard personalities
    if cracks >= 4 and dampness:
        return (
            "The Walking Disaster",
            "Active weeping moisture, rampant fissures, and zero structural morale. This wall is actively plotting its descent.",
            "⚠️ Immediate Hazard: Do not mount shelves or lean against this structure."
        )
    elif repairs >= 3:
        return (
            "The Comeback Story",
            "More spackle and compound than original drywall. Survived toddler artwork, DIY plumbing, and aggressive door slams.",
            "🛠️ Veteran Status: Held together by sheer determination and prayer."
        )
    elif score >= 80:
        return (
            "The Reliable One",
            "A stoic architectural monolith. Has stood through generations without flinching. Safe for heavy antique mirrors.",
            "🛡️ Security Clearance: Certified load-bearing rockstar."
        )
    elif score >= 50:
        return (
            "It's Complicated",
            "Technically standing, but mentally checked out. Avoid loud arguments or intense bass vibrations nearby.",
            "🤔 Behavioral Advice: Polite nods only; do not test its emotional patience."
        )
    else:
        return (
            "The Red Flag",
            "One energetic high-five away from structural collapse. Trembles in high humidity. Do not breathe near it.",
            "🚨 Urgent Advisory: Treat with intense suspicion and keep safety goggles nearby."
        )


def get_red_flags(age, cracks, dampness, repairs, thickness, location=""):
    flags = []
    loc_lower = location.lower()

    # Campus humorous specific flags
    if "canteen" in loc_lower or "pazhampori" in loc_lower or "pazham" in loc_lower or "pori" in loc_lower or "sulaimani" in loc_lower or "chaya" in loc_lower or "thattukada" in loc_lower or "cafeteria" in loc_lower:
        flags.append("Coconut Oil & Sulaimani Saturation: 96% Coconut oil vapor and boiling Chaya steam absorbed into porous lime plaster.")
    if "lecture" in loc_lower or "hall" in loc_lower:
        flags.append("Student Ergonomic Indentation: Lower 1.2 meters polished glass-smooth by generations of sleeping students.")
    if "hostel" in loc_lower or "dorm" in loc_lower or "cricket" in loc_lower:
        flags.append("Midnight Cricket Ballistics: Suspicious circular impact craters concealed beneath anime and band posters.")
    if "library" in loc_lower or "study" in loc_lower:
        flags.append("Exam Tear Salinity: Moisture sensors indicate dampness is 98% distilled GPA-related panic.")
    if "washroom" in loc_lower or "bathroom" in loc_lower or "stall" in loc_lower:
        flags.append("Literary Graffiti Load: Inscribed with unverified calculus shortcuts, phone numbers, and heartbreak lyrics.")
    if "chem" in loc_lower or "lab" in loc_lower:
        flags.append("Acid Vapor Etching: Withstood 4 failed titrations and an unplanned magnesium combustion incident.")
    if "admin" in loc_lower or "fee" in loc_lower:
        flags.append("Bureaucratic Densification: So dense that not even Wi-Fi, cell reception, or student appeals can penetrate.")
    if "gate" in loc_lower or "boundary" in loc_lower:
        flags.append("Curfew Bypass Footholds: Shoe scuff marks at the 1.9m mark confirm routine midnight escape maneuvers.")

    # Core algorithmic flags
    if cracks >= 6:
        flags.append(f"Severe Fracturing: {cracks} structural fissures detected. Wall is having an existential crisis.")
    elif cracks >= 3:
        flags.append(f"Noticeable Cracks: {cracks} cracks found. Emotional containment is failing.")
    elif cracks >= 1:
        flags.append(f"Minor Cracking: {cracks} hairline fissure(s) spotted. Keep a close watch.")

    if dampness and not ("library" in loc_lower or "canteen" in loc_lower):
        flags.append("Active Moisture: Wall is sweating/damp. It may be silently weeping on the inside.")

    if thickness < 150:
        flags.append(f"Dangerously Thin: Only {thickness}mm thick. One aggressive shoulder bump could cause a breach.")

    if age >= 20:
        flags.append(f"Senior Citizen Architecture: {age} years on duty. Suffers from chronic fatigue.")

    if repairs >= 3 and not ("hostel" in loc_lower):
        flags.append(f"Frequent Surgery: {repairs} prior patch jobs. More duct tape and compound than brick.")

    return flags


def get_useless_telemetry(score, thickness, cracks, dampness, age, shirt_color="black", posture="slouch"):
    """Calculates completely useless metrics for the TinkerHub Useless Projects Hackathon."""
    # 1. White chalk powder expected on shirt (in cm²)
    base_chalk = 45 if age > 15 else 18
    if cracks > 0:
        base_chalk += cracks * 6
    if dampness:
        base_chalk = int(base_chalk * 0.35) # wet walls smear paste instead of powder
    chalk_sqcm = min(220, max(0, int(base_chalk)))

    # 2. Shirt Ruin Probability
    shirt_mult = {
        "black": 0.95,
        "navy": 0.90,
        "gray": 0.50,
        "white": 0.12,
        "silk": 0.99,
        "uniform": 0.88,
    }.get(shirt_color.lower(), 0.80)
    shirt_ruin_pct = min(100, int((chalk_sqcm / 110) * 100 * shirt_mult + (20 if dampness else 0)))

    # 3. Maximum Safe Lean Duration
    if score >= 85:
        max_duration = "14 minutes, 30 seconds (or until your leg falls asleep)"
    elif score >= 65:
        max_duration = "5 minutes, 15 seconds (shift posture every 45 seconds)"
    elif score >= 40:
        max_duration = "1 minute, 12 seconds (keep both feet firmly planted on ground)"
    else:
        max_duration = "0.3 seconds (do not make physical contact)"

    # 4. Total Gossip Overheard by This Wall
    gossip_count = int(age * 210 + cracks * 145 + 1420)

    # 5. Useless Alternatives
    if score < 50:
        alternatives = [
            "Lean against a reliable friend who won't flake chalk on your back.",
            "Sit on the floor cross-legged and pretend you're doing meditation.",
            "Bring a folding camp chair to campus next time.",
            "Stand with rigid military posture and question your life decisions."
        ]
    else:
        alternatives = [
            "Safe to lean. Proceed to scroll Instagram reels for 45 minutes.",
            "Enjoy the gentle embrace of campus concrete.",
            "Optimal posture. You may now sip your Sulaimani tea in absolute peace."
        ]

    posture_names = {
        "slouch": "The 4 PM Tea Slouch (45° backward lean)",
        "reels": "The Reel Scroller (One shoulder against wall)",
        "nap": "The 1st Period Nap (Forehead pressed directly against brick)",
        "hero": "The Corridor Hero (One foot on wall, waiting for dramatic wind)",
        "elbow": "The Casual Elbow Rest (Minimal commitment)"
    }

    import random
    alt = alternatives[abs(hash(str(score) + str(age))) % len(alternatives)]

    return {
        "chalk_sqcm": chalk_sqcm,
        "shirt_ruin_pct": shirt_ruin_pct,
        "shirt_color_label": shirt_color.capitalize(),
        "posture_label": posture_names.get(posture, posture),
        "max_duration": max_duration,
        "gossip_count": f"{gossip_count:,}",
        "recommendation": alt,
    }


@app.route("/")
def home():
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    recent_walls = []
    try:
        cursor.execute("SELECT id, location, age, height, thickness, cracks, dampness, repairs, score, verdict, personality FROM walls ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        for row in rows:
            recent_walls.append({
                "id": row[0],
                "location": row[1],
                "age": row[2],
                "height": row[3],
                "thickness": row[4],
                "cracks": row[5],
                "dampness": row[6],
                "repairs": row[7],
                "score": row[8],
                "verdict": row[9],
                "personality": row[10],
            })
    except Exception:
        pass
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass
    return render_template("index.html", recent_walls=recent_walls)


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
        verdict, verdict_class, bar_color = get_verdict_info(score)
        personality, personality_desc, personality_advisory = get_personality_details(score, cracks, dampness, repairs, location)
        red_flags = get_red_flags(age, cracks, dampness, repairs, thickness, location)

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

        shirt_color = request.form.get("shirt_color", "black")
        posture = request.form.get("posture", "slouch")
        useless_data = get_useless_telemetry(score, thickness, cracks, dampness, age, shirt_color, posture)

        return render_template(
            "result.html",
            wall=wall,
            wall_id=wall_id,
            score=score,
            verdict=verdict,
            verdict_class=verdict_class,
            bar_color=bar_color,
            personality=personality,
            personality_desc=personality_desc,
            personality_advisory=personality_advisory,
            red_flags=red_flags,
            useless_data=useless_data,
        )

    return render_template("inspect.html")


@app.route("/result/<int:wall_id>")
def result(wall_id):
    conn, db_type = get_db_connection()
    wall = None
    if db_type == "mysql":
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM walls WHERE id = %s", (wall_id,))
        wall = cursor.fetchone()
        cursor.close()
    else:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM walls WHERE id = ?", (wall_id,))
        row = cursor.fetchone()
        if row:
            wall = dict(row)
        cursor.close()
    conn.close()

    if not wall:
        return "Wall dossier not found", 404

    score = wall.get("score", 50)
    verdict, verdict_class, bar_color = get_verdict_info(score)
    personality, personality_desc, personality_advisory = get_personality_details(
        score,
        wall.get("cracks", 0),
        wall.get("dampness", 0),
        wall.get("repairs", 0),
        wall.get("location", ""),
    )
    red_flags = get_red_flags(
        wall.get("cracks", 0),
        wall.get("dampness", 0),
        wall.get("thickness", 200),
        wall.get("age", 10),
        wall.get("repairs", 0),
        wall.get("location", ""),
    )

    useless_data = get_useless_telemetry(
        score,
        wall.get("thickness", 200),
        wall.get("cracks", 0),
        wall.get("dampness", 0),
        wall.get("age", 10),
    )

    return render_template(
        "result.html",
        wall=wall,
        wall_id=wall_id,
        score=score,
        verdict=verdict,
        verdict_class=verdict_class,
        bar_color=bar_color,
        personality=personality,
        personality_desc=personality_desc,
        personality_advisory=personality_advisory,
        red_flags=red_flags,
        useless_data=useless_data,
    )


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