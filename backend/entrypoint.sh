#!/bin/sh
set -e  # Exit immediately if any command fails

# Implement robust Python-based socket check to wait for PostgreSQL readiness
echo "Verifying PostgreSQL readiness..."
python3 -c "
import socket
import time
import os
import sys

host = os.getenv('POSTGRES_HOST', 'database')
try:
    port = int(os.getenv('POSTGRES_PORT', '5432'))
except ValueError:
    port = 5432

print(f'Checking port {port} on host {host}...')
start_time = time.time()
while time.time() - start_time < 60:
    try:
        with socket.create_connection((host, port), timeout=2):
            print('PostgreSQL database is ready and accepting traffic.')
            sys.exit(0)
    except OSError:
        print('PostgreSQL is not yet reachable, sleeping 1s...')
        time.sleep(1)
print('Error: Database connection timeout exceeded.')
sys.exit(1)
"

# Run collectstatic for Django Admin and backend assets
echo "Running collectstatic..."
python manage.py collectstatic --no-input

# Run database migrations (removed makemigrations as it is an anti-pattern in prod)
echo "Applying database migrations..."
python manage.py migrate --no-input

# Handoff execution to Gunicorn via exec so it runs under PID 1 (proper signal propagation)
echo "Starting production Gunicorn server..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
