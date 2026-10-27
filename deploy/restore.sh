#!/bin/bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run as root' >&2; exit 1; }
[[ $# -ge 1 && $# -le 2 && ( $# -eq 1 || "$2" == '--replace' ) ]] || { echo 'Usage: restore.sh /srv/saigonbite/backups/<file>.db.gz [--replace]' >&2; exit 2; }
root=/srv/saigonbite
metadata=http://metadata.google.internal/computeMetadata/v1
project=$(curl -fsS -H 'Metadata-Flavor: Google' "$metadata/project/project-id")
account=$(curl -fsS -H 'Metadata-Flavor: Google' "$metadata/instance/service-accounts/default/email")
[[ "$project" == kinetic-magnet-512406-m3 && "$account" == saigonbite-vm@kinetic-magnet-512406-m3.iam.gserviceaccount.com ]] || { echo 'VM identity or project mismatch' >&2; exit 1; }
source=$(realpath -e -- "$1")
[[ "$source" == "$root/backups/"*.db.gz ]] || { echo 'Backup must be in the approved local backup directory' >&2; exit 1; }
stamp=$(date -u +%Y%m%dT%H%M%SZ)
dest="$root/restore-check/$stamp"
[[ ! -e "$dest" ]] || { echo 'Restore directory already exists' >&2; exit 1; }
umask 077
mkdir -p "$dest"
gzip -dc -- "$source" > "$dest/saigonbite.db"
python3 - "$dest/saigonbite.db" <<'PY'
import sqlite3, sys
with sqlite3.connect('file:' + sys.argv[1] + '?mode=ro', uri=True) as conn:
    result = conn.execute('PRAGMA integrity_check').fetchone()[0]
    print('integrity_check=' + result)
    print('order_count=' + str(conn.execute('select count(*) from orders').fetchone()[0]))
    if result != 'ok': raise SystemExit('restore failed integrity check')
PY
chown -R 10001:10001 "$dest"
echo "restored_path=$dest/saigonbite.db"
if [[ ${2:-} == --replace ]]; then
    [[ -L "$root/current" ]] || { echo 'No current release; refusing replacement' >&2; exit 1; }
    compose="$root/current/deploy/compose.prod.yml"
    docker compose --env-file "$root/.env" -p saigonbite -f "$compose" stop app
    rollback_dir="$root/backups/pre-restore-$stamp"
    mkdir "$rollback_dir"
    for suffix in '' '-wal' '-shm'; do
        if [[ -e "$root/data/saigonbite.db$suffix" ]]; then mv -- "$root/data/saigonbite.db$suffix" "$rollback_dir/"; fi
    done
    cp -- "$dest/saigonbite.db" "$root/data/saigonbite.db"
    chown 10001:10001 "$root/data/saigonbite.db"
    docker compose --env-file "$root/.env" -p saigonbite -f "$compose" up -d app
    echo "previous_database_saved=$rollback_dir"
fi
