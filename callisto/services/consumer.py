import json
import subprocess
from channels.generic.websocket import WebsocketConsumer

class DataConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()  # Elfogadja a WebSocket kapcsolatot

    def receive(self, text_data):
        # Itt fogadjuk a WebSocket-en érkező adatokat
        json_data = json.loads(text_data)  # JSON formátumra konvertáljuk
        print(f"Received data: {json_data}")

        # Szolgáltatások lekérdezése
        if json_data.get('action') == 'get_services':
            services = self.get_services()
            self.send(text_data=json.dumps({
                'message': 'A rendszer szolgáltatásai és állapotuk:',
                'services': services
            }))

        # Szolgáltatások mentése
        elif json_data.get('action') == 'save_services':
            self.save_chosen_services(json_data.get('services', []))
            self.send(text_data=json.dumps({
                'message': 'Kiválasztott szolgáltatások mentve!',
            }))

    def get_services(self):
        """Lekérdezi a rendszer szolgáltatásait és állapotukat."""
        try:
            # Szolgáltatások listázása
            result = subprocess.run(
                ['systemctl', 'list-unit-files', '--type=service', '--no-pager'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )

            services_output = result.stdout  # A parancs kimenete
            services_list = services_output.splitlines()  # Sorokba bontás

            services = []
            for line in services_list:
                if not line.strip() or '@' in line:  # Üres sorok és "@"-val ellátott sorok kihagyása
                    continue
                parts = line.split()
                service_name = parts[0]
                service_state = parts[1] if len(parts) > 1 else "N/A"

                # Állapot lekérdezése
                status_result = subprocess.run(
                    ['systemctl', 'is-active', service_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False  # Hiba esetén ne dobjon kivételt
                )
                service_status = status_result.stdout.strip()  # Szolgáltatás állapotának lekérése

                services.append({'name': service_name, 'state': service_status})

        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e.stderr}")
            services = []  # Hiba esetén üres lista

        return services

    def save_chosen_services(self, services):
        """Elmenti a kiválasztott szolgáltatásokat egy JSON fájlba."""
        filename = 'chosen_services.json'
        with open(filename, 'w') as file:
            json.dump(services, file)  # Mentsd el a szolgáltatásokat JSON fájlba

    def disconnect(self, close_code):
        print("WebSocket disconnected")
