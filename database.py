import sqlite3
from datetime import datetime

def init_db():
    conn=sqlite3.connect("resume_history.db")
    cursor=conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            role TEXT,
            resume_score INTEGER,
            ats_score INTEGER,
            skills_score INTEGER,
            experience_score INTEGER,
            projects_score INTEGER,
            education_score INTEGER,
            achievements_score INTEGER
        )
    """)
    conn.commit()
    conn.close()
    
def save_analysis(role, resume_score, ats_score, section_score):
    conn = sqlite3.connect("resume_history.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO history (timestamp, role, resume_score, ats_score, 
                             skills_score, experience_score, projects_score, 
                             education_score, achievements_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, role, resume_score, ats_score,
          section_score["Skills"], section_score["Experience"],
          section_score["Projects"], section_score["Education"],
          section_score["Achievements"]))
    
    conn.commit()
    conn.close()


def get_all_history():
    conn = sqlite3.connect("resume_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows