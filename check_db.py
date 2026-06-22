import sqlite3

conn = sqlite3.connect("health.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(history)")
print(cursor.fetchall())

conn.close()