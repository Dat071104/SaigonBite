# UC-05 CRC cards

Author: 722I0004 · AI-assisted (Codex)

Collaborators below resolve real AST constructor/function calls or typed collaborators from the shared model. A † operation is a root-annotated target; it is not a claim of code behavior. DAO collaborators appear here and in the DCD; Section III sequences intentionally defer persistence to 4.3.2.

## KitchenController

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| KitchenController | Knows hubs, menu, orders, payments, deliveries, offers. Does board, get_order, confirm_order†, reject_order†, offer_replacement†. Coordinate authorization, domain decisions and data access. | BoardEntry, ConflictError, HubDAO, KitchenBoard, KitchenOrderView, Order, OrderDAO, PaymentDAO, ReplacementOffer, ReplacementOfferDAO, ValidationError, controllers.common, kitchen |

## kitchen

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| kitchen | Knows selected inputs. Does board, order, confirm, reject, offer. Translate own-hub kitchen actions and render their results. | No outward application call; supplied/read by its typed owner. |

## HubDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| HubDAO | Knows conn. Does get_including_archived, list_menu, get_available_item. Read or write parameterized records. | Hub, HubMenuItem, KitchenController, MenuItem, OrderTrackingController |

## OrderDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderDAO | Knows conn. Does _load, list_for_hub, get_by_id, change_state, list_for_customer, save_lines_and_totals†. Read or write parameterized records. | KitchenController, Order, OrderLine, OrderState, OrderTrackingController, controllers.common |

## ReplacementOfferDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| ReplacementOfferDAO | Knows conn. Does get_open, list_for_order, decide, insert. Read or write parameterized records. | KitchenController, OrderTrackingController |

## UserDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| UserDAO | Knows conn. Does get_by_id. Read or write parameterized records. | No outward application call; supplied/read by its typed owner. |

## PaymentDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentDAO | Knows conn. Does get_by_order_id, change_state, set_amounts†. Read or write parameterized records. | KitchenController, OnlineOption, OrderTrackingController, Payment, PaymentMethod, PaymentState, controllers.common |

## Order

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Order | Knows customer_id, hub_id, address_id, state, delivery_fee, idempotency_token, placed_at, lines, id, archived_at, delivery_address_text, distance_km, voucher_id, voucher_discount, quiet_discount, reject_reason, confirmed_at, ready_at, closed_at. Does move_to, line, replace_line, total. Own the order lifecycle, snapshots and accepted replacement totals. | BoardEntry, InvalidTransition, KitchenController, KitchenOrderView, OrderDAO, OrderDetail, OrderSummary, OrderTrackingController, controllers.common |

## Payment

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Payment | Knows order_id, method, state, amount, created_at, updated_at, online_option, provider_ref, refund_amount, id. Does release_for_unfulfilled_order†. Hold captured amount C and refund obligations without claiming payout. | KitchenOrderView, OrderDetail, PaymentDAO, controllers.common |

## OrderTrackingController

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderTrackingController | Knows customers, orders, payments, hubs, deliveries, offers. Does list_my_orders, get_order, answer_replacement†, _own_order, _require_customer. Coordinate authorization, domain decisions and data access. | AuthorizationError, ConflictError, CustomerDAO, HubDAO, NotFoundError, Order, OrderDAO, OrderSummary, PaymentDAO, ReplacementOfferDAO, controllers.common, order |

## order

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| order | Knows selected inputs. Does my_orders, detail, answer_replacement. Translate authenticated customer routes and render quote, receipt and order results. | kitchen |

## CustomerDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| CustomerDAO | Knows conn. Does get_by_user_id. Read or write parameterized records. | OrderTrackingController |

## OrderDetail

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderDetail | Knows order, payment, hub, delivery, open_offer, offers. Does total_if_accepted. Coordinate authorization, domain decisions and data access. | Order, OrderTrackingController |

## DeliveryDAO

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| DeliveryDAO | Knows conn. Does get_by_order_id. Read or write parameterized records. | KitchenController, OrderTrackingController |

## controllers.common

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| controllers.common | Knows selected inputs. Does move_order, release_payment†. Module functions with their original Python signatures. | ConflictError, KitchenController, Order, OrderDAO, OrderTrackingController, Payment, PaymentDAO |

