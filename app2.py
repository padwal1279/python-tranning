import os
import sqlite3
from database import get_db, init_db, add_voter, get_all_voters

from flask import Flask, render_template, request, redirect, url_for, flash,session

app = Flask(__name__, template_folder='templates')
app.secret_key = 'online_voting_secret_key'
def login_required():
    if "username" not in session:
        flash("Please login first!", "danger")
        return False
    return True


@app.after_request
def add_no_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
init_db()


@app.route("/")
def home():
    if not login_required():
                return redirect(url_for("login"))
    conn = get_db()

    total_voters = conn.execute(
        "SELECT COUNT(*) FROM voters"
    ).fetchone()[0]

    total_candidates = conn.execute(
        "SELECT COUNT(DISTINCT candidate) FROM voters"
    ).fetchone()[0]

    total_cities = conn.execute(
        "SELECT COUNT(DISTINCT city) FROM voters"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "home.html",
        total_voters=total_voters,
        total_candidates=total_candidates,
        total_cities=total_cities
    )


@app.route("/add_vote", methods=["GET", "POST"])
def add_vote():
    if not login_required():
        return redirect(url_for("login"))

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
    if not login_required():
        return redirect(url_for("login"))

    search = request.args.get("search", "").strip()

    conn = get_db()

    if search:
        voters = conn.execute("""
            SELECT * FROM voters
            WHERE voter_name LIKE ?
               OR voter_id LIKE ?
            ORDER BY id DESC
        """, (f"%{search}%", f"%{search}%")).fetchall()
    else:
        voters = conn.execute(
            "SELECT * FROM voters ORDER BY id DESC"
        ).fetchall()

    conn.close()

    return render_template(
        "records.html",
        voters=voters,
        search=search
    )
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please fill all fields!", "danger")
            return redirect(url_for("register"))

        conn = get_db()

        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()

            flash("Registration successful!", "success")
            return redirect(url_for("register"))

        except sqlite3.IntegrityError:
            flash("Username already exists!", "danger")
            return redirect(url_for("register"))

        finally:
            conn.close()

    return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("home"))

        flash("Invalid username or password!", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")
@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/delete/<int:voter_id>")
def delete_vote(voter_id):
    if not login_required():
        return redirect(url_for("login"))
    conn = get_db()
    conn.execute("DELETE FROM voters WHERE id = ?", (voter_id,))
    conn.commit()
    conn.close()

    flash("Vote deleted successfully!", "success")
    return redirect(url_for("records"))


@app.route("/edit/<int:voter_id>", methods=["GET", "POST"])
def edit_vote(voter_id):
    if not login_required():
            return redirect(url_for("login"))
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