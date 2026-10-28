# SaigonBite Part 2 deployment and recovery runbook

Status: deployed and verified at https://34-21-141-239.sslip.io. Release `p6-deploy-20261027`, commit `28d6b33d7552971c87175bb938c9107ccbf7cbaa`, image `sha256:3e6f00614af8e137a01700e113ac34a2a6493c9a461a90b9442ee64e0e20edae`. This is the first release; no previous image exists for rollback. Use synthetic demo data only. Deployed by Codex (AI-assisted), operated in Dat's session, on GCP account `523k0049@student.tdtu.edu.vn` (billing owner: Le Minh Quan, school-managed account).

## Scope and costs

Project `kinetic-magnet-512406-m3`, zone `asia-southeast1-b`; one e2-medium VM, 30 GiB pd-balanced boot disk (auto-delete off), static Premium IPv4, web firewall and IAP-only SSH, one restricted service account, backup bucket, and daily disk snapshots. This uses a free-trial billing account, not an upgrade. Budget `saigonbite-trial` is alerts-only with credits excluded and actual thresholds 33%, 67%, 90%; owner accepted its billing-account scope because the project filter was unavailable. Budget alerts are not spending limits. Estimate: about ₫1.31 million/month, conditional on traffic, backup size, exchange rate and taxes; see `Part2/notes/P6/cost_estimate.md` in the working directory.

On the operator's computer every `gcloud` command must include `--configuration=saigonbite`. Do not activate or alter the default configuration. Check project and school account before cloud writes. On the VM, the only gcloud use is backup/restore, authenticated as `saigonbite-vm@kinetic-magnet-512406-m3.iam.gserviceaccount.com`; the backup script checks metadata identity, project and its exact bucket before writing. No service-account key is used.

SSH lại bằng `gcloud compute ssh --tunnel-through-iap` với `--configuration=saigonbite`; gcloud tự thêm khóa, xong việc thì kiểm tra và xóa đúng khóa vừa thêm, không thay đổi các metadata khác.

## Local reproducible path

```sh
git clone https://github.com/Dat071104/SaigonBite
cd SaigonBite
git checkout v0.9-part2   # reviewer tag is available only after P7
docker compose up --build -d
```

Open http://127.0.0.1:5000 and use the demo accounts in the README. The persistent named volume initializes only if its database does not exist. Run `docker compose logs -f web`; stop with `docker compose down`. Run `python -m pytest -q` in a full checkout with dependencies installed: tests require Git history and do not run in the image. A deliberate local reset is `docker compose down -v`, which deletes the local demo volume; never use it against a production database.

## VM setup and release

Run from the operator machine after verifying the account, project, bundle digest and VM identity:

```sh
gcloud compute scp --tunnel-through-iap --zone=asia-southeast1-b --configuration=saigonbite RELEASE.bundle saigonbite-vm:/tmp/saigonbite-release.bundle
gcloud compute ssh saigonbite-vm --tunnel-through-iap --zone=asia-southeast1-b --configuration=saigonbite --strict-host-key-checking=no
```

On the VM, clone the uploaded bundle into a clean staging directory, checkout the local release tag and run the setup from that checkout (replace placeholders with the verified tag and hostname):

```sh
git clone /tmp/saigonbite-release.bundle /tmp/saigonbite-bootstrap
git -C /tmp/saigonbite-bootstrap checkout --detach p6-deploy-YYYYMMDD
sudo /tmp/saigonbite-bootstrap/deploy/vm_setup.sh A-B-C-D.sslip.io
sudo /tmp/saigonbite-bootstrap/deploy/deploy.sh p6-deploy-YYYYMMDD /tmp/saigonbite-release.bundle
```

Setup checks VM metadata identity/project, installs Docker Engine and Compose, creates 2 GiB swap and directories, makes a VM-only isolated gcloud configuration for backup, generates the application secret into `/srv/saigonbite/.env` as root mode 600, and enables a 20:00 UTC backup timer. It never prints the secret. Deploy clones the exact bundle tag into `/srv/saigonbite/releases`, backs up an existing DB, builds the tagged image, starts Compose and waits for HTTPS. `current` and `previous` symlinks identify the current and prior release. The verified tag, commit, image ID and URL are recorded above and in the Phase 6 deployment evidence.

