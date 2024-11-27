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
    openssh-client \
    && apt-get clean

# A repó klónozása
RUN git clone -b prod --single-branch https://github.com/Jusztusz/callisto-project.git

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
RUN rm -r /etc/nginx/sites-available/default
RUN rm -r /etc/nginx/sites-enabled/default
RUN sed -i 's/^user www-data;/user root;/' /etc/nginx/nginx.conf

# Redis config módosítás
RUN sed -i 's/# requirepass .*/requirepass callisto2024/' /etc/redis/redis.conf

# SSH
USER root

RUN mkdir -p /app/.ssh && \
    chmod 700 /app/.ssh && \
    ssh-keygen -t rsa -b 2048 -f /app/.ssh/id_rsa -N "" && \
    chmod 600 /app/.ssh/id_rsa && \
    chmod 644 /app/.ssh/id_rsa.pub && \
    cat /app/.ssh/id_rsa.pub

# PostgreSQL és Django alkalmazás elindítása
CMD service postgresql start && \
    service redis-server start && \
    service nginx start && \
    /app/venv/bin/python3 /app/callisto-project/callisto/manage.py migrate && \
    #/app/venv/bin/python3 /app/callisto-project/callisto/manage.py runserver 0.0.0.0:8001
    cat /app/.ssh/id_rsa.pub && tail -f /dev/null
