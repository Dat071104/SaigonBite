# 4.3.5 Software Classes Method Code

Author: 722I0004 · AI-assisted (Codex, Claude)

For every main use case, the methods that realise one important system operation are printed in full, in the order of its sequence diagram (controller, then domain, then data access). They are copied unchanged from the source files of release v0.9-part2; the line numbers refer to that release. All other classes and methods are in the repository (`saigonbite/`); the design class tables in 3.x.1 list every method signature.

## UC-01 — confirmCheckout (OP-01)

The customer confirms the quote: the controller re-prices, checks consent and capacity inside one transaction, the domain creates the order, and the DAO stores it.

**PlaceOrderController.confirm_order** — `saigonbite/business/controllers/place_order_controller.py`, lines 88–140; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/controllers/place_order_controller.py#L88-L140).

```python
def confirm_order(self, user_id: int, hub_id: int, address_id: Optional[int],
                  quantities: Mapping[int, str], idempotency_token: str,
                  quoted_total: Optional[int] = None, voucher_code: Optional[str] = None,
                  payment: Optional[PaymentChoice] = None,
                  quote_fingerprint: Optional[str] = None) -> OrderConfirmation:
    """Create Order(PLACED) + OrderLines + Payment in ONE transaction.

    Payment is COD PENDING, or ONLINE PAID when the simulator approved it (A-06: the money is taken
    when the order is saved; a failed save releases the authorisation).
    A repeated call with the same token returns the first order and writes nothing.
    The capacity rule is checked again inside the write lock, so two customers cannot both take
    the last slot of a hub (R-03).
    quoted_total is the total the customer saw on the quote page. It is only compared, never
    used as a price: if it is missing or the re-priced total differs, no order is written and
    QuoteChangedError carries the current quote for the customer to confirm.
    """
    customer = self._require_customer(user_id)
    token = (idempotency_token or "").strip()
    if not token:
        raise ValidationError("This order form has expired. Please start the order again.")
    payment = payment or PaymentChoice()
    reference = None
    try:
        with immediate_transaction(self.conn):
            customer = self._require_customer(user_id)
            existing = self.orders.get_by_token(token)
            if existing is not None:
                if existing.customer_id != customer.id:
                    raise AuthorizationError("This order belongs to another customer.")
                return self._confirmation(existing, created=False)
            self._check_payment_choice(customer, payment)
            quote = self._build_quote(customer, hub_id, address_id, quantities, voucher_code)
            if quoted_total is None or not quote_fingerprint:
                raise QuoteChangedError(quote, QuoteChangedError.MISSING)
            if quoted_total != quote.total or quote_fingerprint != quote.fingerprint(payment.method,payment.option):
                raise QuoteChangedError(quote)
            if payment.method is PaymentMethod.ONLINE:
                auth = self.gateway.authorise(quote.total, payment.option, payment.outcome)
                if not auth.approved:
                    raise PaymentDeclinedError(quote, f"{auth.message} No order was placed. Try again or choose cash on delivery.")
                reference = auth.reference
            now = self._now()
            order = Order.place(customer.id, quote, token, now)
            order.id = self.orders.insert(order)
            self.payments.insert(Payment(
                order_id=order.id, method=payment.method, online_option=payment.option,
                provider_ref=reference, amount=order.total, created_at=now,
                state=PaymentState.PAID if payment.method is PaymentMethod.ONLINE else PaymentState.PENDING))
    except BaseException:
        if reference:
            self.gateway.release(reference)
        raise
    return self._confirmation(self.orders.get_by_id(order.id), created=True)
```

**Order.place** — `saigonbite/business/domain/models.py`, lines 320–330; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/domain/models.py#L320-L330).

```python
@classmethod
def place(cls, customer_id: int, quote: Quote, idempotency_token: str, placed_at: str) -> "Order":
    """Create a new order in state PLACED from an accepted quote."""
    return cls(customer_id=customer_id, hub_id=quote.hub.id, address_id=quote.address.id,
               state=OrderState.PLACED, delivery_fee=quote.delivery_fee,
               idempotency_token=idempotency_token, placed_at=placed_at,
               delivery_address_text=quote.address.full_address, distance_km=round(quote.distance_km,2),
               voucher_id=quote.voucher.id if quote.voucher else None,
               voucher_discount=quote.voucher_discount, quiet_discount=quote.quiet_discount,
               lines=[OrderLine(l.menu_item_id, l.item_name, l.unit_price, l.quantity)
                      for l in quote.lines])
```

