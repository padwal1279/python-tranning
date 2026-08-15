import sqlite3

DATABASE = "myproject.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS voters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_name TEXT NOT NULL,
            voter_id TEXT NOT NULL,
            candidate TEXT NOT NULL,
            city TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_voter(voter_name, voter_id, candidate, city):
    conn = get_db()

    conn.execute("""
        INSERT INTO voters
        (voter_name, voter_id, candidate, city)
        VALUES (?, ?, ?, ?)
    """, (voter_name, voter_id, candidate, city))

    conn.commit()
    conn.close()


def get_all_voters():
    conn = get_db()

    voters = conn.execute(
        "SELECT * FROM voters ORDER BY id DESC"
    ).fetchall()

    conn.close()
    return voters