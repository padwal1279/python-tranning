from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "voting123"


# Database Connection
def get_db():
    conn = sqlite3.connect('myproject.db')
    conn.row_factory = sqlite3.Row
    return conn


# Create Table
def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS voters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_name TEXT NOT NULL,
            voter_id TEXT NOT NULL,
            candidate TEXT NOT NULL,
            city TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Home Page
@app.route('/')
def home():
    return render_template('home.html')


# Add Vote
@app.route('/add_vote', methods=['GET', 'POST'])
def add_vote():
    if request.method == 'POST':
        voter_name = request.form['voter_name']
        voter_id = request.form['voter_id']
        candidate = request.form['candidate']
        city = request.form['city']

        # Validation
        if not voter_name or not voter_id or not candidate or not city:
            flash("All fields are required!")
            return redirect('/add_vote')

        conn = get_db()
        conn.execute(
            '''
            INSERT INTO voters
            (voter_name, voter_id, candidate, city)
            VALUES (?, ?, ?, ?)
            ''',
            (voter_name, voter_id, candidate, city)
        )
        conn.commit()
        conn.close()

        flash("Vote submitted successfully!")
        return redirect('/')

    return render_template('add_vote.html')


# View Records
@app.route('/records')
def records():
    conn = get_db()
    voters = conn.execute('SELECT * FROM voters').fetchall()
    conn.close()
    return render_template('records.html', voters=voters)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)