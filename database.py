import sqlite3

conn = sqlite3.connect("health.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symptom TEXT,
    date_time TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")