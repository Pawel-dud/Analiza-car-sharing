import sqlite3
import requests

#Połączenie z bazdą danych
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

#Tworzqenie tabel
cursor.execute("""
CREATE TABLE IF NOT EXISTS car_models (
               id INTEGER PRIMARY KEY,
               name TEXT,
               type INTEGER,
               max_fuel REAL,
               electric INTEGER
               )
             """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS zone_list (
               id INTEGER PRIMARY KEY,
               name TEXT,
               short_url TEXT,
               lat REAL,
               lng REAL
               )
             """)

#Pobieranie modeli samochodów z API
print("Pobieranie modeli samochodów...")
url = "https://fioletowe.live/api/v1/car-models"

response = requests.get(url)
response.raise_for_status()

models_data = response.json()

for model in models_data["carModels"]:
    cursor.execute("""
                   INSERT OR REPLACE INTO car_models
                   (
                    id,
                    name,
                    type,
                    max_fuel,
                    electric
                   )
                   VALUES (?, ?, ?, ?, ?)
                   """,
                   (
                       model["id"],
                       model["name"],
                       model["type"],
                       model["maxFuel"],
                       model["electric"]
                   ))
print("Modele zapisane")

#Pobieranie stref
print("Pobieranie stref...")
url = "https://fioletowe.live/api/v1/zones"

response = requests.get(url)
response.raise_for_status()

zones_data = response.json()

for zone in zones_data["zones"]:
    cursor.execute("""
                   INSERT OR REPLACE INTO zone_list
                   (
                    id,
                    name,
                    short_url,
                    lat,
                    lng
                   )
                   VALUES (?, ?, ?, ?, ?)
                   """,
                   (
                       zone["id"],
                       zone["name"],
                       zone["shortUrl"],
                       zone["lat"],
                       zone["lng"]
                   ))
print("Strefy zapisane")

#Zapisywanie zmian
conn.commit()
conn.close()

print("Aktualizacja danych zakończona.")