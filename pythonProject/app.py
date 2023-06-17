import requests as req
import psycopg2
import time
import os
import datetime
from flask_cors import CORS
from dotenv import load_dotenv
from threading import Thread, Lock
from flask import Flask, jsonify


app = Flask(__name__)
load_dotenv()
data_lock = Lock()
CORS(app)
# Połączenie z bazą danych PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("DBHOST"),
    port=os.getenv("DBPORT"),
    database=os.getenv("DBDATABASE"),
    user=os.getenv("DBUSER"),
    password=os.getenv("DATABASE_PASSWORD")
)
cur = conn.cursor()


# Tworzenie tabeli w bazie danych
cur.execute(
    "CREATE TABLE IF NOT EXISTS exchange.kurs (id_waluty SERIAL PRIMARY KEY, currency CHARACTER(50), code CHARACTER(5), mid CHARACTER(10), zapis DATE);")

# Funkcja do pobierania danych z API NBP i zapisywania ich do bazy danych
def get_data():
    # Pobranie danych z API NBP

    # Obliczenie daty dzisiejszej
    today = datetime.date.today()

    # Obliczenie daty sprzed 7 dni
    start_date = today - datetime.timedelta(days=7)

    # Budowanie URL-a z dynamicznymi datami
    url = f"https://api.nbp.pl/api/exchangerates/tables/A/{start_date}/{today}/"

    response = req.get(url)
    data = response.json()

    for entry in data:
        date_from_api = entry['effectiveDate']
        rates = entry['rates']

        # Sprawdzenie, czy dane już istnieją w bazie
        cur.execute("SELECT COUNT(*) FROM exchange.kurs WHERE zapis = %s", (date_from_api,))
        result = cur.fetchone()

        # Zapis danych do bazy danych PostgreSQL
        if result[0] == 0:
            with data_lock:
                for item in rates:
                    cur.execute("INSERT INTO exchange.kurs (currency, code, mid, zapis) VALUES (%s, %s, %s, %s)",
                                (item['currency'], item['code'], item['mid'], date_from_api))
            conn.commit()

# Funkcja do sprawdzania, czy aktualny czas odpowiada określonej godzinie
def check_schedule():
    current_time = time.strftime("%H:%M")  # Pobranie aktualnej godziny w formacie HH:MM

    if current_time == "14:14":  # Określenie godziny, o której ma być uruchamiany kod
        get_data()

# Pętla "sleep loop" sprawdzająca godzinę co sekundę
def sleep_loop():
    while True:
        check_schedule()
        time.sleep(1)

# Uruchomienie pętli "sleep loop" w osobnym wątku
sleep_thread = Thread(target=sleep_loop)
sleep_thread.start()


# Funkcja obsługująca żądania HTTP i zwracająca odpowiedzi na porcie 5000/currency
@app.route('/currency')
def currency():
    # Pobranie danych z bazy danych PostgreSQL
    cur.execute("SELECT * FROM exchange.kurs ORDER BY id_waluty DESC LIMIT 33")
    data = cur.fetchall()

    # Konwersja danych na format JSON i wysłanie odpowiedzi do klienta
    rates = []
    for currency in data:
        rates.append({
            "currency": currency[1].strip(),
            'code': currency[2].strip(),
            'mid': currency[3].strip()
        })
    return jsonify({"Rates": rates})


if __name__ == '__main__':
    flask_thread = Thread(target=app.run, kwargs={'debug': False})
    flask_thread.start()