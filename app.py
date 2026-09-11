from flask import Flask, render_template, request

app = Flask(__name__)


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

        wall = {
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
            score=score,
            verdict=verdict,
            personality=personality,
        )

    return render_template("inspect.html")


if __name__ == "__main__":
    app.run(debug=True)