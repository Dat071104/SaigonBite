# 5.1 Testing: Test Plan and Test Cases

Author: 722I0004 · AI-assisted (Codex, Claude)

## Test plan

The tests are derived from the postconditions (PC) and minimum guarantees (MG) of the six main use cases in section 2.2: every PC and MG has at least one automated test that sets up the precondition, runs the system operation and checks the stored result in the database. Four levels of testing were run. All tests were written and run by 722I0004 with AI assistance (Appendix 5); expected results were written before each run.

| Level | What is tested | Tool and environment | When | Entry criterion | Exit criterion | Result |
|---|---|---|---|---|---|---|
| 1. Unit and postcondition tests | Domain rules, controllers and DAOs; every PC/MG; concurrency (two customers for the last slot, two shippers for one order); rollback on failure; role access to all 547 route/role pairs | pytest 9.1.1, Python 3.13.2, Windows 11; a new SQLite database for every test | 24–27/10/2026; full rerun before every gate commit | Code of the use case complete; fixtures seeded | All tests pass on a clean clone | **928 passed**, 0 failed (27/10/2026, commit 252ada1, 52.6 s); rerun 28/10/2026 at 97574bd: 928 passed |
| 2. Integration (cross-role, browser) | Seven scenarios follow one order through Admin → Customer → Kitchen → Shipper → Manager, including replacement, rejection, cancellation, failed delivery, plus a CSRF check | Playwright 1.64.1 driving Microsoft Edge; local Flask server; one browser profile per role; fresh database | 27/10/2026 | Level 1 passes; expected amounts computed by hand and hashed before the run | Every step matches its expected result | **60 / 60 steps** pass (4.3.6) |
| 3. System test on the deployed VM | The main flows on the public HTTPS site; restart, container recreation and VM reboot keep the data; backup and restore | Google Cloud VM, Docker Compose, gunicorn, Caddy (HTTPS) | 27–28/10/2026 | Level 2 passes; release deployed | All steps pass; order survives reboot | **22 / 22 steps** pass (5.2) |
| 4. Non-functional | Response time of key pages, HTTPS and cookie flags, CSRF rejection, no secrets in the repository, layer dependencies | Timed HTTP requests, browser checks, gitleaks, import-policy test | 27/10/2026 | Deployed site reachable | Thresholds of NFR-04, NFR-06–NFR-08, NFR-10 met | All met (1.7, verification summary) |

**How to repeat level 1.** From a full clone of the repository (the tests read the Git history, so the Docker image does not contain them):

```
git clone https://github.com/Dat071104/SaigonBite.git
cd SaigonBite
git checkout v0.9-part2
python -m venv .venv
.venv\Scripts\activate          (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
python -m pytest -q
```

**Defects and regression.** Levels 1–3 found the defects below that the earlier level could not see. Each fix received a regression test where code changed, and the whole level 1 suite and all browser scenarios were rerun from a fresh database before the gate was closed.

| Defect | Found at | Severity | What happened | Fix (commit) | Retest |
|---|---|---|---|---|---|
| P5-D01 | Level 2, UC-06 | Medium | The dish form refused normal prices (number input step) | Template fix (b68bfef) | All scenarios rerun: pass |
| P5-D02 | Level 2, UC-01 | Medium | Every online order showed a false "price changed" warning | Template and script fix (ce18bf6) | All scenarios rerun: pass |
| P5-D03 | Level 2, UC-02 | Low–medium | A shipper who lost the race saw a dead-end error page | Error page links back (1776293) | Step 5.2 rerun: pass |
| P5-D04 | Level 2, UC-01 | Low | Distance printed with 17 decimals in the quote table | Format to 2 decimals (5466f6a) | All scenarios rerun: pass |
| P5-D05 | Level 2, UC-05 | Low | Order page said "to be refunded" instead of "refund owed, payout pending" | Wording fix (252ada1) | All scenarios rerun: pass |
| P5-D06 | Level 2, UC-05 | Low (wording) | The decline banner always mentions an online refund, also for COD | Not fixed (accepted; no data or money effect) | — |

## Test cases derived from postconditions

One row per postcondition (PC) or minimum guarantee (MG). "Input" and "Expected result" are the concrete values used by the first listed test; the actual result is the recorded run of 27/10/2026 at commit 252ada1, in which every listed test passed. The test name is the pytest function in `tests/`; the complete list of test functions per row is in `docs/part2/test_report/p7_2026-10-28/test_cases.csv`.

### Test cases for UC-01

