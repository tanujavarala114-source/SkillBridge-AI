
import sqlite3

def create_database():

    conn = sqlite3.connect("skillbridge.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            career_role TEXT,
            skill_score INTEGER,
            skills_found TEXT,
            missing_skills TEXT
        )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")


def save_analysis(role, score, found, missing):

    conn = sqlite3.connect("skillbridge.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users
        (career_role, skill_score, skills_found, missing_skills)
        VALUES (?, ?, ?, ?)
    """, (
        role,
        score,
        ", ".join(found),
        ", ".join(missing)
    ))

    conn.commit()
    conn.close()

    print("Analysis saved successfully!")


def get_history():

    conn = sqlite3.connect("skillbridge.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    records = cursor.fetchall()

    conn.close()

    return records


if __name__ == "__main__":
    create_database()
