# 5.2 Deployment and recovery

The Part 2 demonstration runs at [https://saigonbite.io.vn](https://saigonbite.io.vn) (fallback [https://34-21-141-239.sslip.io](https://34-21-141-239.sslip.io)) on one Singapore e2-medium Ubuntu VM with Docker Compose, gunicorn and Caddy HTTPS. SQLite resides on a 30 GiB persistent disk; daily disk snapshots and an independent off-VM bucket copy support recovery. The VM's restricted service account has bucket-scoped object creation and reading access; no service-account key is used. The tagged release was transferred as a verified Git bundle. See `deploy/RUNBOOK.md` and `docs/part2/test_report/deploy_2026-10-27/README.md` for operations and evidence.

The full suite passed 928 tests. A new checkout built and ran locally, and public order 9 retained its money and payment fields through application restart, Compose down/up and VM reboot. An online backup passed integrity checking and was copied off VM; a separate restore matched order count and sample money fields and supported a customer login. Live replacement was not exercised. The deployed browser checks exercised kitchen isolation, substitution, acceptance, preparation, a pickup race and COD delivery using an adapted existing order; the BT order and READY seed order were subsequently checked separately, rather than at the same moment as the main scenario run.

HTTPS certificate validation, redirect, secure cookie attributes and rejected invalid CSRF passed. A SQLite state digest matched before and after invalid CSRF. Twenty warm requests per page had the following timings in milliseconds; one concurrent opening test returned 200/200 successful responses with no errors.

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

The estimated cost is approximately ₫1.31 million per month under the explicit assumptions in `Part2/notes/P6/cost_estimate.md`. Actual usage and billing may differ; the approved trial budget sends alerts and does not cap spending. The first release has no prior image to roll back to. Verify the budget email and actual billing, and download a final backup before trial expiry on 21 January 2027.
