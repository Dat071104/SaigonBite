# History of S3/expected.md

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5).

1. 27/10/2026 01:13 the file was written and hashed (SHA-256 prefix `4c16fcd9d6be8cdf`). Step 3.6 said the order page shows the section "Offer a replacement".
2. 27/10/2026 about 01:20, before any scenario had run, I changed step 3.6 to say the section is absent, from a misreading of `kitchen/order.html` (I took the flash "A replacement requires a currently unavailable source dish." seen in a capture for a rule about showing the section).
3. 27/10/2026, during the first complete runs (t1, t2), the actual page showed the section (`KitchenController.get_order` builds `candidates` for every line of a PLACED order; the rule about a sold-out source dish is checked when the offer is sent, step 4.2). My change in item 2 was wrong, not the first expectation.
4. The file was restored to the exact original bytes. Its SHA-256 is again `4c16fcd9d6be8cdf…`, which shows that the restored text is the first, unchanged expectation. No expected value was adjusted to fit an actual result.

S7/expected.md: the zero-voucher cell was changed from "-0 VND" to "0 VND" before any run, because the template was corrected in commit dc87741 (a zero discount has no minus sign). That correction is recorded in the file itself.
