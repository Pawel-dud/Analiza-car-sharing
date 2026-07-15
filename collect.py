import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

for zone in range(1, 12):
    table_name = f"zone_{zone}"

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        observation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        observation_time TEXT,
        car_id INTEGER,
        lat REAL,
        lng REAL,
        location TEXT,
        model_id INTEGER,
        reg_plate TEXT,
        fuel REAL,
        range_km INTEGER,
        available INTEGER,
        last_update TEXT
    )
    """)

conn.commit()
conn.close()

print("Baza została utworzona.")