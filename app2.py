from flask import Flask, render_template

app = Flask(__name__)

voters = [
    {"id": 1, "name": "kartik", "vote": "Candidate A"},
    {"id": 2, "name": "shilpa", "vote": "Candidate B"},
    {"id": 3, "name": "pooja", "vote": "Candidate A"},
    {"id": 4, "name": "mahesh", "vote": "Candidate C"},
    {"id": 5, "name": "krishna", "vote": "Candidate B"}
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/records")
def records():
    return render_template("records.html", voters=voters)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)