import time
import json
import psycopg2
import redis
import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

ALERT_INTERVAL = timedelta(seconds=300)
MAX_ALERTS_PER_HOUR = 5 

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

def can_send_alert(component):
    current_time = datetime.now()
    alert_key = f"alert_{component}_last_sent"
    count_key = f"alert_{component}_count"

    last_sent_str = redis_client.get(alert_key)
    if last_sent_str:
        last_sent = datetime.fromisoformat(last_sent_str)
        if current_time - last_sent < ALERT_INTERVAL:
            print(f"Riasztás túl gyakori: {component} (várakozás szükséges)")
            return False
    else:
        last_sent = None

    alert_count = int(redis_client.get(count_key) or 0)
    if last_sent and current_time - last_sent > timedelta(hours=1):
        redis_client.set(count_key, 0)
        alert_count = 0

    if alert_count < MAX_ALERTS_PER_HOUR:
        redis_client.set(alert_key, current_time.isoformat())
        redis_client.incr(count_key)
        return True
    else:
        print(f"A {component} riasztások száma elérte az óránkénti maximumot.")
        return False

def check_alerts():
    redis_data_list = redis_client.lrange('system_data', -10, -1)
    if not redis_data_list:
        print("Nincsenek adatok a Redis-ben.")
        return

    latest_data = json.loads(redis_data_list[-1])
    cpu_percent = latest_data.get("cpu_percent")

    print(f"Ellenőrzött Redis bejegyzés: CPU használat: {cpu_percent}%")

    cursor.execute('SELECT id, name, component, alert_value, "chatID", "alertMessage" FROM alert_savedalert')
    alerts = cursor.fetchall()

    for alert in alerts:
        id, name, component, alert_value, chatID, alertMessage = alert

        if component == "cpu" and cpu_percent >= alert_value:
            if can_send_alert(component):
                print(f"Riasztás! {alertMessage}: {cpu_percent}% >= {alert_value}%")

                script_path = BOTS_DIR / f"{name}.py"
                try:
                    print(f"A(z) {script_path} szkript futtatása...")
                    subprocess.run(["python3", script_path], check=True)
                    print(f"{script_path} szkript sikeresen lefutott.")
                except subprocess.CalledProcessError as e:
                    print(f"Hiba történt a(z) {script_path} futtatása közben: {e}")

try:
    while True:
        check_alerts()
        time.sleep(5)
except KeyboardInterrupt:
    print("A program leállt.")

cursor.close()
conn.close()
