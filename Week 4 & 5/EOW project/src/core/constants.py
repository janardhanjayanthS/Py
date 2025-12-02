from enum import Enum
from pathlib import Path

INVENTORY_CSV_FILEPATH = str(
    (Path(__file__).parent.parent.parent / "data" / "new_inventory.csv")
)


class ResponseStatus(Enum):
    """
    Response status enum

    Attributes:
        S: success string
        E: error string
    """

    S: str = "success"
    E: str = "error"
