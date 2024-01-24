class InvalidJsonlFile(Exception):
    """This exception signals that the a given file does not satisfy the jsonl specification."""

    pass


class InvalidDelimiterError(Exception):
    """The chosen delimiter is not valid."""
