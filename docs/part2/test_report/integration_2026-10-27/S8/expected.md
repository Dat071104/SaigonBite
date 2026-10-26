# S8 CSRF: every form carries a token; a form without or with a changed token is refused and changes nothing

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Written before the run. Runs on the main database after S7 (port 5100).

| Step | Profile | Action | Expected | Rules |
|---|---|---|---|---|
| 8.1 | all roles | open the main pages of each role and count `<form method=post>` elements | every post form has a hidden `csrf_token` field with a non-empty value: 0 forms without one (customer: hubs, menu, quote, order, my orders; kitchen: board, order, availability; shipper: board, detail; admin: hubs, hub form, catalogue, hub menu, archive; manager: report pages have only GET filter forms) | plan §2.4 |
| 8.2 | admin | Edit BT: set capacity 7 and delete the csrf_token field from the form (script), Save hub | HTTP 400, page "Form expired" with the message "This form has expired or did not come from SaigonBite. Go back, reload the page and try again."; the hub list still shows "1 / 8" for BT | CSRF |
| 8.3 | admin | the same with csrf_token changed to another value | HTTP 400 "Form expired"; BT still "1 / 8" | CSRF |
| 8.4 | kitchen | Availability: delete csrf_token from the "Mark sold out" form of Pho bo tai, press it | HTTP 400 "Form expired"; Pho bo tai still Available | CSRF |
| 8.5 | customer | Order 9: delete csrf_token from "Cancel this order", accept the confirmation | HTTP 400 "Form expired"; order 9 still PLACED | CSRF |

Corroboration (read-only): BT capacity 8; item 1 available at hub 1; order 9 PLACED.