## Operations

```sh
sudo docker compose --env-file /srv/saigonbite/.env -p saigonbite -f /srv/saigonbite/current/deploy/compose.prod.yml ps
sudo docker compose --env-file /srv/saigonbite/.env -p saigonbite -f /srv/saigonbite/current/deploy/compose.prod.yml logs --tail=100
sudo docker compose --env-file /srv/saigonbite/.env -p saigonbite -f /srv/saigonbite/current/deploy/compose.prod.yml restart app
sudo systemctl list-timers saigonbite-backup.timer
```

Do not print or copy `/srv/saigonbite/.env` into evidence. Caddy stores certificates under `/srv/saigonbite/caddy_data`; SQLite and WAL files reside in `/srv/saigonbite/data`. Containers use `unless-stopped`, limited JSON logs and application health checks. Only ports 80/443 are public; SSH is via IAP.

## Backup, restore and reset

Run `sudo /srv/saigonbite/bin/backup.sh`; it makes an online SQLite backup, checks integrity, compresses it, uploads it to the exact configured bucket, then retains seven local archives. The timer runs at 03:00 Vietnam / 20:00 UTC. Confirm both the local file and bucket object; persistent disk and snapshots do not replace a tested backup.

For a non-destructive restore test, run `sudo /srv/saigonbite/current/deploy/restore.sh /srv/saigonbite/backups/saigonbite-YYYYMMDDTHHMMSSZ.db.gz`. It creates a separate path under `restore-check` and verifies integrity; compare order count and sample money fields against the live DB, then start an isolated test container bound to `127.0.0.1:8001` and verify login through an SSH tunnel. The explicit `--replace` argument stops the app, moves the old DB and WAL/SHM aside and copies in the restored database; **do not use it during the test**. Before real replacement, verify the chosen backup, schema compatibility and a fresh off-VM backup.

For a deliberate demo reset only: `sudo /srv/saigonbite/current/deploy/reset_demo.sh --confirm-reset`. This first performs a backup, stops the app and moves the database/WAL/SHM aside; the next start initializes the demo database. Never run it automatically.

## Rollback

Keep the previous image and database backup. Before using previous code, check its expected schema against the current database; never run older code against an incompatible newer schema. If compatible, stop the active application, restore a verified compatible backup if needed, set `RELEASE_TAG` in the root-only env file without revealing the secret, and use the previous release's Compose file to start its image. Verify HTTPS, login, order state and the backup timer. Rollback is an operator action and has not been exercised until evidence says otherwise.

## Demo day and shutdown

- Check URL, certificate, login for all demo roles, current order flow, health, disk space, latest backup and timer. Keep local Docker as a fallback.
- Review Billing → Reports 24 hours after starting the VM and at regular intervals; budget emails can be delayed. Do not upgrade billing.
- Before **21 January 2027**, download and verify a final backup, then decide with the account owner whether to delete all phase-created billable resources or let the trial lapse. A stopped VM can still incur disk/IP/snapshot/storage charges; check each retained item and the billing account. Deletion protection and disk auto-delete off are intentional, so shutdown requires deliberate handling.


## Custom domain — 28 October 2026

Primary URL: https://saigonbite.io.vn; https://www.saigonbite.io.vn redirects there with HTTP 301. Fallback: https://34-21-141-239.sslip.io. Tenten DNS records `@` and `www` both use A record `34.21.141.239`; the domain expires 28 October 2027 and automatic renewal was off in the registrar. VM trial expiry is earlier: 21 January 2027. Release `p6-deploy-20261028` at commit `55df8ae431aa2288c562cc4d82d702bc4cc97aad`; image `sha256:432106755fdf4bf9802a87f0484ea8f39705ae9a938c8a5bf740d1a598add619`. The `p6-deploy-` tag namespace is required by the existing deployment script. Certificates are managed by Caddy; keep ports 80/443 and DNS pointed to this VM for issuance/renewal.
