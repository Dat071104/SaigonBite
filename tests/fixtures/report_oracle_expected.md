# Independent report oracle

Author: 722I0004 · AI-assisted (Codex).
Written before any production report query executes on this dataset. Hand arithmetic only.

Vietnam day 20 October 2026 is UTC [19 October 17:00, 20 October 17:00).
Eligible sales IDs: 101 and 102. 102 finishes at 23:59 Vietnam; 103 at 00:01 the next day is excluded; 104 finishes at 23:59 the previous day. Creation dates never determine sales inclusion. 105/106/107 are cancelled/rejected/failed, not sales. 108 is open.

| Hub | Count | S | D | F-Q | T | Refund owed separately | Net sales |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 90000 | 10000 | 10000 | 90000 | 10000 | 90000 |
| 2 (archived) | 1 | 60000 | 0 | 10000 | 70000 | 0 | 70000 |
| All | 2 | 150000 | 10000 | 20000 | 160000 | 10000 | 160000 |

101: original C=100000; reduced S=90000, D=10000, F=15000, Q=5000 gives T=90000. C-T=10000 owed; subtracting it again would incorrectly report 80000. Its two lines must not duplicate header totals. 102: S=30000*2=60000, T=70000; archiving changes neither sales nor lines.

Top items aggregate by immutable menu item ID, never name. ID 1: quantity 1+2=3; revenue 40000+30000*2=100000; deterministic display uses latest eligible finished delivery/order/line snapshot, `Renamed snapshot`. ID 2: quantity 1; revenue 50000; `Shared name`. IDs 1/2 share a name in 101 and stay separate; ID 1 changes snapshot name in 102 and stays one identity. Sorted revenue descending then item ID ascending.

Deliveries included: 101,102,107. Waits READY→pickup: 10,20,30 minutes; n=3, mean=60/3=20. Successful rides: 20,30; n=2, mean=50/2=25. Failed ride 10 minutes is excluded from the ride mean. Failure=1/(2+1)=33.3%. Hub1: delivered1/failed0, wait10/ride20/failure0%; Hub2: delivered1/failed1, wait25/ride30/failure50%. One shipper (3) has the same overall totals.

Workload is NOW without date/hub filters: both retained hubs 1 and 2 appear. Hub1 has zero open orders; hub2 has one PLACED order (108), active cooking load1. Neither archived hub identity nor historical order dates may remove it. No archived operational order contributes.

Empty day 1 January 2026: no sales, all monetary totals zero; no deliveries, wait/ride/failure ratios n/a with zero samples. Filter hub2 preserves its archived identity; sales total70000. Exact half-open endpoints must include start and exclude end when timestamps are moved to the interval edges in a separate test.
