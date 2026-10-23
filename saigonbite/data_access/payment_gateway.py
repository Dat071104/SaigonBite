"""Team-built payment simulator (A-05, lecturer question L2). Not a real payment provider.

It stands in for the external payment provider so both branches of online payment can be tested:
the customer presses "Approve" or "Decline" on the simulator page, and the outcome comes back here.
No card number or wallet credential is ever asked for or stored.

authorise() returns a reference when the payment is approved. The controller then saves the order in
one transaction (A-06: the money is taken when the order is saved); if the save fails, release()
cancels the authorisation so no money is taken.
"""
from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from typing import Optional

from saigonbite.business.domain import OnlineOption

log = logging.getLogger("saigonbite.payment")

APPROVE = "APPROVE"
DECLINE = "DECLINE"


@dataclass
class Authorisation:
    approved: bool
    reference: Optional[str]
    message: str


class PaymentGatewaySimulator:
    def authorise(self, amount: int, option: OnlineOption, outcome: str) -> Authorisation:
        if outcome == APPROVE:
            ref = f"SIM-{uuid.uuid4().hex[:12].upper()}"
            log.info("payment simulator: authorised %s VND by %s, ref %s", amount, option.value, ref)
            return Authorisation(True, ref, "Approved")
        log.info("payment simulator: declined %s VND by %s (FAILED, no order created)", amount, option.value)
        return Authorisation(False, None, "The payment was declined.")

    def release(self, reference: str) -> None:
        log.info("payment simulator: authorisation %s released, no money taken", reference)
