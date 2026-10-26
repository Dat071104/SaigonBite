# SSD occurrence coverage check

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)

Source map: `Part2/notes/P4_B02/actual_route_controller_SSD_map.csv` (SHA-256 `7fcb455ee23df6eebd23663534a177dc5e5c3a54de88503a5552134f4cd22fed`), 41 rows, 41 distinct occurrences (the three `listCatalogue` occurrences M06-A01, M06-B01, M06-C01 are kept apart).

Screens in `screens.csv`: 47. Occurrences with at least one screen: 41 of 41.
Result: PASS

| UC | Op | Occurrence | Operation | Screens |
|---|---|---|---|---|
| UC-01 | OP-01 | 01S-M04 | confirmCheckout | UC-01-S05, UC-01-S06, UC-01-S07, UC-01-S08 |
| UC-01 | OP-07 | 01S-M07 | cancelOrder | UC-01-S09, UC-01-S12 |
| UC-01 | OP-13 | 01S-M01 | browseHubs | UC-01-S01 |
| UC-01 | OP-14 | 01S-M02 | selectHub | UC-01-S03 |
| UC-01 | OP-15 | 01S-M03 | requestQuote | UC-01-S02, UC-01-S04 |
| UC-01 | OP-16 | 01S-M05 | viewReceipt | UC-01-S09, UC-01-S10 |
| UC-01 | OP-17 | 01S-M06 | viewMyOrders | UC-01-S11 |
| UC-02 | OP-10 | M03 | takeDelivery | UC-02-S02, UC-02-S03, UC-02-S04 |
| UC-02 | OP-11 | M04 | confirmDelivered | UC-02-S03, UC-02-S05, UC-02-S06 |
| UC-02 | OP-12 | M05 | reportFailure | UC-02-S03, UC-02-S07 |
| UC-02 | OP-21 | M01 | viewReadyDeliveries | UC-02-S01 |
| UC-02 | OP-22 | M02 | viewDelivery | UC-02-S02 |
| UC-03 | OP-23 | M03-01 | listHubs | UC-03-S01 |
| UC-03 | OP-24 | M03-02 | getHub | UC-03-S02 |
| UC-03 | OP-34 | M03-03 | createHub | UC-03-S04, UC-03-S05 |
| UC-03 | OP-35 | M03-04 | updateHub | UC-03-S02, UC-03-S03, UC-03-S05 |
| UC-03 | OP-36 | M03-05 | archiveHub | UC-03-S06 |
| UC-04 | OP-26 | M01 | salesReport | UC-04-S01, UC-04-S04, UC-04-S05 |
| UC-04 | OP-27 | M02 | workloadReport | UC-04-S02 |
| UC-04 | OP-28 | M03 | deliveryReport | UC-04-S03, UC-04-S04 |
| UC-05 | OP-02 | 05S-M03 | confirmOrder | UC-05-S02 |
| UC-05 | OP-03 | 05S-M04 | rejectOrder | UC-05-S02, UC-05-S04 |
| UC-05 | OP-04 | 05S-M05 | offerReplacement | UC-05-S02, UC-05-S03 |
| UC-05 | OP-05 | 05S-M08 | acceptReplacement | UC-05-S06, UC-05-S07, UC-05-S09 |
| UC-05 | OP-06 | 05S-M09 | declineReplacement | UC-05-S06, UC-05-S08 |
| UC-05 | OP-17 | 05S-M06 | viewMyOrders | UC-05-S05 |
| UC-05 | OP-18 | 05S-M07 | viewReplacement | UC-05-S06 |
| UC-05 | OP-19 | 05S-M01 | viewKitchenOrders | UC-05-S01 |
| UC-05 | OP-20 | 05S-M02 | viewKitchenOrder | UC-05-S02 |
| UC-06 | OP-25 | M06-A01 | listCatalogue | UC-06-S01 |
| UC-06 | OP-25 | M06-B01 | listCatalogue | UC-06-S01 |
| UC-06 | OP-25 | M06-C01 | listCatalogue | UC-06-S06 |
| UC-06 | OP-37 | M06-A02 | createBrand | UC-06-S01, UC-06-S02 |
| UC-06 | OP-38 | M06-A03 | updateBrand | UC-06-S01, UC-06-S02 |
| UC-06 | OP-39 | M06-A04 | archiveBrand | UC-06-S01, UC-06-S08 |
| UC-06 | OP-40 | M06-B02 | createMenuItem | UC-06-S03, UC-06-S05 |
| UC-06 | OP-41 | M06-B03 | updateMenuItem | UC-06-S04, UC-06-S05 |
| UC-06 | OP-42 | M06-B04 | archiveMenuItem | UC-06-S01, UC-06-S08 |
| UC-06 | OP-43 | M06-C02 | listItemAtHub | UC-06-S06, UC-06-S07 |
| UC-06 | OP-44 | M06-C03 | setListingAvailability | UC-06-S06, UC-06-S07 |
| UC-06 | OP-45 | M06-C04 | unlistItemAtHub | UC-06-S06, UC-06-S08 |
