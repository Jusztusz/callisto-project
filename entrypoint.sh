#!/bin/bash

# Systemd daemon újratöltése
echo "Reloading systemd daemon..."
systemctl daemon-reload || echo "systemctl daemon-reload failed (not running systemd)"

# Callisto service indítása
echo "Starting Callisto service..."
systemctl start callisto.service || echo "Failed to start Callisto service (not running systemd)"

# Nginx újraindítása
echo "Restarting Nginx..."
service nginx restart

# PostgreSQL indítása
echo "Starting PostgreSQL..."
service postgresql start

# Redis indítása
echo "Starting Redis..."
service redis-server start

# Django migrációk
echo "Applying Django migrations..."
/app/venv/bin/python /app/callisto-project/callisto/manage.py migrate

# Django szerver indítása
echo "Starting Django server..."
exec /app/venv/bin/python /app/callisto-project/callisto/manage.py runserver 0.0.0.0:8000
