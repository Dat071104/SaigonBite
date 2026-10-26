"""Business rules and their figures, in one place (plan §0.1).

The figures are team defaults, not client-confirmed: Q1 (busy and quiet hub), Q2 (distance and fee),
Q4 (online payment options). A client answer changes a value here and the tests that pin it.
"""
from __future__ import annotations

import math

from .enums import CustomerType, OnlineOption, OrderState

MAX_QUANTITY = 99

# Q1 / A-02: workload = orders the kitchen still has to cook. A hub is busy at or above its capacity.
ACTIVE_ORDER_STATES = (OrderState.PLACED, OrderState.CONFIRMED, OrderState.PREPARING)
# Q1 / A-03: a quiet hub (load below a quarter of capacity) takes 5,000 VND off the delivery fee.
QUIET_LOAD_RATIO = 0.25
QUIET_DISCOUNT = 5000
MAX_SUGGESTIONS = 3

# Q2 / A-04: straight-line distance; fee = hub base fee + rate per started kilometre.
MAX_DELIVERY_KM = 8.0
PER_KM_FEE = 3000

# Q4 / A-05: online options by customer type; everyone may pay cash on delivery.
ONLINE_OPTIONS = {
    CustomerType.LOCAL: (OnlineOption.E_WALLET, OnlineOption.BANK_QR),
    CustomerType.TOURIST: (OnlineOption.INTERNATIONAL_CARD,),
}

# A-12: no map service. A new address takes the centre of its district (former district names,
# as customers still use them). Approximate coordinates, good enough for a straight-line distance.
DISTRICTS: dict[str, tuple[float, float]] = {
    "District 1": (10.7756, 106.7019),
    "District 3": (10.7843, 106.6844),
    "District 4": (10.7579, 106.7013),
    "District 5": (10.7540, 106.6634),
    "District 7": (10.7340, 106.7215),
    "District 8": (10.7240, 106.6286),
    "District 10": (10.7731, 106.6679),
    "Binh Thanh": (10.8106, 106.7091),
    "Phu Nhuan": (10.7991, 106.6803),
    "Tan Binh": (10.8015, 106.6527),
    "Go Vap": (10.8387, 106.6653),
    "Thu Duc": (10.8494, 106.7537),
}

TERMINAL_ORDER_STATES = (OrderState.REJECTED, OrderState.CANCELLED, OrderState.DELIVERED,
                         OrderState.DELIVERY_FAILED)


def distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Raw Haversine km for decisions; round only in display/storage after checking."""
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(min(1.0, math.sqrt(a)))


def delivery_fee(base_fee: int, km: float) -> int:
    """Base fee plus PER_KM_FEE for every started kilometre (at least one)."""
    return base_fee + PER_KM_FEE * max(1, math.ceil(km))


def is_busy(load: int, capacity: int) -> bool:
    return load >= capacity


def is_quiet(load: int, capacity: int) -> bool:
    return load < capacity * QUIET_LOAD_RATIO


def quiet_discount(load: int, capacity: int, fee: int) -> int:
    return min(QUIET_DISCOUNT, fee) if is_quiet(load, capacity) else 0
