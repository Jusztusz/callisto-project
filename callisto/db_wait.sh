#!/bin/bash
# wait-for-it.sh script

# Az adatbázis elérhetőségének ellenőrzése
nc -z $1 $2
while [ $? -ne 0 ]; do
  echo "Waiting for $1:$2..."
  sleep 2
  nc -z $1 $2
done
echo "$1:$2 is available"