**OrderDAO.insert** — `saigonbite/data_access/order_dao.py`, lines 20–36; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/data_access/order_dao.py#L20-L36).

```python
def insert(self, order: Order) -> int:
    """Insert the order header and all lines; return the new order id."""
    cur = self.conn.execute(
        "INSERT INTO orders (customer_id, hub_id, address_id, delivery_address_text, distance_km, state, "
        "                    item_subtotal, voucher_id, voucher_discount, delivery_fee, quiet_discount, "
        "                    total_amount, idempotency_token, placed_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (order.customer_id, order.hub_id, order.address_id, order.delivery_address_text, order.distance_km,
         order.state.value, order.item_subtotal, order.voucher_id, order.voucher_discount, order.delivery_fee,
         order.quiet_discount, order.total, order.idempotency_token, order.placed_at))
    order_id = cur.lastrowid
    for line in order.lines:
        self.conn.execute(
            "INSERT INTO order_line (order_id, menu_item_id, item_name, unit_price, quantity) "
            "VALUES (?, ?, ?, ?, ?)",
            (order_id, line.menu_item_id, line.item_name, line.unit_price, line.quantity))
    return order_id
```

## UC-02 — takeDelivery (OP-10)

A shipper takes a READY order; the guarded UPDATE lets only one of two competing shippers succeed.

**DeliveryController.pick_up** — `saigonbite/business/controllers/delivery_controller.py`, lines 77–88; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/controllers/delivery_controller.py#L77-L88).

```python
def pick_up(self, user_id: int, order_id: int) -> DeliveryView:
    """Atomic: when two shippers press Pick up together, only the first one gets the order."""
    shipper = self._require_shipper(user_id)
    with immediate_transaction(self.conn):
        delivery = self._delivery(order_id)
        if delivery.state is not DeliveryState.AWAITING_PICKUP or delivery.shipper_id is not None:
            raise ConflictError(f"Order {order_id} has already been picked up. Nothing was changed.")
        now = self._now()
        if not self.deliveries.take(order_id, shipper.id, now):
            raise ConflictError(f"Order {order_id} has already been picked up. Nothing was changed.")
        move_order(self.orders, self.orders.get_by_id(order_id), OrderState.OUT_FOR_DELIVERY, now)
    return self.get_delivery(user_id, order_id)
```

**DeliveryDAO.take** — `saigonbite/data_access/delivery_dao.py`, lines 47–52; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/data_access/delivery_dao.py#L47-L52).

```python
def take(self, order_id: int, shipper_id: int, now: str) -> bool:
    """AWAITING_PICKUP -> PICKED_UP for this shipper. Only the first of two competing shippers wins."""
    cur = self.conn.execute(
        "UPDATE delivery SET shipper_id = ?, state = 'PICKED_UP', picked_up_at = ? "
        "WHERE order_id = ? AND state = 'AWAITING_PICKUP' AND shipper_id IS NULL", (shipper_id, now, order_id))
    return cur.rowcount == 1
```

## UC-02 — confirmDelivered (OP-11)

The assigned shipper finishes the delivery; for COD the cash collected must equal the order total.

**DeliveryController.confirm_delivered** — `saigonbite/business/controllers/delivery_controller.py`, lines 90–116; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/controllers/delivery_controller.py#L90-L116).