## ReplacementOffer

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| ReplacementOffer | Knows order_id, order_line_id, original_item_name, original_unit_price, new_menu_item_id, new_item_name, new_unit_price, state, offered_at, decided_at, id. Does move_to. Hold one proposed whole-line replacement and its decision history. | KitchenController, KitchenOrderView, OrderDetail, ReplacementOfferDAO |

## OrderLine

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderLine | Knows menu_item_id, item_name, unit_price, quantity, id. Does typed value / enumeration initialization and attribute access. Retain item/name/price/quantity snapshots and derive the line total. | Order, OrderDAO |

## Customer

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Customer | Knows id, user_id, full_name, phone, email, passport_no, nationality, customer_type. Does typed value / enumeration initialization and attribute access. Represent customer identity and permitted online payment choices. | CustomerDAO, OrderTrackingController |

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
| Address | Knows id, customer_id, label, full_address, district, latitude, longitude, archived_at. Does typed value / enumeration initialization and attribute access. Hold an owned delivery location and archive flag. | CustomerDAO, Hub |

## MenuItem

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| MenuItem | Knows id, brand_id, brand_name, name, description, price, archived_at. Does typed value / enumeration initialization and attribute access. Hold current catalogue text, whole-VND price and archive flag. | HubDAO, HubMenuItem, KitchenOrderView |

## Brand

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Brand | Knows id, name, archived_at. Does typed value / enumeration initialization and attribute access. Group menu items and retain the archived brand identity. | No outward application call; supplied/read by its typed owner. |

## HubMenuItem

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| HubMenuItem | Knows hub_id, item, is_available. Does typed value / enumeration initialization and attribute access. Represent one hub listing and its independent availability. | HubDAO, KitchenController |

## UserAccount

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| UserAccount | Knows id, username, password_hash, display_name, role, is_active, hub_id, created_at. Does typed value / enumeration initialization and attribute access. Hold account identity, role, active flag and optional kitchen-hub assignment. | KitchenController, UserDAO |

## OrderState

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderState | Knows PLACED, CONFIRMED, REJECTED, PREPARING, READY, OUT_FOR_DELIVERY, DELIVERED, DELIVERY_FAILED, CANCELLED. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | KitchenBoard, Order, OrderDAO, controllers.common |

## PaymentState

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentState | Knows PENDING, PAID, FAILED, VOIDED, REFUND_PENDING, REFUNDED. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Payment, PaymentDAO |

## PaymentMethod

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| PaymentMethod | Knows COD, ONLINE. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Payment, PaymentDAO, order |

## OnlineOption

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OnlineOption | Knows E_WALLET, BANK_QR, INTERNATIONAL_CARD. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Customer, Payment, PaymentDAO, order |

## OfferState

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OfferState | Knows OFFERED, ACCEPTED, DECLINED, WITHDRAWN. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | ReplacementOffer, ReplacementOfferDAO |

## Role

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Role | Knows CUSTOMER, KITCHEN_STAFF, SHIPPER, ADMIN, MANAGER. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | UserAccount |

## KitchenBoard

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| KitchenBoard | Knows hub, columns. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | KitchenController |

## BoardEntry

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| BoardEntry | Knows order, awaiting_customer. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | KitchenBoard, KitchenController |

## KitchenOrderView

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| KitchenOrderView | Knows order, payment, open_offer, offers, candidates. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | KitchenController |

## OrderSummary

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| OrderSummary | Knows order, hub_name, awaiting_answer. Does typed value / enumeration initialization and attribute access. Coordinate authorization, domain decisions and data access. | OrderTrackingController |

## Hub

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| Hub | Knows id, code, name, address_text, latitude, longitude, max_active_orders, base_delivery_fee, archived_at. Does typed value / enumeration initialization and attribute access. Represent a kitchen location, capacity and fee. | HubDAO, KitchenBoard, KitchenController, OrderDetail |

## CustomerType

| Class | Responsibilities (knows / does) | Collaborators |
|---|---|---|
| CustomerType | Knows LOCAL, TOURIST. Does typed value / enumeration initialization and attribute access. Hold typed business state and its local rules. | Customer, LocalCustomer, TouristCustomer |
