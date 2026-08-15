import os
from database import get_db, init_db, add_voter, get_all_voters

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__, template_folder='templates')
app.secret_key = 'online_voting_secret_key'

print('Current folder:', os.getcwd())

init_db()


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

        add_voter(voter_name, voter_id, candidate, city)

        flash("Vote added successfully!", "success")

        return redirect(url_for("records"))

    return render_template("add_vote.html")


@app.route("/records")
def records():
    voters = get_all_voters()
    return render_template("records.html", voters=voters)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/delete/<int:voter_id>")
def delete_vote(voter_id):
    conn = get_db()
    conn.execute("DELETE FROM voters WHERE id = ?", (voter_id,))
    conn.commit()
    conn.close()

    flash("Vote deleted successfully!", "success")
    return redirect(url_for("records"))


@app.route("/edit/<int:voter_id>", methods=["GET", "POST"])
def edit_vote(voter_id):
    conn = get_db()

    if request.method == "POST":
        voter_name = request.form.get("voter_name")
        voter_id_value = request.form.get("voter_id")
        candidate = request.form.get("candidate")
        city = request.form.get("city")

        if not voter_name or not voter_id_value or not candidate or not city:
            flash("Please fill all fields!", "danger")
            conn.close()
            return redirect(url_for("edit_vote", voter_id=voter_id))

        conn.execute("""
            UPDATE voters
            SET voter_name = ?, voter_id = ?, candidate = ?, city = ?
            WHERE id = ?
        """, (voter_name, voter_id_value, candidate, city, voter_id))

        conn.commit()
        conn.close()

        flash("Vote updated successfully!", "success")
        return redirect(url_for("records"))

    voter = conn.execute(
        "SELECT * FROM voters WHERE id = ?", (voter_id,)
    ).fetchone()

    conn.close()

    return render_template("edit_vote.html", voter=voter)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)