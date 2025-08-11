import sqlite3
from tabulate import tabulate  # pip install tabulate

DB_NAME = "detections.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_count INTEGER,
            time TEXT,
            lat REAL,
            lon REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_detection(person_count, time_str, lat, lon):
    """Insert a new detection record into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO detections (person_count, time, lat, lon)
        VALUES (?, ?, ?, ?)
    """, (person_count, time_str, lat, lon))
    conn.commit()
    conn.close()

def read_detections():
    """Read all detection records from the database and display in a table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM detections")
    rows = cursor.fetchall()
    conn.close()

    headers = ["ID", "Person Count", "Time", "Latitude", "Longitude"]
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

# If running directly
if __name__ == "__main__":
    init_db()
    read_detections()