```python
def confirm_delivered(self, user_id: int, order_id: int, cash_collected: Optional[str]) -> DeliveryView:
    """COD: the cash entered must equal the order total, and the payment becomes PAID once.
    Online: no cash is taken (the field must be empty or 0)."""
    shipper = self._require_shipper(user_id)
    with immediate_transaction(self.conn):
        delivery = self._own_active_delivery(shipper, order_id)
        payment = self.payments.get_by_order_id(order_id)
        order = self.orders.get_by_id(order_id)
        cash = self._parse_cash(cash_collected)
        now = self._now()
        if payment.method is PaymentMethod.COD:
            if cash != order.total or payment.amount != order.total:
                raise ValidationError(f"Collect exactly {payment.amount:,} VND in cash and enter that amount.")
            payment.move_to(PaymentState.PAID)
            if not self.payments.change_state(order_id, PaymentState.PENDING, PaymentState.PAID, now):
                raise ConflictError("The payment was already recorded. Nothing was changed.")
        else:
            if payment.state is not PaymentState.PAID:
                raise ConflictError('The online payment is not in a fulfilled-payment state.')
            if cash not in (None, 0):
                raise ValidationError("This order was paid online. Do not take cash from the customer.")
            cash = None
        delivery.move_to(DeliveryState.DELIVERED)
        if not self.deliveries.finish(order_id, shipper.id, DeliveryState.DELIVERED, now, cash_collected=cash):
            raise ConflictError("This delivery was already finished. Nothing was changed.")
        move_order(self.orders, self.orders.get_by_id(order_id), OrderState.DELIVERED, now)
    return self.get_delivery(user_id, order_id)
```

**DeliveryDAO.finish** — `saigonbite/data_access/delivery_dao.py`, lines 54–61; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/data_access/delivery_dao.py#L54-L61).

```python
def finish(self, order_id: int, shipper_id: int, to_state: DeliveryState, now: str,
           failure_reason: Optional[str] = None, cash_collected: Optional[int] = None) -> bool:
    """PICKED_UP -> DELIVERED or FAILED, only by the shipper who picked it up."""
    cur = self.conn.execute(
        "UPDATE delivery SET state = ?, finished_at = ?, failure_reason = ?, cash_collected = ? "
        "WHERE order_id = ? AND shipper_id = ? AND state = 'PICKED_UP'",
        (to_state.value, now, failure_reason, cash_collected, order_id, shipper_id))
    return cur.rowcount == 1
```

## UC-03 — archiveHub (OP-36)

The admin archives a hub; the controller refuses while the hub still has open orders.

**HubController.archive_hub** — `saigonbite/business/controllers/hub_controller.py`, lines 88–104; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/controllers/hub_controller.py#L88-L104).

```python
def archive_hub(self, user_id: int, hub_id: int) -> Hub:
    """Guard: no open orders (anything not yet delivered, failed, rejected or cancelled).
    Archived hubs leave browsing and checkout; order history still shows them."""
    self._require_admin(user_id)
    with immediate_transaction(self.conn):
        hub = self.hubs.get_including_archived(hub_id)
        if hub is None:
            raise NotFoundError("Hub not found.")
        if hub.archived_at is not None:
            raise ConflictError(f"{hub.name} is already archived.")
        open_orders = self.hubs.open_order_count(hub_id)
        if open_orders:
            raise ConflictError(f"{hub.name} still has {open_orders} open order(s). "
                                "Archive it when they are finished.")
        if not self.hubs.archive(hub_id, self._now()):
            raise ConflictError('The hub changed before archive. Please reload.')
    return self.hubs.get_including_archived(hub_id)
```

**HubDAO.archive** — `saigonbite/data_access/hub_dao.py`, lines 66–69; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/data_access/hub_dao.py#L66-L69).

```python
def archive(self, hub_id: int, now: str) -> bool:
    cur = self.conn.execute("UPDATE hub SET archived_at = ? WHERE id = ? AND archived_at IS NULL",
                            (now, hub_id))
    return cur.rowcount == 1
```

## UC-04 — salesReport (OP-26)

The manager asks for sales in a Vietnam-date range; the DAO aggregates delivered orders by hub.

**ReportController.sales_report** — `saigonbite/business/controllers/report_controller.py`, lines 134–147; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/controllers/report_controller.py#L134-L147).

```python
def sales_report(self, user_id: int, date_from: Optional[str] = None, date_to: Optional[str] = None,
                 hub_id: Optional[int] = None) -> SalesReport:
    self._require_manager(user_id)
    period, hub = self._period(date_from, date_to), self._hub(hub_id)
    rows = [SalesRow(label=r["hub_name"], orders=r["orders"], item_sales=r["item_sales"],
                     voucher_discounts=r["voucher_discounts"], delivery_fees=r["delivery_fees"],
                     total=r["total"], refunds_owed=r["refunds_owed"])
            for r in self.reports.sales_by_hub(period.start_utc, period.end_utc, hub_id)]
    totals = SalesRow(label="All hubs" if hub is None else hub.name)
    for row in rows:
        totals.add(row)
    top = [(r["menu_item_id"], r["item_name"], r["quantity"], r["revenue"])
           for r in self.reports.top_items(period.start_utc, period.end_utc, hub_id)]
    return SalesReport(period=period, hub=hub, rows=rows, totals=totals, top_items=top)
```

