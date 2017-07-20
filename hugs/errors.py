class HugsError(Exception):
    """Base class for errors raised by Hugs.
    """


class ParseError(HugsError):
    """Raised when a syntax error is encountered during parsing.
    """
