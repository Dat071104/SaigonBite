# UC-04 — Produce management reports: sales, workload, delivery performance (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

## Use case name

UC-04 — Produce management reports: sales, workload, delivery performance.

## Scenario / trigger

A manager asks for operational sales for Vietnam calendar dates, the current hub workload, or delivery performance. Reports read shared records; no Report entity or lifecycle is created. Main flow is sales; A01/A02 cover the other report requests.

## Actors

Primary: Manager with an authenticated ACTIVE MANAGER account. Other roles, including Admin, are denied these operations. No database, clock, controller or report object is an actor.

## Related use cases

Figure 2.1C associates Manager with UC-04 and has no UC-04 include/extend relation. UC-01/02/05 and SUC-05 supply Order, Payment and Delivery facts; UC-03 supplies hubs; SUC-09 preserves archived history for reporting; SUC-01 supplies authentication. These are serving/data references only.

## Stakeholders and interests

Manager needs comparable definitions, visible filters, sample sizes and honest empty outcomes. Client needs workload for staffing and delivery trends. Customers and management need retained archived history and refunds owed reported separately without double subtraction. Data owners need a read-only operation with no accidental archive or lifecycle changes.

## Pre-conditions

Each report request rechecks the session's active MANAGER role. Order/OrderLine, Payment, Delivery and Hub facts follow their owning contracts; an empty data set is valid. Sales/performance requests require valid `startDateVN`, `endDateVN`, start≤end and, if supplied, an existing `hubId` (archived hubs are permitted historical filters). The workload request takes no dates or hub parameter; it is the current per-hub snapshot labelled “now.” Defaults are team assumptions pending Q5, never recorded as client approval.

## Post-conditions

Verbatim register text:

| ID | Guarantee |
|---|---|
| UC04-PC01 | sales, workload, performance equal the hand oracle for the filter |
| UC04-PC02 | n/a on empty denominators |
| UC04-MG01 | 0 rows written by any report request |
| UC04-MG02 | non-manager denied |

PC01 states required expected behaviour, not an executed test result. Every accepted report labels its definitions, period or “now”, hub scope and sample counts. Every refusal/empty outcome preserves MG01. Nothing saves a Report, updates a timestamp on a domain row, changes an archive flag, or mutates lifecycle/payment facts.

## Flow of activities

| Actor | System |
|---|---|
| 1. Choose sales and enter Vietnam calendar dates and optional hub. | Explain that sales are operational, not accounting; dates use Asia/Ho_Chi_Minh and include both selected days. |
| 2. Send `salesReport(startDateVN, endDateVN, hubId?)`. | Recheck active Manager, date validity/order and hub existence. Convert `[start 00:00 VN, end+1 00:00 VN)` to UTC against stored UTC timestamps (BR-20). |
| 3. Await report. | Select DELIVERED orders by Delivery finish time in that half-open interval and optional hub. Include archived records (BR-21/24). Sum order count, S, D, F−Q, T and refunds owed at order grain, without an OrderLine join; show refunds owed separately, never subtract them again from T. Item detail groups by menu_item_id and displays snapshot names, keeping equal-name distinct items separate. |
| 4. Inspect `operationalSalesAndRefundsOwed`. | Return filter labels, operational totals, item detail and order sample count, without persistent writes (UC04-PC01/MG01). |
| 5. Choose to finish or request another report. | End, or repeat from step 1 / A01 / A02; each request independently rechecks authorization. |

| ID | Branch step | Actor and system behaviour | Rejoin / end |
|---|---|---|---|
| A01 | 1, choose workload | Manager sends `workloadReport()`. System rechecks active Manager and reads the current snapshot per hub, retaining archived hub identities for reporting (BR-18 / UC03-PC02): cooking load=PLACED+CONFIRMED+PREPARING (including PLACED awaiting an offer), capacity, READY count and OUT_FOR_DELIVERY count. Label “now” with as-of time; no date or hub filter is applied (BR-01/22). Return `currentHubLoadCapacityReadyOutForDelivery`; historical archive flags do not remove relevant retained facts. An archived hub has zero open cooking/READY/OUT_FOR_DELIVERY work under BR-18; identify its archived status rather than hiding it from reports. | Rejoin 5; UC04-PC01/MG01. |
| A02 | 1, choose delivery performance | Manager sends `deliveryReport(startDateVN, endDateVN, hubId?)`. System rechecks role/filter as step 2 and reads Delivery DELIVERED or FAILED with finished_at in the UTC interval, including archived orders. Wait samples are READY→PICKED_UP for finished deliveries with both timestamps; ride samples are PICKED_UP→DELIVERED for successes only. Show mean wait and its N, mean ride and its N, and failed/(delivered+failed) with finished N. Missing timestamp pairs contribute no duration sample; expose the corresponding N. Return `waitRideFailureRatesWithNAndNA`. | Rejoin 5; UC04-PC01/MG01; PC02 where a denominator is zero. |
| A03 | 3/A01/A02, no matching rows or no valid metric samples | Return a labelled empty/zero-count report. Counts and sums are zero; a mean or failure-rate denominator of zero is shown as “n/a” with N=0, never 0% or a fabricated duration (BR-23). | Rejoin 5; UC04-PC02/MG01. |

Calculation definitions are part of the required response. Order totals remain T=S−D+F−Q. Refunds owed is a separate column of obligations for the selected delivered orders, not a second reduction of operational sales; this report does not pretend to be a global refund ledger. Workload has no historic period and does not reinterpret archived history as new work. The hand oracle must independently apply the same filter, grain and formulas in later verification; none is measured here.

## Exception conditions

| ID | Branch step | Condition / response | Rejoin / guaranteed end |
|---|---|---|---|
| E01 | 2/A01/A02 | Missing/inactive/non-MANAGER session: return `denied` with no report disclosure. | End; UC04-MG02 and UC04-MG01. |
| E02 | 2/A02 | Malformed/reversed date range or unknown hub: return `invalidFilter`; do not silently coerce a different period or hub. | End; UC04-MG01; corrected request starts at 1/A02. |
| E03 | 3/A01/A02 | Read unavailable or incomplete: report unavailable, do not fabricate successful totals. | End; UC04-MG01. A later retry is a new request. |
