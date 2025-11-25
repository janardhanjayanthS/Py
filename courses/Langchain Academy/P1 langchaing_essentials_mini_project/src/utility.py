from json import load
from typing import Optional


def load_json(filepath: str) -> Optional[list[dict]]:
    """
    loads books data from .json file if book exists 
    else raises FileNotFoundError

    Args:
        filepath: filepath for json file

    Returns:
        Optional[list[dict]]: book data in list containing dict if book json exists

    Raises:
        FileNotFoundError: if .json is not existing in given filepath
    """
    try:
        with open(filepath, 'r') as json_file:
            return load(json_file)
    except FileNotFoundError as e:
        print(f'Unable to find {filepath}, error: {e}')
        return []
