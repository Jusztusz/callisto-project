import json
import os
import paramiko
from channels.generic.websocket import WebsocketConsumer

class DataConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        print("WebSocket disconnected")

    def receive(self, text_data):
        json_data = json.loads(text_data)
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

        # Szolgáltatás állapotok frissítése
        elif json_data.get('action') == 'get_service_statuses':
            statuses = self.get_service_statuses()
            self.send(text_data=json.dumps({
                'message': 'Frissített szolgáltatások állapota',
                'service_statuses': statuses
            }))

    def get_services(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        services = []
        try:
            ssh_client.connect('192.168.1.201', username='callisto', password='callisto2024')

            stdin, stdout, stderr = ssh_client.exec_command('systemctl list-unit-files --type=service --no-pager')
            services_output = stdout.read().decode()
            services_list = services_output.splitlines()

            for line in services_list:
                if not line.strip() or '@' in line:
                    continue
                parts = line.split()
                service_name = parts[0]
                services.append({'name': service_name})

        except Exception as e:
            print(f"Error connecting via SSH: {e}")
        finally:
            ssh_client.close()

        return services

    def save_chosen_services(self, services):
        filename = 'choosen_services.json'
        with open(filename, 'w') as file:
            json.dump(services, file)

    def get_service_statuses(self):
        filename = 'choosen_services.json'
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                chosen_services = json.load(file)

            service_statuses = []
            for service in chosen_services:
                status = self.get_service_status(service)
                service_statuses.append({'name': service, 'status': status})

            return service_statuses
        else:
            return []

    def get_service_status(self, service_name):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect('192.168.1.201', username='callisto', password='callisto2024')

            stdin, stdout, stderr = ssh_client.exec_command(f'systemctl is-active {service_name}')
            status = stdout.read().decode().strip()
            return status

        except Exception as e:
            print(f"Error getting status for {service_name}: {e}")
            return 'unknown'
        finally:
            ssh_client.close()
