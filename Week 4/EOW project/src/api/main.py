from csv import DictReader

from ..models.models import Product


def csv_to_db(csv_filepath: str):
    """
    reads data from inventory.csv,
    adds rows from from csv to products table in postgres

    Args:
        csv_filepath: filepath for inventory.csv
    """
    try:
        with open(csv_filepath) as file:
            reader = DictReader(file)
            for row in reader:
                print(row)
    except FileNotFoundError as e:
        print(f"Requested file {csv_filepath} does not exist. {e}")


csv_to_db("/home/bitcot/python/Week 2/Day 6/package/new_inventory.csv")
