import subprocess
import re
import json

def list_physical_disks():
    result = subprocess.run(['sudo', 'fdisk', '-l'], capture_output=True, text=True)

    # Regex a fizikai lemezek kinyerésére
    disk_pattern = re.compile(r"^Disk (/dev/sda\w*): (\d+\.?\d*) ([TGMK]iB), (\d+) bytes, (\d+) sectors$", re.MULTILINE)
    # Regex a diszk modelljének kinyerésére
    model_pattern = re.compile(r"^Disk model: (.+)$", re.MULTILINE)

    # Keresd meg az összes fizikai lemezt és a modelljeiket
    disk_matches = disk_pattern.findall(result.stdout)
    model_matches = model_pattern.findall(result.stdout)

    # A fizikai lemezek információi
    disks = []
    for i in range(len(disk_matches)):
        device, size, unit, bytes, sectors = disk_matches[i]
        model = model_matches[i] if i < len(model_matches) else "Unknown"

        disk_info = {
            "device": device,
            "size": f"{size} {unit}",
            "bytes": bytes,
            "sectors": sectors,
            "model": model
        }
        disks.append(disk_info)

    # Csak a /dev/sda kifejezést tartalmazó diszkek szűrése
    filtered_disks = [disk for disk in disks if re.search(r"/dev/sda", disk['device'])]

    # Eredmények kiírása egy JSON fájlba
    with open('disks.json', 'w') as json_file:
        json.dump(filtered_disks, json_file, indent=4)
    
    return disk_info

list_physical_disks()
