"""Public controller interface for form values and request connection lifecycle.

Views import these contract types here; persistence construction remains below the
controller boundary. This does not grant DAOs an upward mapper exception.
"""
from saigonbite.business.domain import DiscountType, OnlineOption, PaymentMethod, Role, UserAccount, rules
from saigonbite.data_access import APPROVE, DECLINE, connect


def district_choices() -> list[tuple[str, str]]:
    return [(name, name) for name in rules.DISTRICTS]


def open_request_connection(path: str):
    return connect(path)
