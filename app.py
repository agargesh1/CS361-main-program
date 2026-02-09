from flask import Flask, render_template, redirect, url_for, request
import json
from pathlib import Path

app = Flask(__name__)

DATA_PATH = Path("data/workouts.json")


def load_workouts():
    """Return list of workouts from JSON file. If file missing/empty, return []"""
    if not DATA_PATH.exists():
        return []
    try:
        with DATA_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_workouts(workouts):
    """Write workouts list back to JSON file."""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(workouts, f, indent=2)


@app.get("/")
def index():
    return redirect(url_for("entry"))


@app.route("/entry", methods=["GET", "POST"])
def entry():
    if request.method == "POST":
        workout_type = request.form.get("workout_type", "").strip()
        duration_raw = request.form.get("duration", "").strip()
        date = request.form.get("date", "").strip()
        notes = request.form.get("notes", "").strip()

        # Minimal validation (simple + demo-friendly)
        if not workout_type or not duration_raw or not date:
            return render_template(
                "entry.html",
                status="Please fill in Workout type, Duration, and Date before saving."
            )

        try:
            duration = int(duration_raw)
            if duration <= 0:
                raise ValueError
        except ValueError:
            return render_template(
                "entry.html",
                status="Duration must be a positive whole number of minutes."
            )

        workouts = load_workouts()
        workouts.append({
            "workout_type": workout_type,
            "duration": duration,
            "date": date,
            "notes": notes
        })
        save_workouts(workouts)

        return render_template("entry.html", status="Successfully saved!")

    return render_template("entry.html", status=None)


@app.get("/history")
def history():
    workouts = load_workouts()
    return render_template("history.html", workouts=workouts)


@app.get("/progress")
def progress():
    workouts = load_workouts()
    if len(workouts) == 0:
        return render_template("progress.html", stats=None)

    total_workouts = len(workouts)
    total_minutes = sum(w["duration"] for w in workouts)
    avg_minutes = round(total_minutes / total_workouts)

    stats = {
        "total_workouts": total_workouts,
        "total_minutes": total_minutes,
        "avg_minutes": avg_minutes
    }
    return render_template("progress.html", stats=stats)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
    