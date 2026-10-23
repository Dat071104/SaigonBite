"""Frozen vocabulary shared by code, schema.sql and docs/part2.

Values are the exact strings stored in the database CHECK constraints.
"""
from enum import Enum


class OrderState(str, Enum):
    PLACED = "PLACED"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"
    PREPARING = "PREPARING"
    READY = "READY"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    DELIVERY_FAILED = "DELIVERY_FAILED"
    CANCELLED = "CANCELLED"


class PaymentMethod(str, Enum):
    COD = "COD"
    ONLINE = "ONLINE"   # team-built payment simulator (A-05, L2)


class OnlineOption(str, Enum):
    E_WALLET = "E_WALLET"
    BANK_QR = "BANK_QR"
    INTERNATIONAL_CARD = "INTERNATIONAL_CARD"


class PaymentState(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    VOIDED = "VOIDED"
    REFUND_PENDING = "REFUND_PENDING"
    REFUNDED = "REFUNDED"


class DeliveryState(str, Enum):
    AWAITING_PICKUP = "AWAITING_PICKUP"
    PICKED_UP = "PICKED_UP"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"


class OfferState(str, Enum):
    OFFERED = "OFFERED"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    WITHDRAWN = "WITHDRAWN"


class Role(str, Enum):
    CUSTOMER = "CUSTOMER"
    KITCHEN_STAFF = "KITCHEN_STAFF"
    SHIPPER = "SHIPPER"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"


class CustomerType(str, Enum):
    LOCAL = "LOCAL"
    TOURIST = "TOURIST"


class DiscountType(str, Enum):
    FIXED = "FIXED"
    PERCENT = "PERCENT"
