import time
import json
import psycopg2
import redis
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Állandók a riasztási küszöbhöz
ALERT_INTERVAL = timedelta(seconds=60)  # Minimum 1 perc különbség a riasztások között
MAX_ALERTS_PER_HOUR = 5  # Maximum 5 riasztás óránként

BASE_DIR = Path(__file__).resolve().parent.parent
BOTS_DIR = BASE_DIR / 'callisto' / 'bots'

# PostgreSQL adatbázis kapcsolat
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="PSQ**1",
    host="127.0.0.1",
    port="5432"
)
cursor = conn.cursor()

# Redis kapcsolat
redis_client = redis.StrictRedis(
    host='localhost', 
    port=6379, 
    db=0, 
    password='callisto2024', 
    decode_responses=True
)

# Ellenőrzés, hogy küldhetünk-e riasztást
def can_send_alert(component):
    current_time = datetime.now()
    alert_key = f"alert_{component}_last_sent"
    count_key = f"alert_{component}_count"

    # Az utolsó riasztás idejének lekérdezése Redis-ből
    last_sent_str = redis_client.get(alert_key)
    if last_sent_str:
        last_sent = datetime.fromisoformat(last_sent_str)
        if current_time - last_sent < ALERT_INTERVAL:
            print(f"Riasztás túl gyakori: {component} (várakozás szükséges)")
            return False
    else:
        last_sent = None

    # Riasztási számláló frissítése
    alert_count = int(redis_client.get(count_key) or 0)
    if last_sent and current_time - last_sent > timedelta(hours=1):
        # Ha több mint egy óra eltelt, számláló visszaállítása
        redis_client.set(count_key, 0)
        alert_count = 0

    if alert_count < MAX_ALERTS_PER_HOUR:
        # Riasztási idő és számláló frissítése
        redis_client.set(alert_key, current_time.isoformat())
        redis_client.incr(count_key)
        return True
    else:
        print(f"A {component} riasztások száma elérte az óránkénti maximumot.")
        return False

# Fő funkció az adatok ellenőrzésére
def check_alerts():
    # A legutóbbi Redis bejegyzés lekérdezése
    redis_data_list = redis_client.lrange('system_data', -10, -1)  # Az utolsó 10 bejegyzés lekérdezése
    if not redis_data_list:
        print("Nincsenek adatok a Redis-ben.")
        return

    # Utolsó Redis bejegyzés kinyerése
    latest_data = json.loads(redis_data_list[-1])  # Az utolsó bejegyzés
    cpu_percent = latest_data.get("cpu_percent")

    print(f"Ellenőrzött Redis bejegyzés: CPU használat: {cpu_percent}%")

    # PostgreSQL lekérdezés a riasztási értékekhez
    cursor.execute('SELECT id, name, component, alert_value, "chatID", "alertMessage" FROM alert_savedalert')
    alerts = cursor.fetchall()

    for alert in alerts:
        id, name, component, alert_value, chatID, alertMessage = alert

        # Csak a "cpu" komponensre vonatkozó riasztásokat nézzük
        if component == "cpu" and cpu_percent >= alert_value:
            if can_send_alert(component):
                print(f"Riasztás! {alertMessage}: {cpu_percent}% >= {alert_value}%")

                # A 'name' mező értékét Python szkriptként futtatjuk
                script_path = BOTS_DIR / f"{name}.py"
                try:
                    print(f"A(z) {script_path} szkript futtatása...")
                    subprocess.run(["python3", script_path], check=True)
                    print(f"{script_path} szkript sikeresen lefutott.")
                except subprocess.CalledProcessError as e:
                    print(f"Hiba történt a(z) {script_path} futtatása közben: {e}")

# Időzített ciklus 5 másodpercenként
try:
    while True:
        check_alerts()
        time.sleep(5)
except KeyboardInterrupt:
    print("A program leállt.")

# Adatbázis kapcsolat bezárása
cursor.close()
conn.close()
