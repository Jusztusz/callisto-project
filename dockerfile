# Python alap image
FROM python:3.10-slim

# A munkakönyvtár beállítása
WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    nginx \
    && apt-get clean

# A repó klónozása
RUN git clone https://github.com/Jusztusz/callisto-project.git

# Virtuális környezet létrehozása
RUN python3 -m venv /app/venv

# A csomagok telepítése a virtuális környezetbe (ha később szeretnéd használni)
RUN /app/venv/bin/pip install --no-cache-dir -r /app/callisto-project/requirements.txt

# A Python script futtatása a .env fájl generálásához
RUN python3 /app/callisto-project/callisto/create_env.py

RUN cp /app/callisto-project/callisto/nginx.conf /etc/nginx/nginx.conf

