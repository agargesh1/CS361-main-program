from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.get("/")
def index():
    return redirect(url_for("entry"))

@app.get("/entry")
def entry():
    return render_template("entry.html", status=None)

@app.get("/history")
def history():
    return render_template("history.html", workouts=[])

@app.get("/progress")
def progress():
    return render_template("progress.html", stats=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
