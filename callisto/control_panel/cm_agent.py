import psutil as ps
import datetime
import json
import asyncio
import redis.asyncio as aioredis

class SystemMonitor:
    def __init__(self):
        # Redis aszinkron kapcsolat létrehozása
        self.redis = aioredis.from_url("redis://127.0.0.1:6379", db=0, password="callisto2024")

    async def collect_and_push_data(self):
        while True:
            cpu_freq_current = round(ps.cpu_freq().current)
            cpu_percent = round(ps.cpu_percent())
            ram_available = round(ps.virtual_memory().available / (1024 ** 2))  # MB
            ram_used = round(ps.virtual_memory().used / (1024 ** 2))  # MB
            ram_used_percent = round(ps.virtual_memory().percent, 1)  # %

            disk_usages = []
            for partition in ps.disk_partitions():
                if any(partition.device.startswith(prefix) for prefix in ('/dev/loop', '/dev/sr', '/dev/ram')):
                    continue
                usage = ps.disk_usage(partition.mountpoint)
                disk_usages.append({
                    'name': partition.device.split('/')[-1],
                    'used': usage.used // (1024 ** 2),
                    'total': usage.total // (1024 ** 2)
                })

            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            dynamic_data = {
                'datetime': current_time,
                'cpu_freq_current': cpu_freq_current,
                'cpu_percent': cpu_percent,
                'ram_available': ram_available,
                'ram_used': ram_used,
                'ram_used_percent': ram_used_percent,
                'disk_usages': json.dumps(disk_usages)
            }

            # Adatok aszinkron feltöltése Redis listába
            await self.redis.rpush("system_data", json.dumps(dynamic_data))

            # 5 másodperces várakozás az új mérés előtt
            await asyncio.sleep(1)

# Aszinkron környezet futtatása
async def main():
    monitor = SystemMonitor()
    await monitor.collect_and_push_data()

# Program elindítása
asyncio.run(main())