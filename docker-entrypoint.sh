#!/bin/sh
set -e
DB="${SAIGONBITE_DATABASE:-instance/saigonbite.db}"
if [ ! -f "$DB" ]; then
    python init_db.py --db "$DB"
fi
exec "$@"
