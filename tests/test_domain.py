"""Order state machine v1 (domain). I1 only creates PLACED; the other transitions are the planned ones."""
import pytest

from saigonbite.business.domain import (ALLOWED_TRANSITIONS, InvalidTransition, Order, OrderLine,
                                        OrderState)


def _order(state=OrderState.PLACED):
    return Order(customer_id=1, hub_id=1, address_id=1, state=state, delivery_fee=15000,
                 idempotency_token="t", placed_at="2026-10-19T00:00:00+00:00",
                 lines=[OrderLine(1, "A", 10000, 3)])


def test_T_DOM_01_every_state_has_an_entry_in_the_transition_table():
    assert set(ALLOWED_TRANSITIONS) == set(OrderState)


def test_T_DOM_02_happy_path_placed_to_delivered():
    order = _order()
    for nxt in (OrderState.CONFIRMED, OrderState.PREPARING, OrderState.READY,
                OrderState.OUT_FOR_DELIVERY, OrderState.DELIVERED):
        order.move_to(nxt)
    assert order.state is OrderState.DELIVERED


@pytest.mark.parametrize("terminal", [OrderState.REJECTED, OrderState.DELIVERED,
                                      OrderState.DELIVERY_FAILED, OrderState.CANCELLED])
def test_T_DOM_03_terminal_states_allow_no_transition(terminal):
    order = _order(terminal)
    for target in OrderState:
        assert not order.can_move_to(target)


def test_T_DOM_04_invalid_transition_raises_and_keeps_the_state():
    order = _order()
    with pytest.raises(InvalidTransition):
        order.move_to(OrderState.DELIVERED)
    assert order.state is OrderState.PLACED


def test_T_DOM_05_order_total_is_lines_plus_delivery_fee():
    order = _order()
    assert order.item_subtotal == 30000 and order.total == 45000


@pytest.mark.parametrize("start,allowed", [(OrderState.PLACED, True), (OrderState.CONFIRMED, True),
                                           (OrderState.PREPARING, False), (OrderState.READY, False)])
def test_T_DOM_05_customer_may_cancel_only_before_cooking_starts(start, allowed):
    assert _order(start).can_move_to(OrderState.CANCELLED) is allowed
