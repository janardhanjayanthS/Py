from csv import DictReader


def read_file(filename: str):
    """
    Reads data from csv file
    Args:
        filename: csv file to read
    """
    try: 
        with open(filename, 'r') as csv_file:
            reader = DictReader(csv_file)
            for row in reader:
                print(row)
    except FileNotFoundError as e:
        print(f'File not found {e}')


if __name__ == '__main__':
    read_file('inventory.csv')