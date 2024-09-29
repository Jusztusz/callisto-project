import subprocess
import json
import time

# A szolgáltatások neveit tartalmazó fájl elérési útja
json_file_path = 'choosen_services.json'

def load_chosen_services(file_path):
    """Beolvassa a kiválasztott szolgáltatásokat a megadott JSON fájlból."""
    try:
        with open(file_path, 'r') as file:
            services = json.load(file)
            return services
    except FileNotFoundError:
        print(f"Hiba: A '{file_path}' fájl nem található.")
        return []
    except json.JSONDecodeError:
        print(f"Hiba: A '{file_path}' fájl nem érvényes JSON.")
        return []

def check_service_status(service_name):
    """Ellenőrzi, hogy egy adott szolgáltatás aktív-e."""
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', service_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()  # Visszaadjuk az állapotot: "active", "inactive", "failed", meg mit tom én mi lehet még
    except subprocess.CalledProcessError:
        return "unknown"  # Ha hiba lép fel, az állapot ismeretlen

def monitor_services():
    """A szolgáltatások állapotát 10 másodpercenként ellenőrzi."""
    while True:
        # A szolgáltatások beolvasása a JSON fájlból
        chosen_services = load_chosen_services(json_file_path)

        if chosen_services:
            # Állapotok lekérdezése minden kiválasztott szolgáltatásra
            service_statuses = {service: check_service_status(service) for service in chosen_services}

            # Eredmény mentése egy új JSON fájlba
            with open('service_statuses.json', 'w') as outfile:
                json.dump(service_statuses, outfile, indent=4)

            print("Szolgáltatások állapota frissítve és elmentve a 'service_statuses.json' fájlba.")
        else:
            print("Nincsenek kiválasztott szolgáltatások.")

        # 10 másodperc várakozás
        time.sleep(3)

if __name__ == "__main__":
    try:
        monitor_services()  # A szolgáltatások folyamatos ellenőrzése
    except KeyboardInterrupt:
        print("\nA program leállt.")
