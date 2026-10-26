"""AccountController (SUC-02 Register, edit profile, manage addresses).

    register        -> register(form)                    local: Vietnamese mobile; tourist: passport + e-mail
    viewProfile     -> get_profile(user_id)
    updateProfile   -> update_profile(user_id, form)
    addAddress      -> add_address(user_id, form)
    updateAddress   -> update_address(user_id, address_id, form)
    archiveAddress  -> archive_address(user_id, address_id)

The customer type is chosen at registration and does not change (it decides the payment options, Q4).
An archived address cannot be used for new orders; past orders keep their own copy of the address text.
"""
from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from typing import Mapping

from werkzeug.security import generate_password_hash

from saigonbite.business.domain import (Address, Customer, CustomerType, Role, UserAccount, make_customer, rules)
from saigonbite.data_access import CustomerDAO, immediate_transaction

from .common import BaseController
from .errors import AuthorizationError, NotFoundError, ValidationError

USERNAME = re.compile(r"^[a-z0-9_.]{3,30}$")
VN_MOBILE = re.compile(r"^0[35789][0-9]{8}$")
INTL_PHONE = re.compile(r"^\+?[0-9]{7,15}$")
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PASSPORT = re.compile(r"^[A-Z0-9]{6,12}$")


@dataclass
class Profile:
    user: UserAccount
    customer: Customer
    addresses: list[Address]


class AccountController(BaseController):
    def __init__(self, conn: sqlite3.Connection, clock=None):
        super().__init__(conn, clock)
        self.customers = CustomerDAO(conn)

    def register(self, form: Mapping[str, str]) -> UserAccount:
        username = (form.get("username") or "").strip().lower()
        if not USERNAME.match(username):
            raise ValidationError("Choose a username of 3 to 30 characters: small letters, digits, dot or underscore.")
        password = form.get("password") or ""
        if not (6 <= len(password) <= 72):
            raise ValidationError("The password must have 6 to 72 characters.")
        if password != (form.get("password_again") or ""):
            raise ValidationError("The two passwords are not the same.")
        try:
            customer_type = CustomerType(form.get("customer_type") or "")
        except ValueError:
            raise ValidationError("Please say whether you live in Vietnam or are visiting.") from None
        customer = make_customer(customer_type.value, id=0, user_id=0, full_name="")
        self._fill_customer(customer, form)

        with immediate_transaction(self.conn):
            if self.users.get_by_username(username) is not None:
                raise ValidationError(f"The username {username} is taken. Please choose another one.")
            user = UserAccount(id=0, username=username, password_hash=generate_password_hash(password),
                               display_name=customer.full_name, role=Role.CUSTOMER, created_at=self._now())
            user.id = self.users.insert(user)
            customer.user_id = user.id
            customer.id = self.customers.insert(customer)
        return user

    def get_profile(self, user_id: int) -> Profile:
        user, customer = self._require_customer(user_id)
        return Profile(user=user, customer=customer, addresses=self.customers.list_addresses(customer.id))

    def update_profile(self, user_id: int, form: Mapping[str, str]) -> Profile:
        with immediate_transaction(self.conn):
            user, customer = self._require_customer(user_id)
            if 'customer_type' in form and form['customer_type'] != customer.customer_type.value:
                raise ValidationError('The registered customer type cannot be changed.')
            self._fill_customer(customer, form)
            self.customers.update(customer)
            user.display_name = customer.full_name
            self.users.update(user)
        return self.get_profile(user_id)

    def add_address(self, user_id: int, form: Mapping[str, str]) -> Address:
        _, customer = self._require_customer(user_id)
        address = self._parse_address(form, customer.id, address_id=0)
        with immediate_transaction(self.conn):
            address.id = self.customers.insert_address(address)
        return address

    def update_address(self, user_id: int, address_id: int, form: Mapping[str, str]) -> Address:
        _, customer = self._require_customer(user_id)
        address = self._parse_address(form, customer.id, address_id=address_id)
        with immediate_transaction(self.conn):
            if not self.customers.update_address(address):
                raise NotFoundError("Address not found.")
        return address

    def archive_address(self, user_id: int, address_id: int) -> None:
        _, customer = self._require_customer(user_id)
        with immediate_transaction(self.conn):
            if not self.customers.archive_address(address_id, customer.id, self._now()):
                raise NotFoundError("Address not found.")

    # ---- internals ---------------------------------------------------------------------

    def _require_customer(self, user_id: int) -> tuple[UserAccount, Customer]:
        user = self._require_user(user_id, Role.CUSTOMER, message="Only customers have a profile here.")
        customer = self.customers.get_by_user_id(user.id)
        if customer is None:
            raise AuthorizationError("Only customers have a profile here.")
        return user, customer

    @staticmethod
    def _fill_customer(customer: Customer, form: Mapping[str, str]) -> None:
        """Validate the fields of the customer's type and copy them onto the customer."""
        full_name = (form.get("full_name") or "").strip()
        if not (2 <= len(full_name) <= 80):
            raise ValidationError("Please enter your full name (2 to 80 characters).")
        phone = re.sub(r"[\s.-]", "", form.get("phone") or "")
        customer.full_name = full_name
        if customer.customer_type is CustomerType.LOCAL:
            if not VN_MOBILE.match(phone):
                raise ValidationError("Enter a Vietnamese mobile number of 10 digits, for example 0901234567.")
            customer.phone, customer.email, customer.passport_no, customer.nationality = phone, None, None, None
            return
        email = (form.get("email") or "").strip()
        if not EMAIL.match(email) or len(email) > 120:
            raise ValidationError("Enter a valid e-mail address.")
        passport = (form.get("passport_no") or "").replace(" ", "").upper()
        if not PASSPORT.match(passport):
            raise ValidationError("Enter the passport number: 6 to 12 letters or digits.")
        nationality = (form.get("nationality") or "").strip()
        if not (2 <= len(nationality) <= 40):
            raise ValidationError("Please enter your nationality.")
        if phone and not INTL_PHONE.match(phone):
            raise ValidationError("The phone number may only contain digits and a leading +.")
        customer.phone, customer.email = phone or None, email
        customer.passport_no, customer.nationality = passport, nationality

    @staticmethod
    def _parse_address(form: Mapping[str, str], customer_id: int, address_id: int) -> Address:
        label = (form.get("label") or "").strip()
        if not (1 <= len(label) <= 30):
            raise ValidationError("Give the address a short name, such as Home, Office or Hotel.")
        full_address = (form.get("full_address") or "").strip()
        if not (5 <= len(full_address) <= 200):
            raise ValidationError("Enter the full address (street, number, building or hotel).")
        district = form.get("district") or ""
        if district not in rules.DISTRICTS:
            raise ValidationError("Please choose the district from the list.")
        lat, lon = rules.DISTRICTS[district]
        return Address(id=address_id, customer_id=customer_id, label=label, full_address=full_address,
                       district=district, latitude=lat, longitude=lon)