| Test ID | Use case | Post-condition tested | Input / steps | Expected result | Actual result | Pass / fail | Requirements | Test (pytest function) |
|---|---|---|---|---|---|---|---|---|
| UC01-PC01 | UC-01 | one PLACED order owned by the customer | Customer 1 at hub D1, home address; 2 × Pho bo tai (55,000) + 1 × Goi cuon (35,000); COD; confirm | One PLACED order for customer 1, hub D1; lines (Pho bo tai, 55,000, 2), (Goi cuon, 35,000, 1); one COD payment PENDING 155,000; redirect to the confirmation page | As expected — all 1 cases passed | PASS | FR-14 | `test_T_UC01_10_confirm_creates_placed_order_lines_and_pending_cod_payment` (1 cases) |
| UC01-PC02 | UC-01 | lines with snapshot names/prices | Place an order, then rename the menu item; open the receipt as the owner and as another customer | Receipt shows the stored names and prices (not the new name); another customer gets 404; nothing is written | As expected — all 2 cases passed | PASS | FR-14 | `test_receipt_stored_snapshot_read_only_own_and_truthful` and 1 more (2 cases) |
| UC01-PC03 | UC-01 | address snapshot + distance | Same receipt; quotes at several distances on a fixed sphere (0 km … beyond 8 km) | Receipt shows the stored address text; distance stored with the order; radius checked on the raw distance | As expected — all 6 cases passed | PASS | FR-07, FR-14 | `test_receipt_stored_snapshot_read_only_own_and_truthful` and 1 more (6 cases) |
| UC01-PC04 | UC-01 | S/D/F/Q/T stored and consistent | Order 2 × 45,000 with a 10,000 voucher (COD and online), then cancel | S = 90,000, D = 10,000, T = 90,000 stored; T = S − D + F − Q holds | As expected — all 12 cases passed | PASS | FR-05, FR-08, FR-09, FR-10, FR-14 | `test_fixed_money_oracle_partial_then_unfulfilled_owes_full_c` and 2 more (12 cases) |
| UC01-PC05 | UC-01 | payment PENDING (COD) or PAID (ONLINE, amount C) | Local customer pays by e-wallet or bank QR, tourist by card; simulator approves or declines | Approved: payment PAID, amount = T, reference SIM-…; declined: no order, payment or line | As expected — all 7 cases passed | PASS | FR-12, FR-14 | `test_local_and_tourist_online_allowed_options_and_decline` and 1 more (7 cases) |
| UC01-PC06 | UC-01 | hub load +1 | Two orders at hub D1, then the admin lowers its capacity to 1; a third checkout | Count of active orders is 2; the third checkout is refused (hub busy); still 2 orders | As expected — all 2 cases passed | PASS | FR-06, FR-14 | `test_lower_capacity_below_load_then_checkout_refused` and 1 more (2 cases) |
| UC01-MG01 | UC-01 | refused/declined/invalid → no order, no payment, no line | Quote, then change the address, label, item or voucher so the total stays equal; confirm | Checkout refused with "quote changed"; database unchanged; no open transaction | As expected — all 18 cases passed | PASS | FR-04, FR-07, FR-09, FR-11, … | `test_equal_total_content_changes_require_new_quote` and 2 more (18 cases) |
| UC01-MG02 | UC-01 | replay → same single order | Confirm twice with the same token (second time with invalid inputs); another customer uses the token | Same order returned, nothing new created; the other customer is refused; database unchanged | As expected — all 2 cases passed | PASS | FR-13, NFR-02, NFR-12 | `test_replay_ignores_changed_current_input_but_foreign_token_never_discloses` and 1 more (2 cases) |
| UC01-MG03 | UC-01 | busy → suggestions, nothing saved | Hub full; five other hubs at different loads and distances; repeat after one more order | Suggestions [3, 4, 5], then [4, 5, 2] (load ratio, distance, ID); none when the rest are out of range; nothing saved | As expected — all 2 cases passed | PASS | FR-06 | `test_suggestion_ratio_raw_distance_id_ties_limit_and_empty` and 1 more (2 cases) |

### Test cases for UC-02