**ReportDAO.sales_by_hub** — `saigonbite/data_access/report_dao.py`, lines 31–46; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/data_access/report_dao.py#L31-L46).

```python
def sales_by_hub(self, start_utc: str, end_utc: str, hub_id: Optional[int]) -> list[sqlite3.Row]:
    """DELIVERED orders whose delivery finished in [start_utc, end_utc), one row per hub."""
    self.assert_complete()
    return self.conn.execute(
        "SELECT h.id AS hub_id, h.name AS hub_name, COUNT(*) AS orders, "
        "       SUM(o.item_subtotal) AS item_sales, SUM(o.voucher_discount) AS voucher_discounts, "
        "       SUM(o.delivery_fee - o.quiet_discount) AS delivery_fees, SUM(o.total_amount) AS total, "
        "       SUM(p.refund_amount) AS refunds_owed "
        "FROM orders o "
        "JOIN delivery d ON d.order_id = o.id "
        "JOIN payment p ON p.order_id = o.id "
        "JOIN hub h ON h.id = o.hub_id "
        "WHERE o.state = 'DELIVERED' AND d.finished_at >= ? AND d.finished_at < ? "
        "  AND (? IS NULL OR o.hub_id = ?) "
        "GROUP BY h.id, h.name ORDER BY h.id",
        (start_utc, end_utc, hub_id, hub_id)).fetchall()
```

## UC-05 — rejectOrder (OP-03)

Kitchen staff reject an own-hub PLACED order; the payment is released (COD voided, online amount owed back).

**KitchenController.reject_order** — `saigonbite/business/controllers/kitchen_controller.py`, lines 93–110; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/controllers/kitchen_controller.py#L93-L110).

```python
def reject_order(self, user_id: int, order_id: int, reason: str) -> Order:
    """A-06: COD is voided, an online payment becomes REFUND_PENDING. A reason is required."""
    staff = self._require_staff(user_id)
    reason = (reason or "").strip()
    if not reason:
        raise ValidationError("Please give the reason for rejecting the order.")
    if len(reason) > 200:
        raise ValidationError("The reason must be at most 200 characters.")
    with immediate_transaction(self.conn):
        order = self._hub_order(staff, order_id)
        now = self._now()
        move_order(self.orders, order, OrderState.REJECTED, now, reason)
        offer = self.offers.get_open(order.id)
        if offer is not None:
            if not self.offers.decide(offer.id, OfferState.WITHDRAWN, now):
                raise ConflictError('The open offer changed. Please reload.')
        release_payment(self.payments, order.id, now)
    return order
```

**Payment.release_for_unfulfilled_order** — `saigonbite/business/domain/models.py`, lines 280–283; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/domain/models.py#L280-L283).

```python
def release_for_unfulfilled_order(self) -> None:
    """Rejection, cancellation or failed delivery (A-06): COD is voided, an online payment is owed back."""
    self.move_to(PaymentState.VOIDED if self.method is PaymentMethod.COD else PaymentState.REFUND_PENDING)
    self.refund_amount = self.amount if self.method is PaymentMethod.ONLINE else 0
```

## UC-05 — acceptReplacement (OP-05)

The customer answers an open replacement offer; the controller re-checks the exact offer and the target before the line is replaced.

**OrderTrackingController.answer_replacement** — `saigonbite/business/controllers/order_tracking_controller.py`, lines 77–113; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/controllers/order_tracking_controller.py#L77-L113).

