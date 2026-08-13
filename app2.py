import os

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__, template_folder='templates')
app.secret_key = 'online_voting_secret_key'  # Required for flashing messages

print('Current folder:', os.getcwd())

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

@app.route("/add_vote", methods=["GET", "POST"])
def add_vote():

    if request.method == "POST":

        voter_name = request.form.get("voter_name")
        voter_id = request.form.get("voter_id")
        candidate = request.form.get("candidate")
        city = request.form.get("city")

        if not voter_name or not voter_id or not candidate or not city:
         flash("Please fill all fields!", "danger")
         return redirect(url_for("add_vote"))

        # Add new voter to list
        new_voter = {
            "id": len(voters) + 1,
            "name": voter_name,
            "vote": candidate
        }

        voters.append(new_voter)

        # Success message
        flash("Vote added successfully!", "success")

        # Redirect after submit
        return redirect(url_for("records"))

    return render_template("add_vote.html")

@app.route("/records")
def records():
    return render_template("records.html", voters=voters)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)