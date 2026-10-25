# UC-01 CRC cards

Author: 722I0004 · AI-assisted (Codex)

Collaborators below resolve real AST constructor/function calls or typed collaborators from the shared model. A † operation is a root-annotated target; it is not a claim of code behavior. DAO collaborators appear here and in the DCD; Section III sequences intentionally defer persistence to 4.3.2.

## PlaceOrderController

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PlaceOrderController | Knows customers, hubs, orders, payments, vouchers, gateway. Does list_hubs, select_hub, request_quote†, confirm_order†, _build_quote, suggest_hubs†, _require_customer, _check_payment_choice. Coordinate authorization, domain decisions and data access. | AuthorizationError, CustomerDAO, Hub, HubDAO, HubMenuView, HubStatus, HubUnavailableError, Order, OrderDAO, OrderLine, Payment, PaymentChoice, PaymentDAO, PaymentDeclinedError, Quote, QuoteChangedError, ValidationError, VoucherDAO, order |

## order

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| order | Knows selected inputs. Does choose_hub, choose_items, quote†, confirm†, detail, my_orders, cancel. Translate authenticated customer routes and render quote, receipt and order results. | ValidationError |

## HubStatus

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| HubStatus | Knows hub, load. Does busy, quiet. Derive busy, quiet and load percentage from current load and capacity. | HubMenuView, PlaceOrderController |

## HubDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| HubDAO | Knows conn. Does active_loads, list_active, active_load, get, list_menu, get_available_item, get_including_archived. Read or write parameterized records. | Hub, HubMenuItem, MenuItem, OrderTrackingController, PlaceOrderController |

## CustomerDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| CustomerDAO | Knows conn. Does get_by_user_id, list_addresses, get_address. Read or write parameterized records. | Address, OrderTrackingController, PlaceOrderController |

## UserDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| UserDAO | Knows conn. Does get_by_id. Read or write parameterized records. | No outward application call; supplied/read by its typed owner. |

## Hub

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Hub | Knows id, code, name, address_text, latitude, longitude, max_active_orders, base_delivery_fee, archived_at. Does distance_to†. Represent a kitchen location, capacity and fee. | HubDAO, HubMenuView, HubStatus, OrderConfirmation, OrderDetail, PlaceOrderController, Quote |

## Quote

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Quote | Knows hub, address, lines, distance_km, delivery_fee, quiet_discount, voucher, voucher_discount. Does fingerprint†, total. Compute and bind the complete consented price; not persisted. | Order, PlaceOrderController |

Target collaborators for `fingerprint†`: **PaymentMethod** and **OnlineOption** (pure-domain enum values). The controller adapts PaymentChoice before the call; Quote has no controller-layer collaborator.

## Voucher

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Voucher | Knows id, code, description, discount_type, discount_value, min_subtotal, max_discount, valid_from, valid_until, archived_at. Does discount_for, problem. Check date/subtotal eligibility and calculate the bounded discount. | PlaceOrderController, Quote, VoucherDAO |

## VoucherDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| VoucherDAO | Knows conn. Does get_by_code. Read or write parameterized records. | PlaceOrderController |

## Order

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Order | Knows customer_id, hub_id, address_id, state, delivery_fee, idempotency_token, placed_at, lines, id, archived_at, delivery_address_text, distance_km, voucher_id, voucher_discount, quiet_discount, reject_reason, confirmed_at, ready_at, closed_at. Does place, move_to, replace_line, line. Own the order lifecycle, snapshots and accepted replacement totals. | InvalidTransition, OrderConfirmation, OrderDAO, OrderDetail, OrderLine, OrderSummary, OrderTrackingController, PlaceOrderController, controllers.common |

## PaymentGatewaySimulator

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentGatewaySimulator | Knows selected inputs. Does authorise, release. Read or write parameterized records. | Authorisation, PlaceOrderController |

## OrderDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderDAO | Knows conn. Does _load, get_by_id, get_by_token, insert, list_for_customer, change_state. Read or write parameterized records. | Order, OrderLine, OrderState, OrderTrackingController, PlaceOrderController, controllers.common |

## PaymentDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentDAO | Knows conn. Does get_by_order_id, insert, change_state, set_amounts†. Read or write parameterized records. | OnlineOption, OrderTrackingController, Payment, PaymentMethod, PaymentState, PlaceOrderController, controllers.common |

## OrderTrackingController

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderTrackingController | Knows customers, orders, payments, hubs, deliveries, offers. Does get_order, list_my_orders, cancel_order†, _own_order, _require_customer. Coordinate authorization, domain decisions and data access. | AuthorizationError, CustomerDAO, HubDAO, NotFoundError, OrderDAO, OrderSummary, ReplacementOfferDAO, controllers.common, order |

## DeliveryDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| DeliveryDAO | Knows conn. Does get_by_order_id. Read or write parameterized records. | OrderTrackingController |

## ReplacementOfferDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| ReplacementOfferDAO | Knows conn. Does get_open, list_for_order, decide. Read or write parameterized records. | OrderTrackingController |

