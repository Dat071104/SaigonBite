"""Business-rule errors raised by controllers. The View turns them into messages or HTTP codes."""


class BusinessError(Exception):
    """Base class. str(error) is the message shown to the user."""


class ValidationError(BusinessError):
    """Input breaks a rule (empty cart, bad quantity, unavailable item, missing address). No data is written."""


class AuthorizationError(BusinessError):
    """The user has no right to perform the operation (wrong role, wrong hub or not the owner)."""


class NotFoundError(BusinessError):
    """The requested record does not exist."""


class ConflictError(BusinessError):
    """The record is no longer in the state the page showed (another user acted first, or the same
    button was pressed twice). Nothing was written."""


class QuoteChangedError(BusinessError):
    """The re-priced total differs from the total the customer saw. No order is written;
    the View shows the new quote so the customer can confirm again."""

    CHANGED = "The price changed since your quote. Please check the new total and confirm again."
    MISSING = "We could not match this order to a quote. Please check the total and confirm again."

    def __init__(self, quote, message: str = CHANGED):
        super().__init__(message)
        self.quote = quote


class HubUnavailableError(BusinessError):
    """The chosen hub cannot take this order (busy kitchen or address out of range).
    suggestions lists other hubs that can, quietest first (HubStatus objects)."""

    def __init__(self, message: str, suggestions):
        super().__init__(message)
        self.suggestions = suggestions


class PaymentDeclinedError(BusinessError):
    """The online payment was declined. No order and no payment row were written (Payment FAILED is
    shown and logged only); the customer may try again or choose cash on delivery."""

    def __init__(self, quote, message: str):
        super().__init__(message)
        self.quote = quote
