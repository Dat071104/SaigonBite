# Phase 6 deployment evidence — 27 October 2026

Deployed by Codex (AI-assisted), operated in Dat's session, on GCP account 523k0049@student.tdtu.edu.vn (billing owner: Le Minh Quan, school-managed account).

- Environment: e2-medium, asia-southeast1-b, Ubuntu `ubuntu-2404-noble-amd64-v20261024`, Docker 29.9.2, Compose 5.6.1, Caddy 2.10.2, gunicorn 23.0.0; Python 3.13.9-slim.
- Release: `https://34-21-141-239.sslip.io`, tag `p6-deploy-20261027`, commit `28d6b33d7552971c87175bb938c9107ccbf7cbaa`, image `sha256:3e6f00614af8e137a01700e113ac34a2a6493c9a461a90b9442ee64e0e20edae`; bundle SHA-256 `2d7201810652e419d19ed414cda97ac81865fac88361a4f2d2756a0f7cd9e3cf`. Clean detached checkout and container settings: `vm_final_check.txt`.
- Full test suite expected/pass 928; actual 928 passed in 51.58s: `pytest_full.txt`. Fresh tagged clone built, login, quote and persistence across restart and down/up passed: `release_persistence.txt`, `local_smoke.md` and screenshots.
- Public persistence expected same order across restart, down/up and reboot: order 9 COD/PENDING and S/D/F/Q/T 100000/0/15000/5000/110000 matched after each (`order9_*.txt`, screenshots). Subsequently the scenario changed its state and amount, as intended.
- Backup expected local + bucket with integrity ok: observed; separate restore had equal 8 orders and three sample money fields, integrity ok, login through isolated IAP tunnel passed. Real replace was NOT RUN. See `cloud_setup.md`, `restore_login.png`. Timer active (`vm_final_check.txt`).
- Scenario checks: 22/22 recorded steps passed with screenshots (`scenarios/results.json`). P5 scenarios 3–5 were adapted to existing order 9; original unrelated scenario-2 order 10 and separate seed order 7 were not asserted during that run. A later supplementary browser check confirmed seed order 7 READY and created a BT order 10 visible to the BT kitchen; this was not contemporaneous with the earlier isolation and pickup tests (`scenario_prerequisites/results.json`). Cross-hub access, replacement/acceptance, kitchen transitions, pickup race, incorrect cash and paid delivery were exercised.
- HTTPS expected valid certificate and redirect: Let's Encrypt YE1, expires 25 January 2027 13:35:03 UTC; HTTP 308; session Secure, HttpOnly, SameSite=Lax. Invalid CSRF returned 400; whole SQLite logical-row digest identical before/after (`security_public.json`, `db_digest_before.txt`, `db_digest_after.txt`), not a claim about non-database effects.
- Production secret guard passed with absent and throwaway test secrets; actual VM env root-owned mode 600, secret set length 64 without recording its value (`production_*.txt`, `vm_final_check.txt`). Gitleaks review: 66 metadata false positives, zero confirmed credentials in scanned release candidate; scanner limitations and scope `gitleaks_review.md`.
- Concurrency: 20 clients × 10 public GETs, 200/200 HTTP 200, zero errors, 3.33 s total, slowest 1187.99 ms (`performance.json`). This concurrency maximum is separate from the single-request latency target.
- Uptime check NOT SET: optional monitoring API not enabled and no notification address supplied. Budget is alerts-only, credits excluded, billing-account scope accepted by owner; alert email not yet verified. Budget is not a spending cap. A project SSH public key was temporarily added by gcloud; owner approved the exception and exact-key-only removal, which was completed and verified; `Part2/notes/P6/gcloud_log.md`.
- Rollback to a previous image NOT RUN: initial release has no previous image. Persistent disk is not a backup. Automated snapshot schedule attached; real snapshot creation at next schedule not asserted.

## Warm requests over public HTTPS

20 measured complete response bodies per page after two warmups from operator PC; nearest-rank p95. Expected each measured response under 1000 ms; all measured single requests met this target. Role-authenticated requests except the public concurrency test.

| Page | Min ms | Median ms | p95 ms | Max ms |
|---|---:|---:|---:|---:|
| customer_browse | 67.45 | 70.51 | 89.37 | 92.83 |
| quote | 69.27 | 73.47 | 109.16 | 120.6 |
| order | 68.75 | 81.06 | 104.62 | 107.86 |
| receipt | 66.47 | 70.52 | 79.17 | 107.67 |
| kitchen_queue | 65.04 | 68.71 | 73.42 | 79.93 |
| shipper_ready_board | 70.34 | 75.88 | 79.41 | 82.7 |
| admin_catalogue | 60.1 | 64.03 | 70.45 | 80.35 |
| manager_report | 64.65 | 69.34 | 80.28 | 375.59 |

## Screenshots

- `invalid_csrf.png`
- `local_order_9.png`
- `local_quote.png`
- `public_persistence_before.png`
- `public_persistence_created.png`
- `public_persistence_quote.png`
- `public_persistence_reboot.png`
- `public_persistence_recreate.png`
- `public_persistence_restart.png`
- `restore_login.png`
- `scenarios/S3_1_customer_existing_order.png`
- `scenarios/S3_2_kitchen_board.png`
- `scenarios/S3_3_other_hub_board.png`
- `scenarios/S3_4_other_hub_get.png`
- `scenarios/S3_5_other_hub_post.png`
- `scenarios/S3_6_order_detail.png`
- `scenarios/S4_1_mark_sold_out.png`
- `scenarios/S4_2_offer.png`
- `scenarios/S4_3_customer_offer.png`
- `scenarios/S4_4_accept.png`
- `scenarios/S4_5a_confirm.png`
- `scenarios/S4_5b_prepare.png`
- `scenarios/S4_5c_ready.png`
- `scenarios/S4_6_customer_ready.png`
- `scenarios/S4_7_restore_availability.png`
- `scenarios/S5_1a_shipper_board.png`
- `scenarios/S5_1b_second_shipper_board.png`
- `scenarios/S5_2a_pickup_winner.png`
- `scenarios/S5_2b_pickup_loser.png`
- `scenarios/S5_3_incorrect_cash.png`
- `scenarios/S5_4_delivered.png`
- `scenarios/S5_5_customer_receipt.png`

Supplementary screenshots: `scenario_prerequisites/seed_order_7.png`, `bt_order_created.png`, `bt_correct_hub.png`.