## Payment

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Payment | Knows order_id, method, state, amount, created_at, updated_at, online_option, provider_ref, refund_amount, id. Does release_for_unfulfilled_order†. Hold captured amount C and refund obligations without claiming payout. | OrderConfirmation, OrderDetail, PaymentDAO, PlaceOrderController, controllers.common |

## controllers.common

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| controllers.common | Knows selected inputs. Does move_order, release_payment†. Module functions with their original Python signatures. | ConflictError, Order, OrderDAO, OrderTrackingController, Payment, PaymentDAO |

## ReplacementOffer

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| ReplacementOffer | Knows order_id, order_line_id, original_item_name, original_unit_price, new_menu_item_id, new_item_name, new_unit_price, state, offered_at, decided_at, id. Does move_to. Hold one proposed whole-line replacement and its decision history. | OrderDetail, ReplacementOfferDAO |

## OrderLine

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderLine | Knows menu_item_id, item_name, unit_price, quantity, id. Does typed value / enumeration initialization and attribute access. Retain item/name/price/quantity snapshots and derive the line total. | Order, OrderDAO, PlaceOrderController, Quote |

## Customer

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Customer | Knows id, user_id, full_name, phone, email, passport_no, nationality, customer_type. Does typed value / enumeration initialization and attribute access. Represent customer identity and permitted online payment choices. | CustomerDAO, OrderTrackingController, PlaceOrderController |

## LocalCustomer

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| LocalCustomer | Knows customer_type. Does typed value / enumeration initialization and attribute access. Specialize the Customer type and permitted payment options for a local customer. | No outward application call; supplied/read by its typed owner. |

## TouristCustomer

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| TouristCustomer | Knows customer_type. Does typed value / enumeration initialization and attribute access. Specialize Customer identity and permitted payment options for a tourist. | No outward application call; supplied/read by its typed owner. |

## Address

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Address | Knows id, customer_id, label, full_address, district, latitude, longitude, archived_at. Does typed value / enumeration initialization and attribute access. Hold an owned delivery location and archive flag. | CustomerDAO, Hub, HubMenuView, PlaceOrderController, Quote |

## MenuItem

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| MenuItem | Knows id, brand_id, brand_name, name, description, price, archived_at. Does typed value / enumeration initialization and attribute access. Hold current catalogue text, whole-VND price and archive flag. | HubDAO, HubMenuItem |

## Brand

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Brand | Knows id, name, archived_at. Does typed value / enumeration initialization and attribute access. Group menu items and retain the archived brand identity. | No outward application call; supplied/read by its typed owner. |

## HubMenuItem

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| HubMenuItem | Knows hub_id, item, is_available. Does typed value / enumeration initialization and attribute access. Represent one hub listing and its independent availability. | HubDAO, HubMenuView |

## UserAccount

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| UserAccount | Knows id, username, password_hash, display_name, role, is_active, hub_id, created_at. Does typed value / enumeration initialization and attribute access. Hold account identity, role, active flag and optional kitchen-hub assignment. | UserDAO |

## OrderState

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderState | Knows PLACED, CONFIRMED, REJECTED, PREPARING, READY, OUT_FOR_DELIVERY, DELIVERED, DELIVERY_FAILED, CANCELLED. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Order, OrderDAO, controllers.common |

## PaymentState

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentState | Knows PENDING, PAID, FAILED, VOIDED, REFUND_PENDING, REFUNDED. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Payment, PaymentDAO |

## PaymentMethod

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentMethod | Knows COD, ONLINE. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Payment, PaymentChoice, PaymentDAO, Quote, order |

## OnlineOption

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OnlineOption | Knows E_WALLET, BANK_QR, INTERNATIONAL_CARD. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Customer, Payment, PaymentChoice, PaymentDAO, PaymentGatewaySimulator, PlaceOrderController, Quote, order |

## OfferState

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OfferState | Knows OFFERED, ACCEPTED, DECLINED, WITHDRAWN. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | ReplacementOffer, ReplacementOfferDAO |

## Role

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Role | Knows CUSTOMER, KITCHEN_STAFF, SHIPPER, ADMIN, MANAGER. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | UserAccount |

## PaymentChoice

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentChoice | Knows method, option, outcome. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | PlaceOrderController, order |

## OrderConfirmation

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderConfirmation | Knows order, payment, hub, created. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | PlaceOrderController |

## HubMenuView

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| HubMenuView | Knows hub, status, menu, addresses. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | PlaceOrderController |

## OrderDetail

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderDetail | Knows order, payment, hub, delivery, open_offer, offers. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | OrderTrackingController |

## OrderSummary

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderSummary | Knows order, hub_name, awaiting_answer. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | OrderTrackingController |

## Authorisation

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Authorisation | Knows approved, reference, message. Does typed value / enumeration initialization and attribute access. Carry the local simulator decision, reference and message; not persisted. | PaymentGatewaySimulator |

## domain.rules

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| domain.rules | Knows selected inputs. Does delivery_fee, quiet_discount. Module functions with their original Python signatures. | PlaceOrderController, domain.rules |

## DiscountType

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| DiscountType | Knows FIXED, PERCENT. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Voucher |

## CustomerType

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| CustomerType | Knows LOCAL, TOURIST. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Customer, LocalCustomer, TouristCustomer |
