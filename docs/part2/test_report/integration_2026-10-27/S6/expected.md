# S6 Declined payment, rejected paid order, cancellation, failed delivery

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Written before the run. Money is hand-computed.

Start state (after S5): orders 1 to 11 exist; D1 load 2 (orders 8, 9; capacity 14, quiet: 2 < 3.5). Customer Mai, Home (fee 15,000, quiet discount 5,000). Demo order 7 is READY at D1 (COD 65,000 VND, no shipper).

| Step | Profile | Action | Expected | Rules |
|---|---|---|---|---|
| 6a.1 | customer | order 1 × Tra da at D1, choose "Pay now online: E-wallet", "Confirm order" | the next screen is the "Payment simulator" with "Amount: 20,000 VND" (10,000 + 15,000 - 5,000) and "Method: E-wallet"; no notice "The price changed since your quote" | BR-10, BR-14 |
| 6a.2 | customer | "Decline payment" | the quote page again, HTTP 402, banner "The payment was declined. No order was placed. Try again or choose cash on delivery." | BR-14, MG01 |
| 6a.3 | (database) | count orders and payments | unchanged: 11 orders and 11 payment rows; no order 12 and no payment row for this attempt | MG01 |
| 6b.1 | customer | order 1 × Pho bo tai at D1, online E-wallet, "Confirm order", "Approve payment" | "Order 12 is placed", 65,000 VND (55,000 + 15,000 - 5,000), payment ONLINE PAID ("You paid online") | BR-14 |
| 6b.2 | kitchen | Order 12: reason "The beef has run out for today.", "Reject order" | banner "Order 12 is rejected and the customer is told why." | BR-16, BR-17 |
| 6b.3 | customer | open Order 12 and its receipt | Order page: status Rejected with the reason; the payment line says refund pending and names 65,000 VND as a refund owed (payout pending), not as refunded. Receipt: "Payment amount captured C" 65,000 VND, Payment state REFUND_PENDING, "Refund owed, payout pending" 65,000 VND. The state never reads Refunded | BR-13, BR-17 |
| 6c.1 | customer | order 1 × Tra da at D1, cash on delivery | "Order 13 is placed", 20,000 VND | BR-03, BR-07 |
| 6c.2 | customer | Order 13, "Cancel this order", accept the confirmation "Cancel order 13?" | banner "Order 13 is cancelled."; status Cancelled; payment "COD, voided" | BR-15, BR-17 |
| 6c.3 | kitchen | open the Kitchen board | no card for Order 13 | BR-26 |
| 6d.1 | shipper | Deliveries: "Pick up this order" on Order 7 | banner "You picked up order 7."; badge Picked up | BR-25 |
| 6d.2 | shipper | reason "Customer did not answer the phone.", "Report failed delivery", accept the confirmation | banner "The failed delivery of order 7 is recorded. Bring the food back to the hub."; badge Failed; Problem "Customer did not answer the phone." | BR-17, BR-25 |
| 6d.3 | customer | open Order 7 | status Delivery failed; "Delivery problem" shows the reason; payment "COD, voided" | BR-17 |

Corroboration (read-only): order 12 REJECTED, payment REFUND_PENDING amount 65,000 refund_amount 65,000; order 13 CANCELLED, payment VOIDED; order 7 DELIVERY_FAILED, delivery FAILED with the reason, payment VOIDED. After S6: 13 orders.
