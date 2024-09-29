#!/bin/bash
#systemctl list-units --type=service --all --no-pager > collected_services | awk '$3 !="not-found" {print $1 " " $3}' | grep -E '\.service' > collected_services 
while true; do
    # Minden telepített szolgáltatás lekérdezése, figyelmen kívül hagyva a dinamikus szolgáltatásokat
    systemctl list-unit-files --type=service --no-pager | grep -v '@' | awk '{print $1 " " $2}' | grep -E '\.service' | while read -r line; do
        service=$(echo "$line" | awk '{print $1}')
        status=$(systemctl is-active "$service")

        # Ellenőrizzük, hogy a python script létezik-e
        if [[ -f send_service_data.py ]]; then
            # A Python script futtatása
            python3 send_service_data.py "$service" "$status"
            if [[ $? -ne 0 ]]; then
                echo "Hiba a $service státuszának elküldésekor."
            fi
        else
            echo "A send_service_data.py fájl nem található."
        fi
    done
    sleep 10
done