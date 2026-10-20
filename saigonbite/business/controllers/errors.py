"""Business-rule errors raised by controllers. The View turns them into messages or HTTP codes."""


class BusinessError(Exception):
    """Base class. str(error) is the message shown to the user."""


class ValidationError(BusinessError):
    """Input breaks a rule (empty cart, bad quantity, unavailable item, missing address). No data is written."""


class AuthorizationError(BusinessError):
    """The user has no right to perform the operation (wrong role or not the owner)."""


class NotFoundError(BusinessError):
    """The requested record does not exist."""


class QuoteChangedError(BusinessError):
    """The re-priced total differs from the total the customer saw. No order is written;
    the View shows the new quote so the customer can confirm again."""

    def __init__(self, quote):
        super().__init__("The price changed since your quote. Please check the new total and confirm again.")
        self.quote = quote
