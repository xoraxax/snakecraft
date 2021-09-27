class SnakeCraftException(Exception):
    pass


class DuplicateDeclarationException(SnakeCraftException):
    """Raised when a name was duplicated."""


class TwoAnonymousNames(DuplicateDeclarationException):
    """Raised when the anonymous instantiation was done twice."""


class IncompatibleProviderConfiguration(SnakeCraftException):
    """Raised when two providers aliases are created that are both (differently) configured."""
