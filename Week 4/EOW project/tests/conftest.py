from pathlib import Path

import pytest


@pytest.fixture
def get_csv_filepath() -> str:
    """
    Used to get csv filepath

    Returns:
        str: csv file path
    """
    return str(Path(__file__).parent.parent / "data/test_inventory.csv")
