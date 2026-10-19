"""Frozen vocabulary shared by code, schema.sql and docs/i1 (AC-9).

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
    ONLINE = "ONLINE"   # team-built stub, not used before Iteration 3


class PaymentState(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    VOIDED = "VOIDED"
    REFUND_PENDING = "REFUND_PENDING"


class Role(str, Enum):
    CUSTOMER = "CUSTOMER"
    KITCHEN_STAFF = "KITCHEN_STAFF"
    SHIPPER = "SHIPPER"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"


class CustomerType(str, Enum):
    LOCAL = "LOCAL"
    TOURIST = "TOURIST"
