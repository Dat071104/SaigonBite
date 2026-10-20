"""AC-9 (second sentence): docs/i1 use the same names as the code and the schema."""
import os
import re

import pytest

from init_db import ROOT, SCHEMA_PATH
from saigonbite.business.controllers import AuthController, PlaceOrderController
from saigonbite.business.domain import OrderState, PaymentMethod, PaymentState, Role
from saigonbite import data_access

DOCS = os.path.join(ROOT, "docs", "i1")
DOC_FILES = ["uc01_subset_description.md", "domain_model_v1.md", "order_state_machine_v1.md",
             "ssd_uc01_subset.md", "crud_inventory_v1.md", "activity_uc01_subset.md"]
AI_HEADER = "AI-assisted (Claude)"


def read(name):
    with open(os.path.join(DOCS, name), encoding="utf-8") as f:
        return f.read()


def schema_tables():
    sql = open(SCHEMA_PATH, encoding="utf-8").read()
    return re.findall(r"CREATE TABLE (\w+)", sql)


@pytest.mark.parametrize("name", DOC_FILES)
def test_T_DOC_01_every_doc_starts_with_the_ai_assisted_label(name):
    first_line = read(name).splitlines()[0]
    assert AI_HEADER in first_line


def test_T_DOC_02_state_machine_doc_names_every_order_and_payment_state():
    doc = read("order_state_machine_v1.md")
    for state in list(OrderState) + list(PaymentState) + list(PaymentMethod):
        assert f"`{state.value}`" in doc or state.value in doc, state
    assert "ALLOWED_TRANSITIONS" in doc


def test_T_DOC_03_crud_doc_names_every_schema_table_and_every_dao():
    doc = read("crud_inventory_v1.md")
    for table in schema_tables():
        assert f"`{table}`" in doc, table
    for dao in ("HubDAO", "CustomerDAO", "UserDAO", "OrderDAO", "PaymentDAO"):
        assert f"`{dao}`" in doc and hasattr(data_access, dao)


def test_T_DOC_04_domain_doc_names_every_table_and_domain_class():
    doc = read("domain_model_v1.md")
    for table in schema_tables():
        assert f"`{table}`" in doc, table
    for cls in ("UserAccount", "Customer", "LocalCustomer", "TouristCustomer", "Address", "Hub", "Brand",
                "MenuItem", "HubMenuItem", "Order", "OrderLine", "Payment"):
        assert cls in doc


def test_T_DOC_05_ssd_doc_lists_the_controller_methods_that_exist():
    doc = read("ssd_uc01_subset.md")
    for target in ("PlaceOrderController.list_hubs", "PlaceOrderController.select_hub",
                   "PlaceOrderController.request_quote", "PlaceOrderController.confirm_order",
                   "PlaceOrderController.get_confirmation", "AuthController.authenticate"):
        assert f"`{target}`" in doc, target
        cls_name, method = target.split(".")
        cls = {"PlaceOrderController": PlaceOrderController, "AuthController": AuthController}[cls_name]
        assert callable(getattr(cls, method))


def test_T_DOC_06_uc_description_uses_the_schema_names_and_roles():
    doc = read("uc01_subset_description.md")
    for name in ("orders", "order_line", "payment", "idempotency_token", "delivery_fee_flat",
                 "hub_menu_item", "`PLACED`", "`COD`", "`PENDING`", f"`{Role.CUSTOMER.value}`"):
        assert name in doc, name
    for pre in ("PRE-01", "POST-01", "POST-F1", "E-01"):
        assert pre in doc
