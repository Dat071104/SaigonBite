#!/bin/bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run as root' >&2; exit 1; }
[[ $# -eq 2 && "$1" =~ ^p6-deploy-[0-9]{8}$ && -f "$2" ]] || { echo 'Usage: deploy.sh p6-deploy-YYYYMMDD /absolute/path/release.bundle' >&2; exit 2; }
tag=$1
bundle=$(realpath "$2")
root=/srv/saigonbite
metadata=http://metadata.google.internal/computeMetadata/v1
project=$(curl -fsS -H 'Metadata-Flavor: Google' "$metadata/project/project-id")
account=$(curl -fsS -H 'Metadata-Flavor: Google' "$metadata/instance/service-accounts/default/email")
[[ "$project" == kinetic-magnet-512406-m3 && "$account" == saigonbite-vm@kinetic-magnet-512406-m3.iam.gserviceaccount.com ]] || { echo 'VM identity or project mismatch' >&2; exit 1; }
[[ ! -e "$root/releases/$tag" ]] || { echo 'Release directory already exists; inspect it before resuming' >&2; exit 1; }
if [[ -f "$root/data/saigonbite.db" ]]; then "$root/bin/backup.sh"; fi
git clone --no-local "$bundle" "$root/releases/$tag"
git -C "$root/releases/$tag" checkout --detach "refs/tags/$tag"
[[ -z "$(git -C "$root/releases/$tag" status --porcelain)" ]] || { echo 'Release checkout is not clean' >&2; exit 1; }
docker build -t "saigonbite:$tag" "$root/releases/$tag"
old=$(readlink "$root/current" || true)
python3 - "$root/.env" "$tag" <<'PY'
import os, sys, tempfile
path, tag = sys.argv[1:]
lines = open(path, encoding='utf-8').read().splitlines()
assert sum(line.startswith('RELEASE_TAG=') for line in lines) == 1
lines = [('RELEASE_TAG=' + tag if line.startswith('RELEASE_TAG=') else line) for line in lines]
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix='.env.')
try:
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as f: f.write('\n'.join(lines) + '\n')
    os.replace(tmp, path)
finally:
    if os.path.exists(tmp): os.unlink(tmp)
PY
install -m 0700 "$root/releases/$tag/deploy/backup.sh" "$root/bin/backup.sh"
docker compose --env-file "$root/.env" -p saigonbite -f "$root/releases/$tag/deploy/compose.prod.yml" up -d
host=$(sed -n 's/^SITE_HOST=//p' "$root/.env")
[[ "$host" =~ ^[A-Za-z0-9.-]+$ ]] || { echo 'Invalid host' >&2; exit 1; }
healthy=0
for ((i=0; i<30; i++)); do
    if curl -fsS "https://$host/" -o /dev/null; then healthy=1; break; fi
    sleep 5
done
[[ $healthy -eq 1 ]] || { echo 'HTTPS did not become healthy; inspect before retrying' >&2; exit 1; }
if [[ -n "$old" ]]; then ln -sfn "$old" "$root/previous"; fi
ln -sfn "$root/releases/$tag" "$root/current"
previous_tag=${old##*/}
for release in "$root"/releases/p6-deploy-*; do
    [[ -d "$release/.git" ]] || continue
    candidate=${release##*/}
    [[ "$candidate" =~ ^p6-deploy-[0-9]{8}$ ]] || continue
    [[ "$candidate" == "$tag" || "$candidate" == "$previous_tag" ]] && continue
    if docker image inspect "saigonbite:$candidate" >/dev/null 2>&1; then
        docker image rm "saigonbite:$candidate"
    fi
done
printf 'tag=%s\ncommit=%s\nimage_id=%s\n' "$tag" "$(git -C "$root/current" rev-parse HEAD)" "$(docker image inspect --format '{{.Id}}' "saigonbite:$tag")"
