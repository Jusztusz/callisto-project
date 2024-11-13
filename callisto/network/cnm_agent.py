import psutil as p

network_data = p.net_io_counters(pernic=True)

for interface, stats in network_data.items():
    print(f"Interface: {interface}")
    print(f"  Bytes Sent: {stats.bytes_sent}")
    print(f"  Bytes Received: {stats.bytes_recv}")
    print(f"  Packets Sent: {stats.packets_sent}")
    print(f"  Packets Received: {stats.packets_recv}")
    print("----------")