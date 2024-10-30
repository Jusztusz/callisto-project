from django.shortcuts import render
import aioredis
import json
from django.http import JsonResponse
import math

async def fetch_last_n_data(redis_client, timeToSeconds, numberOfPoints=30):
    # Lekérjük az utolsó n elemet a Redis listából
    data = await redis_client.lrange("system_data", -timeToSeconds, -1)
    cpu_data = []
    ram_used_mb = []
    timestamps = []

    for item in data:
        entry = json.loads(item)  # JSON formátum visszaállítása
        cpu_percent = entry.get('cpu_percent', 0)
        ramUMB = entry.get('ram_used', 0)
        metric_date = entry.get('datetime', 'N/A')

        cpu_data.append(cpu_percent)
        ram_used_mb.append(ramUMB)
        timestamps.append(metric_date)

    print(cpu_data)
    listSize = len(data)
    print(timeToSeconds)
    sizeOfGroup = math.ceil(listSize / numberOfPoints)
    print(sizeOfGroup)

    for i in range(timeToSeconds):
        print("i: " + str(i*sizeOfGroup) + " " + "end: " + str((i*sizeOfGroup)+20))
        group = cpu_data[i*sizeOfGroup: (i*sizeOfGroup)+sizeOfGroup]
        print(group)


    return cpu_data, ram_used_mb, timestamps

async def get_new_data(request):
    data = request.GET.get('data')
    data2 = json.loads(str(data))

    redis_client = await aioredis.from_url("redis://localhost:6379", password="callisto2024")


    cpu_data, ram_used_mb, timestamps = await fetch_last_n_data(redis_client, data2.get("timeToSeconds"), data2.get("numberOfPoints") )  # Lekérjük az utolsó 30 elemet
    await redis_client.close()
    
    # JSON válasz a frontend számára
    return JsonResponse({
        'cpu_data': cpu_data,
        'ram_used_mb': ram_used_mb,
        'timestamps': timestamps,
    })

async def hardware(request):
    redis_client = await aioredis.from_url("redis://localhost:6379", password="callisto2024")
    cpu_data, ram_used_mb, timestamps = await fetch_last_n_data(redis_client, 30)
    await redis_client.close()

    return render(request, "hardware/hardware.html", {
        'cpu_data': cpu_data,
        'ram_used_mb': ram_used_mb,
        'timestamps': timestamps,
    })