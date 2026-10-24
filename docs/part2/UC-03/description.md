# UC-03 — Maintain hubs and kitchen capacity (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

**Use case name**

UC-03 — Maintain hubs and kitchen capacity.

**Scenario / trigger**

An Admin inspects hubs or submits a create, update or archive request to maintain the available kitchens and their capacity. The main success scenario creates a hub; alternatives cover read, update and archive.

**Actors**

Primary: Admin. The authenticated session supplies identity and role; posted actor identifiers are not trusted.

**Related use cases**

UC-01 consumes active hubs and capacity; UC-04 reads retained hub history and workload. SUC-08 maintains accounts attached to hubs independently. These are supporting dependencies, not include/extend relationships: Figure 2.1C gives UC-03 no such relation. SUC-01 login is a precondition.

**Stakeholders and interests**

Admin needs accurate hub records and controlled refusals; customers need valid hub choices; kitchen staff need truthful capacity; managers need retained reporting history.

**Pre-conditions**

An active Admin session is required for every request. An update or archive identifies an existing ACTIVE hub; reads may inspect archived records. Required data is available for validation; no capacity reservation is created by this use case.

**Post-conditions**

The selected command produces its applicable success guarantee. Read-only inspection writes zero persistent rows. Minimum guarantees apply to failures and also preserve unrelated records.

- **UC03-PC01**: hub created/updated with valid code, coordinates, fee, capacity
- **UC03-PC02**: archived hub hidden from browse/checkout, visible in history/reports
- **UC03-MG01**: duplicate code / capacity < 1 / archive with open order → nothing changed

Additional refusal detail: invalid coordinates, negative fee, missing/stale records, authorization failure or failed persistence leave all records unchanged under UC03-MG01. A successful create starts ACTIVE. Capacity is an integer at least 1, even when lower than current cooking load. Busy/quiet are derived from load, not stored lifecycle states. Archive retains the hub and historical references.

**Flow of activities**

| Actor | System |
|---|---|
| 1. Request `listHubs(includeArchived?)`. |  |
|  | 2. Recheck active Admin before disclosure; deny without data if inactive/unauthorized. Otherwise return `hubRecordsAndLoad`, including capacity and derived load/busy context. No write occurs. |
| 3. Submit `createHub(code, name, address, latitude, longitude, baseDeliveryFee, capacity)`. |  |
|  | 4. Check active Admin context, nonempty required fields, unique hub code, valid finite latitude/longitude, nonnegative whole-VND base fee and integer capacity ≥ 1. Recheck guards at the change boundary. |
|  | 5. Save one ACTIVE hub and return `savedRecord`; UC03-PC01 holds. Existing orders are unchanged. |
| 6. Read the saved result and finish. | Show the saved record and capacity/load context. |

- **A01 — Inspect (branch at 3; end at 6):** Admin submits `getHub(hubId)`; System returns `hubAndArchiveGuard` (record, current load/capacity and whether open orders prevent archive). Admin may finish without a mutation. `listHubs` and `getHub` never write; a further chosen command starts A02/A03 or main step 3.
- **A02 — Update (branch at 3; rejoin 6):** Admin first uses A01 and submits `updateHub(hubId, code, name, address, latitude, longitude, baseDeliveryFee, capacity)`. System rechecks active record and step 4 validation, excluding this same hub from duplicate-code comparison; saves attributes and returns `savedRecord` under UC03-PC01. Capacity may be lowered below current load: the ACTIVE hub is then busy and checkout refuses until load falls. This does not cancel or reprice existing orders.
- **A03 — Archive (branch at 3; rejoin 6):** Admin first uses A01 and submits `archiveHub(hubId)`. System rechecks active Admin and ACTIVE hub, and counts open orders: every state except DELIVERED, DELIVERY_FAILED, REJECTED and CANCELLED is open (READY and OUT_FOR_DELIVERY still block archive). If none exist, set ARCHIVED, return `savedRecord`, hide the hub from browse/checkout, retain it in history/reports: UC03-PC02. No restore command is defined.
- **A04 — More inspection (branch at 6; rejoin 1):** Admin may start another independent request; each request rechecks session and guards. There is no automatic background update.

**Exception conditions**

- **E01 — Invalid create/update (branch at 4 or A02 validation; end):** duplicate code, capacity < 1 or malformed coordinates/fee/required data returns `controlledRefusal` with a reason; UC03-MG01, nothing changed. A correction is a new request at 3/A02, not a partially saved record.
- **E02 — Unsafe archive (branch at A03 guard; end):** any open order returns `controlledRefusal`; UC03-MG01, nothing changed. Lowering capacity itself is not this failure.
- **E03 — Missing/stale target or denied context (branch at any request; end); archived target for update/archive only:** return `refusal` for `getHub`, or `controlledRefusal` for a mutation; no data disclosure to a denied actor and UC03-MG01, nothing changed. Authorized inspection of a retained archived hub remains valid; archive status alone does not refuse listHubs/getHub. No update revives an archived hub.
- **E04 — Persistence failure (branch at 5/A02/A03 save; end):** return a controlled failure after rollback; UC03-MG01, nothing changed. No partial hub change is claimed.
