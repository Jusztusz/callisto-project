# Python alap image
FROM python:3.9-slim

# A munkakönyvtár beállítása
WORKDIR /app

RUN apt-get update && apt-get install -y git

# A repó klónozása
RUN git clone https://github.com/Jusztusz/callisto-project.git

# Virtuális környezet létrehozása
RUN python3 -m venv /app/venv

# A csomagok telepítése a virtuális környezetbe (ha később szeretnéd használni)
RUN /app/venv/bin/pip install --no-cache-dir -r /app/callisto-project/requirements.txt
# A Python script futtatása a .env fájl generálásához
RUN python3 /app/callisto-project/callisto/create_env.py

# A Django szerver futtatása a virtuális környezetből
CMD ["/app/venv/bin/python3", "/app/callisto-project/callisto/manage.py", "runserver", "0.0.0.0:8000"]
