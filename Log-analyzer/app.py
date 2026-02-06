from flask import Flask, render_template, request
from src.log_analyzer import analyze_log_entries, suggest_solutions



app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["logfile"]
        lines = file.read().decode().splitlines()
        analysis = analyze_log_entries(lines)
        suggestions = suggest_solutions(analysis)
        return render_template("results.html", analysis=analysis, suggestions=suggestions)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)