| Test ID | Use case | Post-condition tested | Input / steps | Expected result | Actual result | Pass / fail | Requirements | Test (pytest function) |
|---|---|---|---|---|---|---|---|---|
| UC02-PC01 | UC-02 | one shipper assigned, Delivery PICKED_UP, order OUT_FOR_DELIVERY | Two shippers take the same READY order at the same moment (two threads) | Exactly one "won", one "lost"; delivery PICKED_UP for the winner; order OUT_FOR_DELIVERY; one delivery row | As expected — all 1 cases passed | PASS | FR-18, FR-19 | `test_two_shippers_one_ready_order_exactly_one_persisted_claim` (1 cases) |
| UC02-PC02 | UC-02 | delivered: Delivery DELIVERED, order DELIVERED, COD PAID with cash = T | Wrong shipper tries first; assigned shipper confirms with COD cash "100,000" (or online) | Wrong shipper refused, no change; order and delivery DELIVERED; same finish time; COD PAID, cash 100,000 | As expected — all 6 cases passed | PASS | FR-20 | `test_assigned_finish_pair_states_timestamps_refund_and_repeat` (6 cases) |
| UC02-PC03 | UC-02 | failed: Delivery FAILED + reason, order DELIVERY_FAILED, BR-17 | Assigned shipper reports a failure with a reason (COD and online) | Order DELIVERY_FAILED, delivery FAILED with reason; COD VOIDED or online REFUND_PENDING with the full amount owed | As expected — all 6 cases passed | PASS | FR-21 | `test_assigned_finish_pair_states_timestamps_refund_and_repeat` (6 cases) |
| UC02-MG01 | UC-02 | second shipper / wrong shipper / wrong cash / repeat → 0 rows changed | Second shipper, wrong shipper, wrong cash amount, repeated confirmation | Each refused; zero rows changed | As expected — all 27 cases passed | PASS | FR-18, FR-19, FR-20, NFR-01, NFR-12 | `test_assigned_finish_pair_states_timestamps_refund_and_repeat` and 2 more (27 cases) |

### Test cases for UC-03

| Test ID | Use case | Post-condition tested | Input / steps | Expected result | Actual result | Pass / fail | Requirements | Test (pytest function) |
|---|---|---|---|---|---|---|---|---|
| UC03-PC01 | UC-03 | hub created/updated with valid code, coordinates, fee, capacity | Admin creates a hub, opens it, renames it to "Renamed kitchen" | HTTP 303 after each post; the hub is stored with the new name | As expected — all 1 cases passed | PASS | FR-22 | `test_admin_real_crud_and_archived_history` (1 cases) |
| UC03-PC02 | UC-03 | archived hub hidden from browse/checkout, visible in history/reports | Admin archives that hub | Hub hidden from the customer hub list and the active admin list; still listed with "include archived" | As expected — all 2 cases passed | PASS | FR-22 | `test_admin_real_crud_and_archived_history` and 1 more (2 cases) |
| UC03-MG01 | UC-03 | duplicate code / capacity < 1 / archive with open order → nothing changed | Archive a hub that has an order in each open state (PLACED … OUT_FOR_DELIVERY); duplicate code; capacity 0 | Each refused; database unchanged | As expected — all 19 cases passed | PASS | FR-22, NFR-01 | `test_every_open_state_blocks_archive` and 3 more (19 cases) |

### Test cases for UC-04

| Test ID | Use case | Post-condition tested | Input / steps | Expected result | Actual result | Pass / fail | Requirements | Test (pytest function) |
|---|---|---|---|---|---|---|---|---|
| UC04-PC01 | UC-04 | sales, workload, performance equal the hand oracle for the filter | Fixed sample: 2 delivered and 1 failed delivery in the date range across two hubs | Delivered 2, failed 1, failure rate 33.3 %, average wait 20.0 min, average ride 25.0 min; per hub (1, 0, 0 %, 10, 20) and (1, 1, 50 %, 25, 30) | As expected — all 5 cases passed | PASS | FR-23, FR-24, FR-25 | `test_delivery_means_sample_sizes_and_failure_denominator` and 4 more (5 cases) |
| UC04-PC02 | UC-04 | n/a on empty denominators | Hub 1 empty, hub 2 with one PLACED order, an archived hub with history; one READY and one OUT_FOR_DELIVERY order; an empty date range | Workload rows (hub 1, load 0), (hub 2, load 1); archived hubs are kept; READY and OUT_FOR_DELIVERY counted separately; empty range shows "n/a", not 0 | As expected — all 1 cases passed | PASS | FR-25 | `test_workload_now_retains_archived_hubs_and_empty_values` (1 cases) |
| UC04-MG01 | UC-04 | 0 rows written by any report request | Run all three reports with a SQLite authorizer that records every write attempt | No write attempted; database unchanged | As expected — all 1 cases passed | PASS | FR-23, FR-24, FR-25 | `test_reports_actual_connection_authorizer_and_unchanged_facts` (1 cases) |
| UC04-MG02 | UC-04 | non-manager denied | Call every route as every role (547 combinations), including the report routes as non-managers | Non-managers get 403/redirect to login; database unchanged | As expected — all 547 cases passed | PASS | NFR-01 | `test_route_role_matrix` and 1 more (547 cases) |

### Test cases for UC-05

