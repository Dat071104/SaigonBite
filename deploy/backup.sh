#!/bin/bash
set -Eeuo pipefail

# The VM's metadata identity and project must match before any local or cloud write.
expected_account='saigonbite-vm@kinetic-magnet-512406-m3.iam.gserviceaccount.com'
expected_project='kinetic-magnet-512406-m3'
expected_bucket='saigonbite-backups-kinetic-magnet-512406-m3'
metadata='http://metadata.google.internal/computeMetadata/v1'
account=$(curl --fail --silent --show-error -H 'Metadata-Flavor: Google' "$metadata/instance/service-accounts/default/email")
project=$(curl --fail --silent --show-error -H 'Metadata-Flavor: Google' "$metadata/project/project-id")
[[ "$account" == "$expected_account" && "$project" == "$expected_project" ]] || { echo 'Identity or project mismatch; backup aborted' >&2; exit 1; }
export CLOUDSDK_CONFIG=/srv/saigonbite/gcloud
config="$CLOUDSDK_CONFIG/configurations/config_saigonbite"
[[ -f "$config" ]] || { echo 'Missing isolated gcloud configuration' >&2; exit 1; }
grep -Fxq "account = $expected_account" "$config" && grep -Fxq "project = $expected_project" "$config" || { echo 'gcloud configuration mismatch' >&2; exit 1; }

umask 077
backup_dir=/srv/saigonbite/backups
db=/srv/saigonbite/data/saigonbite.db
[[ -f "$db" ]] || { echo 'Database missing; backup aborted' >&2; exit 1; }
mkdir -p "$backup_dir"
stamp=$(date -u +%Y%m%dT%H%M%SZ)
tmp=$(mktemp "$backup_dir/.backup.XXXXXXXX.db")
trap 'rm -f -- "$tmp"' EXIT
python3 - "$db" "$tmp" <<'PY'
import sqlite3, sys
src = sqlite3.connect('file:' + sys.argv[1] + '?mode=ro', uri=True, timeout=30)
dst = sqlite3.connect(sys.argv[2])
with dst:
    src.backup(dst)
result = dst.execute('PRAGMA integrity_check').fetchone()[0]
dst.close(); src.close()
if result != 'ok':
    raise SystemExit('integrity_check failed')
print('integrity_check=ok')
PY
archive="$backup_dir/saigonbite-$stamp.db.gz"
gzip -c "$tmp" > "$archive"
gcloud storage cp "$archive" "gs://$expected_bucket/$(basename "$archive")" --configuration=saigonbite --project="$expected_project" --account="$expected_account" --quiet
echo "backup_created=$(basename "$archive")"
# Keep only the seven newest local archives created by this script, after upload succeeds.
mapfile -t old < <(find "$backup_dir" -maxdepth 1 -type f -name 'saigonbite-*.db.gz' -printf '%f\n' | sort -r | tail -n +8)
for f in "${old[@]}"; do rm -f -- "$backup_dir/$f"; done
