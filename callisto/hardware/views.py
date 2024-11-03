from django.shortcuts import render
import aioredis
import json
from django.http import JsonResponse
import math
import psutil

async def fetch_last_n_data(redis_client, timeToSeconds = 60, numberOfPoints=30):
    # Lekérjük az utolsó n elemet a Redis listából
    data = await redis_client.lrange("system_data", -timeToSeconds, -1)
    cpu_data = []
    ram_used_mb = []
    disk_usage_uvulv_mb = []
    disk_usage_sda2_mb = []
    disk_usage_sda1_mb = []
    timestamps = []
    # Adatok kinyerése másodperc szerint
    for item in data:
        entry = json.loads(item)  # JSON formátum visszaállítása
        cpu_percent = entry.get('cpu_percent', 0)
        ramUMB = entry.get('ram_used', 0)
        diskUMB = entry.get('disk_usages')
        currentDisks = json.loads(diskUMB)
        for i in range(len(currentDisks)):
            match currentDisks[i].get("name"):
                case "ubuntu--vg-ubuntu--lv":
                    disk_usage_uvulv_mb.append(currentDisks[i])
                case "sda2":
                    disk_usage_sda2_mb.append(currentDisks[i])
                case "sda1":
                    disk_usage_sda1_mb.append(currentDisks[i])
                case _:
                    print("Fasz")
        
        
        metric_date = entry.get('datetime', 'N/A')
        cpu_data.append(cpu_percent)
        ram_used_mb.append(ramUMB)
        timestamps.append(metric_date)

    # Pie Chart adatok a háttértárakhoz
    disk_pie_chart_data = [] 
    disk_pie_chart_data.append(disk_usage_uvulv_mb[-1])
    disk_pie_chart_data.append(disk_usage_sda2_mb[-1])
    disk_pie_chart_data.append(disk_usage_sda1_mb[-1])

    disk_pie_chart_data

    # Adatpontok listájának mérete
    cpu_list_size = len(cpu_data)
    ram_list_size = len(ram_used_mb)
    disk_uvulv_size = len(disk_usage_uvulv_mb)
    disk_sda2_size = len(disk_usage_sda2_mb)
    disk_sda1_size = len(disk_usage_sda1_mb)

    # Csoportméretek a lista hossza és a megjelenítendő pontok alapján
    cpu_size_of_group = math.floor(cpu_list_size / numberOfPoints)
    ram_size_of_group = math.floor(ram_list_size / numberOfPoints)
    disk_uvulv_size_group = math.floor(disk_uvulv_size / numberOfPoints)
    disk_sda2_size_group = math.floor(disk_sda2_size / numberOfPoints)
    disk_sda1_size_group = math.floor(disk_sda1_size / numberOfPoints)

    # Csoportok átlagainak tárolása
    cpu_data_avg = []
    ram_data_avg = []
    disk_uvulv_obj = {"name": "", "total" : 0, "disk_uvulv_avg": []}
    disk_sda2_obj = {"name": "", "total" : 0, "disk_sda2_avg": []}
    disk_sda1_obj = {"name": "", "total" : 0, "disk_sda1_avg": []}
    disk_uvulv_avg = []
    disk_sda2_avg = []
    disk_sda1_avg = []

    # Időpontok meghatározása (mindegyiknél megegyezik az adatpontok vételezése miatt)
    timestamps_of_last_item = []

    # Adatok összeállítása a grafikonhoz
    for i in range(numberOfPoints):
        
        # Csoportok létrehozása
        cpu_group = cpu_data[i*cpu_size_of_group: (i*cpu_size_of_group)+cpu_size_of_group]
        ram_group = ram_used_mb[i*ram_size_of_group: (i*ram_size_of_group)+ram_size_of_group]
        disk_uvulv_group = disk_usage_uvulv_mb[i*disk_uvulv_size_group: (i*disk_uvulv_size_group)+disk_uvulv_size_group]
        disk_sda2_group = disk_usage_sda2_mb[i*disk_sda2_size_group: (i*disk_sda2_size_group)+disk_sda2_size_group]
        disk_sda1_group = disk_usage_sda1_mb[i* disk_sda1_size_group: (i* disk_sda1_size_group)+ disk_sda1_size_group]

        #print(disk_uvulv_group)
        # CPU csoport átlaga
        cpu_average = sum(cpu_group) / len(cpu_group)
        cpu_data_avg.append(cpu_average)

        # MEMORY csoport átlaga
        ram_average = sum(ram_group) / len(ram_group)
        ram_data_avg.append(ram_average)


        # Ide egy függvény kell (optimalizálás)
        disk_uvulv_sum = 0
        for disk_uvulv in disk_uvulv_group:
            disk_uvulv_sum = disk_uvulv_sum + disk_uvulv.get("used")
        disk_uvulv_average = disk_uvulv_sum / len(disk_uvulv_group)
        disk_uvulv_avg.append(disk_uvulv_average)

        # uvulv DISKPART átlaga
        disk_sda2_sum = 0
        for disk_sda2 in disk_sda2_group:
            disk_sda2_sum = disk_sda2_sum + disk_sda2.get("used")
        disk_sda2_average = disk_sda2_sum / len(disk_sda2_group)
        disk_sda2_avg.append(disk_sda2_average)

        disk_sda1_sum = 0
        for disk_sda1 in disk_sda1_group:
            disk_sda1_sum = disk_sda1_sum + disk_sda1.get("used")
        disk_sda1_average = disk_sda1_sum / len(disk_sda1_group)
        disk_sda1_avg.append(disk_sda1_average)


        # Időpontok (mindegyiknél megegyezik az adatpontok vételezése miatt)
        timeOfTheItems = timestamps[i* cpu_size_of_group]
        timestamps_of_last_item.append(timeOfTheItems)


    # Adatok visszaküldése a grafikonok felépítéséhez

    # Ide egy osztály kell, példányok létrehozása (optimalizálás) 
    disk_uvulv_name = disk_usage_uvulv_mb[0].get("name")
    disk_uvulv_total = disk_usage_uvulv_mb[0].get("total")
    disk_uvulv_obj["name"] = disk_uvulv_name
    disk_uvulv_obj["total"] = disk_uvulv_total
    disk_uvulv_obj["disk_uvulv_avg"] = disk_uvulv_avg

    disk_sda2_name = disk_usage_sda2_mb[0].get("name")
    disk_sda2_total = disk_usage_sda2_mb[0].get("total")
    disk_sda2_obj["name"] = disk_sda2_name
    disk_sda2_obj["total"] = disk_sda2_total
    disk_sda2_obj["disk_sda2_avg"] = disk_sda2_avg

    disk_sda1_name = disk_usage_sda1_mb[0].get("name")
    disk_sda1_total = disk_usage_sda1_mb[0].get("total")
    disk_sda1_obj["name"] = disk_sda1_name
    disk_sda1_obj["total"] = disk_sda1_total
    disk_sda1_obj["disk_sda1_avg"] = disk_sda1_avg
    
    return cpu_data_avg, ram_data_avg, timestamps_of_last_item, disk_uvulv_obj, disk_sda2_obj, disk_sda1_obj, disk_pie_chart_data

