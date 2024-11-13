import psutil
import json
import asyncio
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer

class networkConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.prev_bytes_sent = None  # Az első adatnál ne számoljon
        self.prev_bytes_recv = None  # Az első adatnál ne számoljon

    async def connect(self):
        # WebSocket kapcsolat
        self.room_group_name = "network_data"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

        # Adatok folyamatos küldése másodpercenként
        await self.send_periodic_data()

    async def disconnect(self, close_code):
        # WebSocket bontás
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        pass

    async def send_network_data(self):
        # Psutil hálózati statisztikák lekérése
        net_io = psutil.net_io_counters()

        # A jelenlegi időpont lekérése (dátum formátumban)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Ha az előző adat nem null, akkor végezzük el a különbség kiszámítását
        if self.prev_bytes_sent is not None and self.prev_bytes_recv is not None:
            sent_delta = net_io.bytes_sent - self.prev_bytes_sent
            recv_delta = net_io.bytes_recv - self.prev_bytes_recv
        else:
            sent_delta = 0
            recv_delta = 0

        # Az adatokat JSON formátumban küldjük
        data = {
            'timestamp': timestamp,  # Dátum és idő
            'bytes_sent': sent_delta,  # Az aktuális küldött adat
            'bytes_recv': recv_delta   # Az aktuális fogadott adat
        }

        # Az új értékek tárolása a következő iterációra
        self.prev_bytes_sent = net_io.bytes_sent
        self.prev_bytes_recv = net_io.bytes_recv

        # Az adatokat WebSocket-en keresztül küldjük
        await self.send(text_data=json.dumps(data))

    async def send_periodic_data(self):
        while True:
            await self.send_network_data()
            await asyncio.sleep(1)  # 1 másodpercenként küldjük az adatokat
