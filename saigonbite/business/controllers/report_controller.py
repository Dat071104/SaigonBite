"""ReportController (UC-04 Produce management reports). Read-only: no method writes.

    requestSalesReport     -> sales_report(user_id, date_from, date_to, hub_id)
    requestWorkloadReport  -> workload_report(user_id)
    requestDeliveryReport  -> delivery_report(user_id, date_from, date_to, hub_id)

Definitions (Q5 / A-07, plan §0.1):
  * Sales are DELIVERED orders counted on the day they were delivered, in Ho Chi Minh City time.
    The period is every day from date_from to date_to inclusive: [date_from 00:00, date_to + 1 00:00).
  * Workload is a snapshot now: orders still to cook (PLACED, CONFIRMED, PREPARING) against capacity.
  * Delivery performance covers deliveries that ended (DELIVERED or FAILED) in the period:
    wait = READY -> PICKED_UP, ride = PICKED_UP -> DELIVERED, failure rate = failed / (delivered + failed).
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Optional

from saigonbite.business.domain import Hub, HubStatus, OrderState, Role
from saigonbite.data_access import HubDAO, ReportDAO
from saigonbite.data_access.report_dao import ReportDataUnavailable

from .common import BaseController, vn_day_start_utc
from .errors import ValidationError

MAX_DAYS = 366
DEFAULT_DAYS = 7


@dataclass
class Period:
    date_from: str
    date_to: str
    start_utc: str
    end_utc: str


@dataclass
class SalesRow:
    label: str
    orders: int = 0
    item_sales: int = 0
    voucher_discounts: int = 0
    delivery_fees: int = 0
    total: int = 0
    refunds_owed: int = 0

    @property
    def net(self) -> int:
        # BR-24: reduced T already reflects accepted replacement pricing.
        # The difference from original charge is an obligation, not another sales deduction.
        return self.total

    def add(self, other: "SalesRow") -> None:
        for name in ("orders", "item_sales", "voucher_discounts", "delivery_fees", "total", "refunds_owed"):
            setattr(self, name, getattr(self, name) + getattr(other, name))


@dataclass
class SalesReport:
    period: Period
    hub: Optional[Hub]
    rows: list[SalesRow]
    totals: SalesRow
    top_items: list[tuple[int, str, int, int]]      # item ID, snapshot name, quantity, revenue


@dataclass
class WorkloadRow:
    status: HubStatus
    counts: dict[OrderState, int]

    @property
    def label(self) -> str:
        if self.status.busy:
            return "Busy"
        return "Quiet" if self.status.quiet else "Normal"


@dataclass
class WorkloadReport:
    as_of: str
    rows: list[WorkloadRow]


@dataclass
class DeliveryRow:
    label: str
    delivered: int = 0
    failed: int = 0
    waits: list[float] = field(default_factory=list)
    rides: list[float] = field(default_factory=list)

    @property
    def failure_rate(self) -> Optional[float]:
        finished = self.delivered + self.failed
        return round(100 * self.failed / finished, 1) if finished else None

    @property
    def avg_wait(self) -> Optional[float]:
        return round(sum(self.waits) / len(self.waits), 1) if self.waits else None

    @property
    def avg_ride(self) -> Optional[float]:
        return round(sum(self.rides) / len(self.rides), 1) if self.rides else None


@dataclass
class DeliveryReport:
    period: Period
    hub: Optional[Hub]
    by_hub: list[DeliveryRow]
    by_shipper: list[DeliveryRow]
    overall: DeliveryRow


def _minutes(start: Optional[str], end: Optional[str]) -> Optional[float]:
    if not start or not end:
        return None
    return (datetime.fromisoformat(end) - datetime.fromisoformat(start)).total_seconds() / 60


class ReportController(BaseController):
    def __init__(self, conn: sqlite3.Connection, clock=None):
        super().__init__(conn, clock)
        self.reports = ReportDAO(conn)
        self.hubs = HubDAO(conn)

    def all_hubs(self) -> list[Hub]:
        return self.hubs.list_all()

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

    def workload_report(self, user_id: int) -> WorkloadReport:
        self._require_manager(user_id)
        counts: dict[int, dict[OrderState, int]] = {}
        for r in self.reports.open_orders_by_hub_and_state():
            counts.setdefault(r["hub_id"], {})[OrderState(r["state"])] = r["n"]
        rows = []
        for hub in self.hubs.list_all():
            per_state = counts.get(hub.id, {})
            load = sum(per_state.get(s, 0) for s in (OrderState.PLACED, OrderState.CONFIRMED, OrderState.PREPARING))
            rows.append(WorkloadRow(status=HubStatus(hub, load), counts=per_state))
        return WorkloadReport(as_of=self._now(), rows=rows)

    def delivery_report(self, user_id: int, date_from: Optional[str] = None, date_to: Optional[str] = None,
                        hub_id: Optional[int] = None) -> DeliveryReport:
        self._require_manager(user_id)
        period, hub = self._period(date_from, date_to), self._hub(hub_id)
        by_hub: dict[int, DeliveryRow] = {}
        by_shipper: dict[int, DeliveryRow] = {}
        overall = DeliveryRow(label="All deliveries")
        for r in self.reports.finished_deliveries(period.start_utc, period.end_utc, hub_id):
            targets = (by_hub.setdefault(r["hub_id"], DeliveryRow(label=r["hub_name"])),
                       by_shipper.setdefault(r["shipper_id"], DeliveryRow(label=r["shipper_name"] or "Unknown")),
                       overall)
            wait = _minutes(r["ready_at"], r["picked_up_at"])
            ride = _minutes(r["picked_up_at"], r["finished_at"]) if r["state"] == "DELIVERED" else None
            for row in targets:
                if r["state"] == "DELIVERED":
                    row.delivered += 1
                else:
                    row.failed += 1
                if wait is not None:
                    row.waits.append(wait)
                if ride is not None:
                    row.rides.append(ride)
        return DeliveryReport(period=period, hub=hub, by_hub=list(by_hub.values()),
                              by_shipper=sorted(by_shipper.values(), key=lambda r: r.label), overall=overall)

    # ---- internals ---------------------------------------------------------------------

    def _require_manager(self, user_id: int) -> None:
        self._require_user(user_id, Role.MANAGER, message="Only managers can read the reports.")

    def _hub(self, hub_id: Optional[int]) -> Optional[Hub]:
        if hub_id is None:
            return None
        hub = self.hubs.get_including_archived(hub_id)
        if hub is None:
            raise ValidationError("Choose a hub from the list.")
        return hub

    def _period(self, date_from: Optional[str], date_to: Optional[str]) -> Period:
        today = date.fromisoformat(self._today_vn())
        try:
            end = date.fromisoformat(date_to) if date_to else today
            start = date.fromisoformat(date_from) if date_from else end - timedelta(days=DEFAULT_DAYS - 1)
        except ValueError:
            raise ValidationError("Enter the dates as YYYY-MM-DD.") from None
        if start > end:
            raise ValidationError("The first day must be on or before the last day.")
        if (end - start).days >= MAX_DAYS:
            raise ValidationError(f"Choose a period of at most {MAX_DAYS} days.")
        return Period(date_from=start.isoformat(), date_to=end.isoformat(), start_utc=vn_day_start_utc(start),
                      end_utc=vn_day_start_utc(end + timedelta(days=1)))
