import json
import paramiko
import math as m
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import datetime


class CPUConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        ssh_client = self.get_ssh_client()

        try:
            cpu_info = self.get_cpu_info(ssh_client)
            core_count = self.get_core_count(ssh_client)
            ram_all = self.get_total_ram(ssh_client)

            static_data = {
                'cpu_type': cpu_info,
                'core_count': core_count,
                'ram_all': ram_all,
            }

            await self.send(text_data=json.dumps(static_data))

            while True:
                cpu_freq_current = self.get_cpu_frequency(ssh_client)
                cpu_percent = self.get_cpu_percent(ssh_client)
                ram_stats = self.get_ram_stats(ssh_client)
                disk_usages = self.get_disk_usages(ssh_client)

                # Aktuális idő emberi olvasható formátumban
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Dátum és idő

                dynamic_data = {
                    'datetime': current_time,  # Emberi formátumú dátum
                    'cpu_freq_current': cpu_freq_current,
                    'cpu_percent': cpu_percent,
                    'ram_available': ram_stats['available'],
                    'ram_used': ram_stats['used'],
                    'ram_used_percent': ram_stats['percent'],
                    'disk_usages': json.dumps(disk_usages)  # Lista JSON formátumba alakítása
                }

                # Küldjük az aktuális adatokat a kliensnek
                await self.send(text_data=json.dumps(dynamic_data))

                # Várjunk 1 másodpercet a következő frissítésig
                await asyncio.sleep(1)
        finally:
            ssh_client.close()

    def get_ssh_client(self):
        """SSH kapcsolat létrehozása."""
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect('192.168.1.201', username='callisto', password='callisto2024')
        return ssh_client

    def execute_command(self, ssh_client, command):
        """Távoli parancs futtatása és eredményének visszaadása."""
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode().strip()
        return output

    def get_cpu_info(self, ssh_client):
        """CPU típusa."""
        command = "cat /proc/cpuinfo | grep 'model name' | head -n 1 | awk -F ': ' '{print $2}'"
        return self.execute_command(ssh_client, command)

    def get_core_count(self, ssh_client):
        """CPU magok száma."""
        command = "nproc"
        return int(self.execute_command(ssh_client, command))

    def get_total_ram(self, ssh_client):
        """Teljes RAM mérete GB-ban."""
        command = "free -g | grep Mem | awk '{print $2}'"
        return int(self.execute_command(ssh_client, command))

    def get_cpu_frequency(self, ssh_client):
        """Aktuális CPU frekvencia MHz-ben."""
        command = "lscpu | grep 'CPU MHz' | awk -F ': ' '{print $2}'"
        return round(float(self.execute_command(ssh_client, command)))

    def get_cpu_percent(self, ssh_client):
        """CPU kihasználtság százalékban."""
        command = "top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'"
        return round(float(self.execute_command(ssh_client, command)))

    def get_ram_stats(self, ssh_client):
        """RAM statisztikák MB-ban."""
        command = "free -m | grep Mem"
        output = self.execute_command(ssh_client, command)
        parts = output.split()
        return {
            'total': int(parts[1]),         # Összes RAM MB
            'available': int(parts[6]),     # Elérhető RAM MB
            'used': int(parts[2]),          # Használt RAM MB
            'percent': round((int(parts[2]) / int(parts[1])) * 100, 1)  # Használat százalékban
        }

    def get_disk_usages(self, ssh_client):
        """Lemezhasználati adatok lekérdezése."""
        command = "df -m | grep '^/dev/'"
        output = self.execute_command(ssh_client, command)
        disk_usages = []
        for line in output.splitlines():
            parts = line.split()
            disk_usages.append({
                'name': parts[0].split('/')[-1],  # Meghajtó neve
                'used': int(parts[2]),           # Használt hely MB-ban
                'total': int(parts[1])           # Teljes méret MB-ban
            })
        return disk_usages
