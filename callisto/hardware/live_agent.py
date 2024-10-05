import psutil as ps
import subprocess
import math as m
    
def get_cpu_info():
    try:
        cpu_info = subprocess.check_output("cat /proc/cpuinfo", shell=True).decode('utf-8')
        for line in cpu_info.split("\n"):
            if "model name" in line:
                return line.split(":")[1].strip()
    except Exception as e:
        return str(e)

# Proci adatok
cpu_type = get_cpu_info()
core_count = ps.cpu_count()
cpu_freq_current = round(ps.cpu_freq([0]))
# Memória adatok
ram_all = m.ceil(ps.virtual_memory()[0]/(1024 ** 3)) #GB
ram_available = round(ps.virtual_memory()[1]/(1024 ** 3)) #GB
ram_used = round(ps.virtual_memory()[3]/(1024 ** 3)) #GB
ram_used_percent = round(ps.virtual_memory()[2],1) #%