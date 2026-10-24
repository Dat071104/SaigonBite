# UC-06 — Maintain brands, menu items and hub listings (author: 722I0004)

Author: 722I0004 · AI-assisted (Codex)

**Use case name**

UC-06 — Maintain brands, menu items and hub listings.

**Scenario / trigger**

An Admin inspects the catalogue and chooses a brand, menu-item or hub-listing maintenance command. The main scenario creates a brand. Alternative requests maintain items and listings independently.

**Actors**

Primary: Admin, authenticated by active session. Kitchen staff perform their own-hub availability goal through SUC-06; they are not granted Admin catalogue rights here.

**Related use cases**

UC-01 reads orderable catalogue entries; UC-05 reads availability for replacement. SUC-06 independently sets availability at the staff member's own hub. Figure 2.1C associates Admin with UC-06 and Figure 2.1B associates Kitchen staff with SUC-06; no include/extend is claimed between them. SUC-01 login is a precondition.

**Stakeholders and interests**

Admin needs valid catalogue records; kitchens need availability specific to their hub; customers need only eligible items; customers and managers need old order names/prices retained.

**Pre-conditions**

Every Admin request requires an active Admin session. Maintenance identifies existing records where required. Creation/listing requires active parent records; a listing is uniquely identified by its hub–item pair. An archived item or brand cannot be newly listed or ordered, regardless of a retained listing availability flag.

**Post-conditions**

The selected successful request satisfies the applicable guarantee; all inspections write zero persistent rows. Minimum guarantees preserve historical snapshots on both successful changes and refusals.

- **UC06-PC01**: brand/item created, updated, archived
- **UC06-PC02**: listing added/removed, availability per hub
- **UC06-PC03**: archived/sold-out items not orderable
- **UC06-MG01**: old order lines unchanged after price change/archive
- **UC06-MG02**: duplicates/invalid prices refused

Brand/MenuItem start ACTIVE and archive to ARCHIVED, with no undo-archive operation. Availability is AVAILABLE or SOLD_OUT on HubMenuItem, never a global MenuItem status. Unlist physically removes only that association; a later valid list is a new association lifecycle. Existing OrderLine names, prices and quantities are never rewritten by this use case.

**Flow of activities**

| Actor | System |
|---|---|
| 1. Request `listCatalogue(hubId?)` (omit hubId for the full catalogue, supply it for a hub view). |  |
|  | 2. Recheck active Admin before disclosure; deny without data if inactive/unauthorized. Otherwise return `brandsItemsHubsAndListings`; show active/archive status and listing availability per hub. This is also the read path for Brand, MenuItem and HubMenuItem. No write occurs. |
| 3. Submit `createBrand(name)`. |  |
|  | 4. Check active Admin, valid required name and unique Brand name. Recheck guards at the change boundary. |
|  | 5. Save one ACTIVE brand; return `savedRecord` under UC06-PC01. Preserve old order lines (UC06-MG01). |
| 6. Inspect the result and finish. | Show the saved record or the applicable listing result. |

