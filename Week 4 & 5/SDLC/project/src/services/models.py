from enum import Enum


class ResponseStatus(str, Enum):
    """
    Response status enum

    Attributes:
        S: success string
        E: error string
    """

    S = "success"
    E = "error"
