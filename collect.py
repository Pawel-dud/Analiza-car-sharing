import sqlite3
import requests
from datetime import datetime, timezone

#Połączenie z bazdą danych
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

#Tworzenie tabel
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

#Pobieranie danych z API
for zone in range(1, 12):
    print(f"Pobieranie danych dla strefy {zone}...")
    url = f"https://fioletowe.live/api/v1/cars?zoneId={zone}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    table_name = f"zone_{zone}"
    observation_time = datetime.now(timezone.utc).isoformat()

#Zapisywanie samochodów
    for car in data["cars"]:
        cursor.execute(f"""
                   INSERT INTO {table_name}
                   (
                    car_id,
                    observation_time,
                    lat,
                    lng,
                    location,
                    model_id,
                    reg_plate,
                    fuel,
                    range_km,
                    available,
                    last_update
                     )
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                     """,
                     (
                        car["id"],
                        observation_time,
                        car["lat"],
                        car["lng"],
                        car["location"],
                        car["modelId"],
                        car["regPlate"],
                        car["fuel"],
                        car["range"],
                        car["available"],
                        car["lastUpdate"]
                     ))
                    
    print(f"Zone {zone} zapisane")
        
#Zapis zmian
conn.commit()
conn.close()

print("Zakończono pobieranie danych.")