| Test ID | Use case | Post-condition tested | Input / steps | Expected result | Actual result | Pass / fail | Requirements | Test (pytest function) |
|---|---|---|---|---|---|---|---|---|
| UC05-PC01 | UC-05 | confirm: own-hub PLACED → CONFIRMED | Kitchen staff of the order's hub confirm one PLACED order and reject another with "Synthetic refusal" | First CONFIRMED with confirmed_at; second REJECTED with the reason and closed_at; its COD payment VOIDED | As expected — all 1 cases passed | PASS | FR-26, FR-27, FR-30 | `test_main_kitchen_confirm_and_reject_have_exact_durable_effects` (1 cases) |
| UC05-PC02 | UC-05 | reject: REJECTED + reason + BR-17 + offer WITHDRAWN | Reject an order paid online 100,000 after an accepted cheaper replacement | Order REJECTED; payment REFUND_PENDING; amount owed 100,000 (the full captured amount) | As expected — all 7 cases passed | PASS | FR-26, FR-27 | `test_fixed_money_oracle_partial_then_unfulfilled_owes_full_c` and 1 more (7 cases) |
| UC05-PC03 | UC-05 | offer: one OFFERED offer per §3.3 | Offer a replacement under each invalid condition (dish available, archived brand, other hub, dearer target …) and once validly | Each invalid offer refused with no change; the valid one creates one OFFERED offer | As expected — all 10 cases passed | PASS | FR-28, FR-29 | `test_offer_guard_one_negative_per_condition` and 1 more (10 cases) |
| UC05-PC04 | UC-05 | accepted offer applied per §3.3 5–7 | Customer accepts a cheaper replacement: 2 × 45,000 instead of 2 × 50,000, voucher 10,000 | Line replaced; S = 90,000, D = 10,000, T = 90,000; online: PAID 100,000 with 10,000 owed back; COD: amount due 90,000 | As expected — all 10 cases passed | PASS | FR-31, FR-32, NFR-12 | `test_fixed_money_oracle_partial_then_unfulfilled_owes_full_c` and 1 more (10 cases) |
| UC05-MG01 | UC-05 | wrong hub / open offer / stale / invalid target → order unchanged | Customer accepts after the target dish was unlisted, archived or sold out | Only that offer becomes WITHDRAWN with a notice; order and payment unchanged (T 100,000, owed 0) | As expected — all 28 cases passed | PASS | FR-26, FR-28, FR-30, FR-31, … | `test_invalid_target_withdraws_only_exact_offer` and 3 more (28 cases) |

### Test cases for UC-06

| Test ID | Use case | Post-condition tested | Input / steps | Expected result | Actual result | Pass / fail | Requirements | Test (pytest function) |
|---|---|---|---|---|---|---|---|---|
| UC06-PC01 | UC-06 | brand/item created, updated, archived | Admin creates brand "New brand", renames it; creates dish "New dish" 12,000; edits it to 13,000; archives it | HTTP 303 for each; item stored as "Renamed dish", 13,000; archived_at set | As expected — all 1 cases passed | PASS | FR-36 | `test_real_brand_item_crud_and_composite_reader` (1 cases) |
| UC06-PC02 | UC-06 | listing added/removed, availability per hub | List dish 9 at hub 1 as unavailable while hub 2 keeps it available | One INSERT (1, 9, 0), no extra UPDATE; hub 1 unavailable, hub 2 available; never half-written | As expected — all 2 cases passed | PASS | FR-35, FR-37 | `test_initial_unavailable_listing_is_atomic_and_two_hubs_independent` and 1 more (2 cases) |
| UC06-PC03 | UC-06 | archived/sold-out items not orderable | Dish 9 unavailable at hub 1; brand of dish 1 archived; customer opens the hub menu; admin tries to list the dish again | Sold-out and archived dishes are not on the customer menu; the new listing is refused; nothing else changes | As expected — all 2 cases passed | PASS | FR-04 | `test_initial_unavailable_listing_is_atomic_and_two_hubs_independent` and 1 more (2 cases) |
| UC06-MG01 | UC-06 | old order lines unchanged after price change/archive | Rename, reprice and archive dishes that already appear in orders | orders, order_line, payment, replacement_offer and delivery rows unchanged | As expected — all 1 cases passed | PASS | FR-36, FR-37 | `test_every_catalogue_mutation_preserves_old_snapshot_and_money` (1 cases) |
| UC06-MG02 | UC-06 | duplicates/invalid prices refused | Duplicate brand name, duplicate dish in a brand, price 0 or negative, stale archive | Each refused; database unchanged | As expected — all 14 cases passed | PASS | FR-36, NFR-01 | `test_catalogue_checked_zero_row_outcomes` and 1 more (14 cases) |

Sources: `docs/part2/pc_mg_register.csv` (postconditions), `docs/part2/test_report/2026-10-27_252ada1.xml` (JUnit result), `docs/part2/test_report/integration_2026-10-27/` (browser run), `docs/part2/test_report/deploy_2026-10-27/` (deployed run).