```python
def answer_replacement(self, user_id: int, order_id: int, offer_id: int, accept: bool) -> OrderDetail:
    """Accept: the line takes the new dish and price, totals are recomputed; COD owes the new total,
    ONLINE records the difference as refund owed (payment stays PAID).
    Decline: the order is REJECTED and the payment released (A-06)."""
    customer = self._require_customer(user_id)
    notice = None
    with immediate_transaction(self.conn):
        order = self._own_order(customer, order_id)
        offer = self.offers.get_open(order.id)
        if order.state is not OrderState.PLACED or offer is None or offer.id != offer_id:
            raise ConflictError("This replacement offer is no longer open. Nothing was changed.")
        now = self._now()
        target_valid = self.hubs.get_available_item(order.hub_id,offer.new_menu_item_id) is not None
        if accept and not target_valid:
            if not self.offers.decide(offer.id,OfferState.WITHDRAWN,now):
                raise ConflictError('The offer changed. Please reload.')
            notice = 'The replacement is no longer available. The offer was withdrawn; your order and payment are unchanged.'
        elif accept:
            order.replace_line(offer.order_line_id, offer.new_menu_item_id, offer.new_item_name,
                               offer.new_unit_price)
            if not self.orders.save_lines_and_totals(order):
                raise ConflictError('The order lines changed. Please reload.')
            payment = self.payments.get_by_order_id(order.id)
            if payment.method is PaymentMethod.COD:
                saved = self.payments.set_amounts(order.id, order.total, 0, now)
            else:
                saved = self.payments.set_amounts(order.id, payment.amount, payment.amount - order.total, now)
            if not saved or not self.offers.decide(offer.id, OfferState.ACCEPTED, now):
                raise ConflictError('The payment or offer changed. Please reload.')
        else:
            if not self.offers.decide(offer.id, OfferState.DECLINED, now):
                raise ConflictError('The offer changed. Please reload.')
            move_order(self.orders, order, OrderState.REJECTED, now, DECLINED_REASON)
            release_payment(self.payments, order.id, now)
    result = self.get_order(user_id, order_id)
    result.notice = notice
    return result
```

**Order.replace_line** — `saigonbite/business/domain/models.py`, lines 343–352; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/domain/models.py#L343-L352).

```python
def replace_line(self, line_id: int, menu_item_id: int, item_name: str, unit_price: int) -> None:
    """Apply an accepted replacement. The voucher discount agreed at checkout is kept,
    but never more than the new item subtotal, so the total can only stay the same or fall."""
    if self.state is not OrderState.PLACED:
        raise InvalidTransition('Only a PLACED order can accept a replacement.')
    line = self.line(line_id)
    if line is None:
        raise ValueError(f"Order {self.id} has no line {line_id}")
    line.menu_item_id, line.item_name, line.unit_price = menu_item_id, item_name, unit_price
    self.voucher_discount = min(self.voucher_discount, self.item_subtotal)
```

## UC-06 — updateMenuItem (OP-41)

The admin edits a menu item; earlier orders keep their own name and price snapshot.

**MenuController.update_item** — `saigonbite/business/controllers/menu_controller.py`, lines 109–126; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/controllers/menu_controller.py#L109-L126).

```python
def update_item(self, user_id: int, item_id: int, form: Mapping[str, str]) -> MenuItem:
    """Name, description and price. The brand of a dish does not change."""
    self._require_admin(user_id)
    with immediate_transaction(self.conn):
        current = self._active_item(item_id)
        self._active_brand(current.brand_id)
        try:
            context = int(form.get('brand_id') or 0)
        except ValueError:
            context = 0
        if context != current.brand_id:
            raise ValidationError('The brand context must match the current parent; reparenting is not supported.')
        item = self._parse_item({**form, "brand_id": str(current.brand_id)}, item_id=item_id)
        if self.menu.item_name_exists(current.brand_id, item.name, except_id=item_id):
            raise ValidationError(f"{current.brand_name} already has a dish called {item.name}.")
        if not self.menu.update_item(item):
            raise ConflictError('The item changed before saving.')
    return self.menu.get_item(item_id)
```

**MenuDAO.update_item** — `saigonbite/data_access/menu_dao.py`, lines 66–71; [source at release v0.9-part2]({{LinkRepo}}/blob/v0.9-part2/saigonbite/data_access/menu_dao.py#L66-L71).

```python
def update_item(self, item: MenuItem) -> bool:
    """Change name, description or price. Order lines keep their own copy, so history is unchanged."""
    cur = self.conn.execute(
        "UPDATE menu_item SET name = ?, description = ?, price = ? WHERE id = ? AND archived_at IS NULL",
        (item.name, item.description, item.price, item.id))
    return cur.rowcount == 1
```

