#!/bin/sh
# Create and seed instance/saigonbite.db on first start; keep it on later starts.
set -e
if [ ! -f instance/saigonbite.db ]; then
    python init_db.py
fi
exec "$@"
