"""Holds logic for core errors."""


class BaseError(Exception):
    """An error that occurred during validation."""

    pass


class BadRequest(BaseError):
    """Bad Request"""

    pass


class UnsupportedMediaTypeError(BaseError):
    """Invalid Media Type"""

    pass
