# P4 validation and uniqueness reconciliation (P2-S17)

Author: 722I0004 · AI-assisted (Codex).

Retained archived identities stay in uniqueness scope: username; hub code (and conservative hub-name comparison); Brand name; MenuItem name within its existing Brand; Voucher code. Unlisting removes only the hub/item association. Neither archived-name reuse, account-role reassignment, Customer subtype changes, reparenting nor restore is promised. Phone, email and passport are required/validated by customer subtype; the frozen contract does not grant them new globally unique identity semantics, so no such uniqueness was invented.

Existing input bounds remain implementation validation choices, not newly client-approved business rules: username 3–30 small letters/digits/dot/underscore; password 6–72; customer full name 2–80; Local mobile `^0[35789][0-9]{8}$`; Tourist passport 6–12 uppercase letters/digits, nationality 2–40, email at most120, optional phone 7–15 digits with optional leading plus; address label 1–30, text 5–200 and selected district. The Hotel label is accepted. Staff display name 2–60; Kitchen staff require an active assigned hub.

Hub code `HUB-` plus2–8 alphanumeric characters, name at most80, address at most200, capacity1–500, base fee0–100000, finite latitude10.3–11.2 and longitude106.3–107.1 are preserved draft implementation bounds. Capacity ≥1 is the locked business minimum; the maxima and HCMC rectangle are conservative draft validation assumptions, not geographical precision or lecturer approval. District-centroid Haversine is explicitly approximate, with raw radius8km and started-km fee decisions kept separate.

Catalogue uses required names, positive whole-VND prices and current-parent Brand context. Voucher code3–20 capital alphanumeric characters, description≤120, FIXED positive or PERCENT1–100, nonnegative minimum, positive optional cap, and ordered inclusive Vietnam dates are validated. Date-window/monetary eligibility is checked on demand; there is no scheduled expiration transition.

Behavioral evidence: the final full-suite receipt and `p4_test_coverage.csv` bind the invalid-field, retained-name, immutable-role/type, archived-parent, payment-choice and date-edge cases to real nodes. This reconciliation preserves bounds rather than silently widening them. A differing owner/client answer affecting these assumptions requires impact assessment and the established31October checkpoint; no unanswered question is marked approved.
