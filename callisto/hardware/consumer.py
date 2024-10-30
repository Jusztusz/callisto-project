import json
import psutil as ps
import subprocess
import math as m
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import datetime
import aioredis

class CPUConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Statikus adatok egyszeri küldése a kapcsolat létrejöttekor
        cpu_info = self.get_cpu_info()
        core_count = ps.cpu_count()
        ram_all = m.ceil(ps.virtual_memory()[0] / (1024 ** 3))  # GB

        static_data = {
            'cpu_type': cpu_info,
            'core_count': core_count,
            'ram_all': ram_all,
        }

        await self.send(text_data=json.dumps(static_data))

        # Aszinkron Redis kapcsolat létrehozása
        self.redis = await aioredis.from_url("redis://127.0.0.1:6379", password="callisto2024")

        # Folyamatosan frissítendő dinamikus adatok küldése
        while True:
            cpu_freq_current = round(ps.cpu_freq().current)
            cpu_percent = round(ps.cpu_percent())
            ram_available = round(ps.virtual_memory()[1] / (1024 ** 2))  # MB
            ram_used = round(ps.virtual_memory()[3] / (1024 ** 2))  # MB
            ram_used_percent = round(ps.virtual_memory()[2], 1)  # %
            disk_usages = []
            for partition in ps.disk_partitions():
                if any(partition.device.startswith(prefix) for prefix in ('/dev/loop', '/dev/sr', '/dev/ram')):
                    continue
                
                usage = ps.disk_usage(partition.mountpoint)
                disk_usages.append({
                    'name': partition.device.split('/')[-1],  # Meghajtó neve
                    'used': usage.used // (1024 ** 2),  # Használt tárhely MB-ban
                    'total': usage.total // (1024 ** 2)  # Teljes méret MB-ban
                })

            # Aktuális idő emberi olvasható formátumban
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Dátum és idő

            dynamic_data = {
                'datetime': current_time,  # Emberi formátumú dátum
                'cpu_freq_current': cpu_freq_current,
                'cpu_percent': cpu_percent,
                'ram_available': ram_available,
                'ram_used': ram_used,
                'ram_used_percent': ram_used_percent,
                'disk_usages': json.dumps(disk_usages)  # Lista JSON formátumba alakítása
            }

            # Küldjük az aktuális adatokat a kliensnek
            await self.send(text_data=json.dumps(dynamic_data))

            # Tároljuk el az adatokat Redis-ben
            await self.redis.rpush("system_data", json.dumps(dynamic_data))

            # Várjunk 1 másodpercet a következő frissítésig
            await asyncio.sleep(1)

    async def disconnect(self, close_code):
        await self.redis.close()  # Zárd be a Redis kapcsolatot

    def get_cpu_info(self):
        try:
            cpu_info = subprocess.check_output("cat /proc/cpuinfo", shell=True).decode('utf-8')
            for line in cpu_info.split("\n"):
                if "model name" in line:
                    return line.split(":")[1].strip()
        except Exception as e:
            return str(e)
