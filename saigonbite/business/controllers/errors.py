"""Business-rule errors raised by controllers. The View turns them into messages or HTTP codes."""


class BusinessError(Exception):
    """Base class. str(error) is the message shown to the user."""


class ValidationError(BusinessError):
    """Input breaks a rule (empty cart, bad quantity, unavailable item, missing address). No data is written."""


class AuthorizationError(BusinessError):
    """The user has no right to perform the operation (wrong role or not the owner)."""


class NotFoundError(BusinessError):
    """The requested record does not exist."""
