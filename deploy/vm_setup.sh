#!/bin/bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || { echo 'Run as root' >&2; exit 1; }
[[ $# -eq 1 && "$1" =~ ^[A-Za-z0-9.-]+$ ]] || { echo 'Usage: vm_setup.sh <hostname>' >&2; exit 2; }
host=$1
expected_account='saigonbite-vm@kinetic-magnet-512406-m3.iam.gserviceaccount.com'
expected_project='kinetic-magnet-512406-m3'
metadata='http://metadata.google.internal/computeMetadata/v1'
account=$(curl -fsS -H 'Metadata-Flavor: Google' "$metadata/instance/service-accounts/default/email")
project=$(curl -fsS -H 'Metadata-Flavor: Google' "$metadata/project/project-id")
[[ "$account" == "$expected_account" && "$project" == "$expected_project" ]] || { echo 'VM identity or project mismatch' >&2; exit 1; }

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y ca-certificates curl git gnupg python3
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
arch=$(dpkg --print-architecture)
. /etc/os-release
cat > /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: ${UBUNTU_CODENAME:-$VERSION_CODENAME}
Components: stable
Architectures: $arch
Signed-By: /etc/apt/keyrings/docker.asc
EOF
cloud_package=()
if ! command -v gcloud >/dev/null 2>&1; then
    curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /etc/apt/keyrings/google-cloud.gpg
    echo 'deb [signed-by=/etc/apt/keyrings/google-cloud.gpg] https://packages.cloud.google.com/apt cloud-sdk main' > /etc/apt/sources.list.d/google-cloud-sdk.list
    cloud_package=(google-cloud-cli)
fi
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin "${cloud_package[@]}"
systemctl enable --now docker
if [[ ! -e /swapfile ]]; then
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
fi
if ! swapon --show=NAME --noheadings | grep -Fxq /swapfile; then swapon /swapfile; fi
grep -Fqx '/swapfile none swap sw 0 0' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
install -d -m 0755 /srv/saigonbite/{releases,data,backups,caddy_data,caddy_config,bin}
chown 10001:10001 /srv/saigonbite/data
chmod 700 /srv/saigonbite/backups
install -d -m 0700 /srv/saigonbite/gcloud/configurations
printf '[core]\naccount = %s\nproject = %s\ndisable_usage_reporting = True\n' "$expected_account" "$expected_project" > /srv/saigonbite/gcloud/configurations/config_saigonbite
chmod 600 /srv/saigonbite/gcloud/configurations/config_saigonbite
if [[ ! -e /srv/saigonbite/.env ]]; then
    umask 077
    python3 - "$host" <<'PY' > /srv/saigonbite/.env
import secrets, sys
print('SAIGONBITE_ENV=production')
print('SAIGONBITE_DATABASE=/data/saigonbite.db')
print('SAIGONBITE_SECRET_KEY=' + secrets.token_urlsafe(48))
print('SITE_HOST=' + sys.argv[1])
print('RELEASE_TAG=UNDEPLOYED')
PY
fi
chmod 600 /srv/saigonbite/.env
chown root:root /srv/saigonbite/.env
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
install -m 0700 "$script_dir/backup.sh" /srv/saigonbite/bin/backup.sh
install -m 0644 "$script_dir/saigonbite-backup.service" /etc/systemd/system/saigonbite-backup.service
install -m 0644 "$script_dir/saigonbite-backup.timer" /etc/systemd/system/saigonbite-backup.timer
systemctl daemon-reload
systemctl enable --now saigonbite-backup.timer
echo 'VM setup complete; secret set in root-only env file (value not displayed).'
