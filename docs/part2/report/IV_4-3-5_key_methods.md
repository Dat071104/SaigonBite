# 4.3.5 Software Classes Method Code

Author: 722I0004 · AI-assisted (Codex)

These excerpts are copied from the source files at the P7 working revision. Each path links to the planned release tag; the tag link will resolve only after the release is published. An excerpt can omit other guards or calls in the same method. The operation and sequence references identify the corresponding design, while the named code is the implementation.

## UC-01 — confirmCheckout (OP-01)

SSD: `models/UC-01/ssd_uc01_PartB.drawio#01S-M04`. Design sequence: `models/UC-01/seq_uc01_confirmCheckout_PartA.png`. The controller and data-access excerpts follow the operation realisation; domain or value behavior is included where that operation calls a named method.

**PlaceOrderController.confirm_order** — `saigonbite/business/controllers/place_order_controller.py`, lines 104–115; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/controllers/place_order_controller.py#L104-L115).

```python
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
```

**Order.place** — `saigonbite/business/domain/models.py`, lines 323–330; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/domain/models.py#L323-L330).

```python
        return cls(customer_id=customer_id, hub_id=quote.hub.id, address_id=quote.address.id,
                   state=OrderState.PLACED, delivery_fee=quote.delivery_fee,
                   idempotency_token=idempotency_token, placed_at=placed_at,
                   delivery_address_text=quote.address.full_address, distance_km=round(quote.distance_km,2),
                   voucher_id=quote.voucher.id if quote.voucher else None,
                   voucher_discount=quote.voucher_discount, quiet_discount=quote.quiet_discount,
                   lines=[OrderLine(l.menu_item_id, l.item_name, l.unit_price, l.quantity)
                          for l in quote.lines])
```

**OrderDAO.insert** — `saigonbite/data_access/order_dao.py`, lines 22–33; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/data_access/order_dao.py#L22-L33).

```python
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
```

## UC-02 — takeDelivery (OP-10)

SSD: `models/UC-02/ssd_uc02_PartA.drawio#M03`. Design sequence: `models/UC-02/seq_uc02_takeDelivery.png`. The controller and data-access excerpts follow the operation realisation; domain or value behavior is included where that operation calls a named method.

**DeliveryController.pick_up** — `saigonbite/business/controllers/delivery_controller.py`, lines 79–88; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/controllers/delivery_controller.py#L79-L88).

```python
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

**Order.move_to** — `saigonbite/business/domain/models.py`, lines 336–338; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/domain/models.py#L336-L338).

```python
        if not self.can_move_to(new_state):
            raise InvalidTransition(f"Order {self.id}: {self.state.value} -> {new_state.value} is not allowed")
        self.state = new_state
```

**DeliveryDAO.take** — `saigonbite/data_access/delivery_dao.py`, lines 49–52; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/data_access/delivery_dao.py#L49-L52).

```python
        cur = self.conn.execute(
            "UPDATE delivery SET shipper_id = ?, state = 'PICKED_UP', picked_up_at = ? "
            "WHERE order_id = ? AND state = 'AWAITING_PICKUP' AND shipper_id IS NULL", (shipper_id, now, order_id))
        return cur.rowcount == 1
```

## UC-03 — archiveHub (OP-36)

SSD: `models/UC-03/ssd_uc03.drawio#M03-05`. Design sequence: `models/UC-03/seq_uc03_archiveHub.png`. The controller and data-access excerpts follow the operation realisation; domain or value behavior is included where that operation calls a named method.

The design records construction or reading of typed values, rather than a separate domain behavior call for this operation.

**HubController.archive_hub** — `saigonbite/business/controllers/hub_controller.py`, lines 91–102; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/controllers/hub_controller.py#L91-L102).

```python
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
```

**HubDAO.archive** — `saigonbite/data_access/hub_dao.py`, lines 67–69; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/data_access/hub_dao.py#L67-L69).

```python
        cur = self.conn.execute("UPDATE hub SET archived_at = ? WHERE id = ? AND archived_at IS NULL",
                                (now, hub_id))
        return cur.rowcount == 1
```

## UC-04 — salesReport (OP-26)

SSD: `models/UC-04/ssd_uc04.drawio#M01`. Design sequence: `models/UC-04/seq_uc04_salesReport.png`. The controller and data-access excerpts follow the operation realisation; domain or value behavior is included where that operation calls a named method.

**ReportController.sales_report** — `saigonbite/business/controllers/report_controller.py`, lines 136–147; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/controllers/report_controller.py#L136-L147).

```python
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

**SalesRow.add** — `saigonbite/business/controllers/report_controller.py`, lines 57–58; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/controllers/report_controller.py#L57-L58).

```python
        for name in ("orders", "item_sales", "voucher_discounts", "delivery_fees", "total", "refunds_owed"):
            setattr(self, name, getattr(self, name) + getattr(other, name))
```

**ReportDAO.sales_by_hub** — `saigonbite/data_access/report_dao.py`, lines 33–44; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/data_access/report_dao.py#L33-L44).

```python
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
```

## UC-05 — rejectOrder (OP-03)

SSD: `models/UC-05/ssd_uc05_PartA.drawio#05S-M04`. Design sequence: `models/UC-05/seq_uc05_rejectOrder.png`. The controller and data-access excerpts follow the operation realisation; domain or value behavior is included where that operation calls a named method.

**KitchenController.reject_order** — `saigonbite/business/controllers/kitchen_controller.py`, lines 95–106; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/controllers/kitchen_controller.py#L95-L106).

```python
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
```

**Payment.release_for_unfulfilled_order** — `saigonbite/business/domain/models.py`, lines 282–283; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/domain/models.py#L282-L283).

```python
        self.move_to(PaymentState.VOIDED if self.method is PaymentMethod.COD else PaymentState.REFUND_PENDING)
        self.refund_amount = self.amount if self.method is PaymentMethod.ONLINE else 0
```

**PaymentDAO.set_amounts** — `saigonbite/data_access/payment_dao.py`, lines 41–43; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/data_access/payment_dao.py#L41-L43).

```python
        cur = self.conn.execute("UPDATE payment SET amount = ?, refund_amount = ?, updated_at = ? WHERE order_id = ?",
                          (amount, refund_amount, now, order_id))
        return cur.rowcount == 1
```

## UC-06 — updateMenuItem (OP-41)

SSD: `models/UC-06/ssd_uc06_PartB.drawio#M06-B03`. Design sequence: `models/UC-06/seq_uc06_updateMenuItem.png`. The controller and data-access excerpts follow the operation realisation; domain or value behavior is included where that operation calls a named method.

The design records construction or reading of typed values, rather than a separate domain behavior call for this operation.

**MenuController.update_item** — `saigonbite/business/controllers/menu_controller.py`, lines 111–122; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/business/controllers/menu_controller.py#L111-L122).

```python
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
```

**MenuDAO.update_item** — `saigonbite/data_access/menu_dao.py`, lines 68–71; author 722I0004; [planned tag]({{LinkRepo}}/blob/v0.9-part2/saigonbite/data_access/menu_dao.py#L68-L71).

```python
        cur = self.conn.execute(
            "UPDATE menu_item SET name = ?, description = ?, price = ? WHERE id = ? AND archived_at IS NULL",
            (item.name, item.description, item.price, item.id))
        return cur.rowcount == 1
```
