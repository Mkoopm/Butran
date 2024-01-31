class ButranException(Exception):
    """Base exception class for all custom exception to inherrit form."""


class InvalidJsonlFile(ButranException):
    """This exception signals that the a given file does not satisfy the jsonl specification."""


class InvalidDelimiterError(ButranException):
    """The chosen delimiter is not valid."""
