from pathlib import Path

from utility import load_json

JSON_FILEPATH = str(Path(__file__).parent.parent) + "/data/books.json"

BOOK_DATA: list = load_json(JSON_FILEPATH)