- **A01 — Read only (branch at 3; end at 6):** inspect the response from step 2, optionally repeat `listCatalogue(hubId?)` with another hub filter, then finish. No separate get-item/get-brand query is invented.
- **A02 — Update brand (branch at 3; rejoin 6):** submit `updateBrand(brandId, name)` after step 2 inspection. System checks active target and valid unique Brand name excluding itself; save current name and return `savedRecord`. UC06-PC01; UC06-MG01 preserves snapshots.
- **A03 — Archive brand (branch at 3; rejoin 6):** submit `archiveBrand(brandId)`. System checks active target and Admin, saves ARCHIVED and returns `savedRecord`. Descendant items become ineligible for operational menus/new listing/ordering even if their own archive or availability flag was not changed. UC06-PC01/PC03; UC06-MG01.
- **A04 — Create item (branch at 3; rejoin 6):** submit `createMenuItem(brandId, name, description, price)`. System validates active Brand, valid fields, whole-VND price > 0 and unique item name within that Brand; creates ACTIVE item and returns `savedRecord`. UC06-PC01; UC06-MG01. Nothing is listed automatically.
- **A05 — Update item (branch at 3; rejoin 6):** submit `updateMenuItem(itemId, brandId, name, description, price)`. System validates ACTIVE item and active parent, fields, price > 0 and uniqueness in that parent excluding itself; saves current catalogue attributes and returns `savedRecord`. UC06-PC01; UC06-MG01. The brandId parameter identifies the current parent; this flow does not promise reparenting. Existing OrderLine snapshot names/prices remain unchanged even after a price change.
- **A06 — Archive item (branch at 3; rejoin 6):** submit `archiveMenuItem(itemId)`; System checks ACTIVE target/Admin, saves ARCHIVED and returns `savedRecord`. Item cannot be listed or ordered, while old order lines remain unchanged: UC06-PC01/PC03 and UC06-MG01.
- **A07 — List at hub (branch at 3; rejoin 6):** inspect `listCatalogue(hubId)` then submit `listItemAtHub(hubId, itemId, available)`. System checks active Hub, Brand and MenuItem, boolean availability, no existing hub–item association; inserts the pair as AVAILABLE when true, SOLD_OUT when false; return `savedRecord`. UC06-PC02; false makes this hub's item not orderable (UC06-PC03). No other hub changes.
- **A08 — Set availability (branch at 3; rejoin 6):** inspect `listCatalogue(hubId)` then submit `setListingAvailability(hubId, itemId, available)`. System checks the existing pair and boolean flag; writes only this pair's AVAILABLE/SOLD_OUT flag and returns `savedRecord`. UC06-PC02/PC03; old lines remain unchanged (UC06-MG01). AVAILABLE alone never overrides archived-parent exclusion. This is the Admin path; SUC-06 uses `setMenuAvailability` with the staff hub from session and is only referenced here.
- **A09 — Unlist (branch at 3; rejoin 6):** inspect `listCatalogue(hubId)` then submit `unlistItemAtHub(hubId, itemId)`. System checks the pair exists and Admin context; removes only HubMenuItem, returns `savedRecord` as the catalogue's acknowledgement of removal. UC06-PC02; UC06-MG01. Do not delete Brand, MenuItem or OrderLine.
- **A10 — Another request (branch at 6; rejoin 1):** Admin may start a further command. Each request rechecks context and current guards, so concurrent changes cannot be bypassed by an old read response.

**Exception conditions**

- **E01 — Duplicate/invalid fields (branch at 4/A02/A04/A05/A07 guard; end):** duplicate name or hub–item pair, invalid required field or price ≤ 0 returns `controlledRefusal`; UC06-MG02 and UC06-MG01, no records changed. Correcting data starts another request.
- **E02 — Ineligible/stale target (branch at A02–A09 guard; end):** missing record/pair, archived record for update/archive, or archived Hub/Brand/MenuItem for creation/listing returns `controlledRefusal`; no partial change and UC06-MG01. Archive/availability eligibility continues to enforce UC06-PC03; the system cannot make an archived item orderable through a flag. Invalid boolean availability is refused with the same no-change minimum guarantee.
- **E03 — Session/role denied (branch at any request; end):** deny without catalogue disclosure or write; UC06-MG01 and, for submitted mutations, UC06-MG02's refusal discipline. No staff-to-Admin privilege escalation.
- **E04 — Persistence failure (branch at any save/remove; end):** roll back the complete selected change, return a controlled failure, and preserve UC06-MG01; no half-saved Brand/MenuItem/listing is claimed.

Duplicate checks include retained archived names in their uniqueness scope; this conservative analysis promises neither archived-name reuse nor restore/reparenting. Draft-only maximum lengths, prices, capacity and HCMC coordinate bounds are not promoted into new locked business rules.
