"""Read-only queries for the management reports (UC-04). Nothing here writes.

Order totals are summed from the orders table only (one row per order: delivery and payment are 1:1),
never from a join with order_line, so a multi-line order is counted once (plan §7).
Archived orders are included: archiving hides an order from operational screens, not from reports.
"""
from __future__ import annotations

import sqlite3
from typing import Optional


class ReportDAO:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def sales_by_hub(self, start_utc: str, end_utc: str, hub_id: Optional[int]) -> list[sqlite3.Row]:
        """DELIVERED orders whose delivery finished in [start_utc, end_utc), one row per hub."""
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

    def top_items(self, start_utc: str, end_utc: str, hub_id: Optional[int], limit: int = 10) -> list[sqlite3.Row]:
        """Dishes sold on DELIVERED orders in the period, by revenue (line level, so the join is correct here)."""
        return self.conn.execute(
            "SELECT ol.item_name, SUM(ol.quantity) AS quantity, SUM(ol.unit_price * ol.quantity) AS revenue "
            "FROM order_line ol "
            "JOIN orders o ON o.id = ol.order_id "
            "JOIN delivery d ON d.order_id = o.id "
            "WHERE o.state = 'DELIVERED' AND d.finished_at >= ? AND d.finished_at < ? "
            "  AND (? IS NULL OR o.hub_id = ?) "
            "GROUP BY ol.item_name ORDER BY revenue DESC, ol.item_name LIMIT ?",
            (start_utc, end_utc, hub_id, hub_id, limit)).fetchall()

    def open_orders_by_hub_and_state(self) -> list[sqlite3.Row]:
        """Current counts of unfinished orders per hub and state (workload snapshot)."""
        return self.conn.execute(
            "SELECT hub_id, state, COUNT(*) AS n FROM orders "
            "WHERE state IN ('PLACED', 'CONFIRMED', 'PREPARING', 'READY', 'OUT_FOR_DELIVERY') "
            "GROUP BY hub_id, state").fetchall()

    def finished_deliveries(self, start_utc: str, end_utc: str, hub_id: Optional[int]) -> list[sqlite3.Row]:
        """Deliveries that ended (DELIVERED or FAILED) in [start_utc, end_utc)."""
        return self.conn.execute(
            "SELECT o.id AS order_id, o.hub_id, h.name AS hub_name, d.state, d.ready_at, d.picked_up_at, "
            "       d.finished_at, d.shipper_id, u.display_name AS shipper_name "
            "FROM delivery d "
            "JOIN orders o ON o.id = d.order_id "
            "JOIN hub h ON h.id = o.hub_id "
            "LEFT JOIN user_account u ON u.id = d.shipper_id "
            "WHERE d.state IN ('DELIVERED', 'FAILED') AND d.finished_at >= ? AND d.finished_at < ? "
            "  AND (? IS NULL OR o.hub_id = ?) "
            "ORDER BY o.hub_id, d.finished_at",
            (start_utc, end_utc, hub_id, hub_id)).fetchall()
