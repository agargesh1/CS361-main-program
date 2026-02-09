from flask import Flask, render_template, redirect, url_for, request
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flask import abort

app = Flask(__name__)

DATA_PATH = Path("data/workouts.json")
GOAL_PATH = Path("data/goal.json")

def load_goal_minutes(default=150):
    if not GOAL_PATH.exists():
        return default
    try: 
        with GOAL_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return int(data.get("goal_minutes", default))
    except (json.JSONDecodedError, ValueError, TypeError):
        return default

def save_goal_minutes(goal_minutes: int):
    GOAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with GOAL_PATH.open("w", encoding="utf-8") as f:
        json.dump({"goal_minutes": goal_minutes}, f, indent=2)


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

CHART_PATH = Path("static/progress_chart.png")

def generate_progress_chart(workouts):
    """
    Creates a simple bar chart: total min per date
    Saves to static/progress_chart.png
    """
    if len(workouts) == 0:
        if CHART_PATH.exists():
            CHART_PATH.unlink()
        return
    
    minutes_by_date = {}
    for w in workouts:
        d = w["date"]
        minutes_by_date[d] = minutes_by_date.get(d, 0) + int(w["duration"])

    dates = sorted(minutes_by_date.keys())
    minutes = [minutes_by_date[d] for d in dates]

    plt.figure()
    plt.bar(dates, minutes)
    plt.title("Minutes per day")
    plt.xlabel("Date")
    plt.ylabel("Minutes")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    CHART_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(CHART_PATH)
    plt.close()

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
    status = request.args.get("status")
    return render_template("history.html", workouts=workouts, status=status)

@app.get("/history/delete/<int:idx>")
def confirm_delete(idx: int):
    workouts = load_workouts()
    if idx < 0 or idx >= len(workouts):
        abort(404)

    workout = workouts[idx]
    return render_template("confirm_delete.html", idx=idx, workout=workout)

@app.post("/history/delete/<int:idx>")
def delete_workout(idx: int):
    workouts = load_workouts()
    if idx < 0 or idx >= len(workouts):
        abort(404)
    
    workouts.pop(idx)
    save_workouts(workouts)

    return redirect(url_for("history", status="Workout Deleted."))

@app.post("/goal")
def set_goal():
    goal_raw = request.form.get("goal_minutes", "").strip()
    try:
        goal = int(goal_raw)
        if goal <= 0:
            raise ValueError
    except ValueError:
        return redirect(url_for("entry", status="Goal must be a positive whole number."))

    save_goal_minutes(goal)
    return redirect(url_for("progress"))



@app.get("/progress")
def progress():
    workouts = load_workouts()

    GOAL_MINUTES = load_goal_minutes(default=150)

    if len(workouts) == 0:
        return render_template(
            "progress.html",
            stats=None,
            chart_exists=False,
            status="Log at least one workout to see progress."
        )

    total_workouts = len(workouts)
    total_minutes = sum(int(w["duration"]) for w in workouts)
    avg_minutes = round(total_minutes / total_workouts)

    progress_percent = int(min(100, round((total_minutes / GOAL_MINUTES) * 100)))

    generate_progress_chart(workouts)
    chart_exists = CHART_PATH.exists()

    if progress_percent >= 100:
        status = "Goal Reached 🥳✨! Fantastic work 👏👏👏. Set a new goal whenever you're ready."
    elif progress_percent >= 75: 
        status = f" Almoss there, keep goin 🤏📈! You're at {progress_percent}% of your goal."
    elif progress_percent >= 25:
        status = f" Great Progress 💪! {progress_percent}% toward your goal."
    else: 
        status = f"Great Start! {progress_percent}% towards your goal." 

    stats = {
        "total_workouts": total_workouts,
        "total_minutes": total_minutes,
        "avg_minutes": avg_minutes,
        "goal_minutes": GOAL_MINUTES,
        "progress_percent": progress_percent
    }

    return render_template(
        "progress.html",
        stats=stats,
        chart_exists=chart_exists,
        status=status
    )




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
