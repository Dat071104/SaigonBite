#!/bin/bash
set -Eeuo pipefail
[[ $EUID -eq 0 && ${1:-} == --confirm-reset && $# -eq 1 ]] || { echo 'Usage: sudo reset_demo.sh --confirm-reset' >&2; exit 2; }
root=/srv/saigonbite
metadata=http://metadata.google.internal/computeMetadata/v1
project=$(curl -fsS -H 'Metadata-Flavor: Google' "$metadata/project/project-id")
account=$(curl -fsS -H 'Metadata-Flavor: Google' "$metadata/instance/service-accounts/default/email")
[[ "$project" == kinetic-magnet-512406-m3 && "$account" == saigonbite-vm@kinetic-magnet-512406-m3.iam.gserviceaccount.com ]] || { echo 'VM identity or project mismatch' >&2; exit 1; }
[[ -L "$root/current" && -f "$root/data/saigonbite.db" ]] || { echo 'No current release or database' >&2; exit 1; }
"$root/bin/backup.sh"
compose="$root/current/deploy/compose.prod.yml"
docker compose --env-file "$root/.env" -p saigonbite -f "$compose" stop app
saved="$root/backups/pre-reset-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir "$saved"
for suffix in '' '-wal' '-shm'; do
    if [[ -e "$root/data/saigonbite.db$suffix" ]]; then mv -- "$root/data/saigonbite.db$suffix" "$saved/"; fi
done
docker compose --env-file "$root/.env" -p saigonbite -f "$compose" up -d app
echo "previous_database_saved=$saved"