async def get_new_data(request):
    data = request.GET.get('data')
    data2 = json.loads(str(data))

    redis_client = await aioredis.from_url("redis://localhost:6379", password="callisto2024")

    cpu_data, ram_used_mb, timestamps, disk_uvulv, disk_sda2, disk_sda1, disk_pie_chart_data = await fetch_last_n_data(redis_client, data2.get("timeToSeconds"), data2.get("numberOfPoints") )  # Lekérjük az utolsó 30 elemet
    await redis_client.close()
    
    # JSON válasz a frontend számára
    return JsonResponse({
        'cpu_data': cpu_data,
        'ram_used_mb': ram_used_mb,
        'timestamps': timestamps,
        'disk_uvulv': disk_uvulv,
        'disk_sda2' : disk_sda2,
        'disk_sda1' : disk_sda1,
        'disk_pie_chart_data': disk_pie_chart_data
    })

async def hardware(request):
    redis_client = await aioredis.from_url("redis://localhost:6379", password="callisto2024")
    cpu_data, ram_used_mb, timestamps, disk_uvulv, disk_sda2, disk_sda1, disk_pie_chart_data = await fetch_last_n_data(redis_client, 30)
    await redis_client.close()

    return render(request, "hardware/hardware.html", {
        'cpu_data': cpu_data,
        'ram_used_mb': ram_used_mb,
        'timestamps': timestamps,
        'disk_uvulv': disk_uvulv,
        'disk_sda2': disk_sda2,
        'disk_sda1' : disk_sda1,
        'disk_pie_chart_data' : disk_pie_chart_data
    })