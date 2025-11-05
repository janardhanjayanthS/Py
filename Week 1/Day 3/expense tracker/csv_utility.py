import csv

from helpers import Expense

def append_expense(expense: Expense):
    """
    append values to csv file: expenses.csv
    """
    with open('expenses.csv', 'a') as csv_file:
        headers = ['description', 'amount', 'category', 'date', 'is_recurring']
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writerow({
            'description': expense.description,
            'amount': expense.amount,
            'category': expense.category,
            'date': expense.date,
            'is_recurring': expense.is_recurring
        })
    print('Successfully appended to csv file')


def get_expenses() -> list[dict[str, str]] | None:
    """
    This function gets all the expenses stored in the expenses.csv file 
    and returns them as a list
    Returns:
        expenses: List containing dict for each expense
    """ 
    expenses: list[dict[str, str]] = []
    with open('expenses.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            expenses.append(row)
    return expenses