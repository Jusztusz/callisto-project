# Python alap image
FROM python:3.10-slim

# A munkakönyvtár beállítása
WORKDIR /app

# Telepítjük a szükséges csomagokat (git, nginx, PostgreSQL)
RUN apt-get update && apt-get install -y \
    git \
    nginx \
    postgresql \
    postgresql-contrib \
    redis \
    systemctl \
    && apt-get clean

# A repó klónozása
RUN git clone https://github.com/Jusztusz/callisto-project.git

# Virtuális környezet létrehozása
RUN python3 -m venv /app/venv

# A csomagok telepítése a virtuális környezetbe
RUN /app/venv/bin/pip install --no-cache-dir -r /app/callisto-project/requirements.txt

# A Python script futtatása a .env fájl generálásához
RUN python3 /app/callisto-project/callisto/create_env.py

# PostgreSQL adatbázis beállítása
RUN service postgresql start && \
    su postgres -c "psql -c \"ALTER USER postgres WITH PASSWORD 'PSQ**1';\"" && \
    su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;\"" && \
    service postgresql stop

# Nginx konfiguráció másolása
RUN cp /app/callisto-project/callisto/callisto-nginx /etc/nginx/sites-available
RUN ln -s /etc/nginx/sites-available/callisto-nginx /etc/nginx/sites-enabled/callisto-nginx

# Redis config módosítás
RUN sed -i 's/# requirepass .*/requirepass callisto2024/' /etc/redis/redis.conf

# PostgreSQL és Django alkalmazás elindítása
CMD service postgresql start && \
    service redis-server start && \
    service nginx start && \
    /app/venv/bin/python3 /app/callisto-project/callisto/manage.py migrate && \
    /app/venv/bin/python3 /app/callisto-project/callisto/manage.py runserver 0.0.0.0:8001
