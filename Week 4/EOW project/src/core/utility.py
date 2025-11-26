from csv import DictReader


def get_initial_product_data_from_csv(csv_filepath: str) -> dict[str, list]:
    """
    reads data from inventory.csv,
    adds rows from from csv to products table in postgres

    Args:
        csv_filepath: filepath for inventory.csv
    """
    initial_data: dict[str, list] = {'products': []}
    try:
        with open(csv_filepath) as file:
            reader = DictReader(file)
            for row in reader:
                initial_data['products'].append({
                    'id': row['product_id'],
                    'name': row['product_name'],
                    'quantity': row['quantity'],
                    'price': row['price'],
                    'type': row['type'],
                    'days_to_expire': row['days_to_expire'],
                    'is_vegetarian': row['is_vegetarian'],
                    'warranty_in_years': row['warranty_period_in_years']
                })
    except FileNotFoundError as e:
        print(f"Requested file {csv_filepath} does not exist. {e}")
    finally:
        return initial_data

