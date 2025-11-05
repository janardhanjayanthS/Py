from datetime import datetime as dt
from helpers import Expense


def prompt_amount() -> int | float:
    """
    Prompt for amount
    """
    while True:
        try:
            amount: int | float = float(input('Enter amount: '))
            if amount > 0:
                return amount
            else:
                print('value of amount should not be 0 or negative')
        except ValueError:
            print('Enter a valid integer/float value for amount')


def promt_category() -> str:
    """
    prompts for category
    """
    category_dict = {
        1: 'food',
        2: 'transport',
        3: 'entertainment',
        4: 'utilities',
        5: 'other'
    }
    for i, value in category_dict.items():
        print(f'{i}. {value}')

    while True:
        try:
            choice: int = int(input('Enter catergory 1 - 5: '))
            if choice in category_dict.keys():
                return category_dict[choice]
            else:
                print('Enter a valid number from 1 to 5: ')
        except ValueError:
            print('Enter a valid number from 1 to 5: ')

def prompt_date() -> str:
    """
    prompts for date in 'YYYY-MM-DD' format
    """
    while True:
        date: str = input("Enter date in 'YYYY-MM-DD' format: ")
        try:
            date_object: dt = dt.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print('Enter valid date')

def prompt_recurrance():
    """
    prompt for recurrence either True or False
    """
    while True:
        recurrance_choice: str = input('Is the expense recurrance: Y-yes/N-no: ').upper()
        if recurrance_choice in {'Y', 'N'}:
            return True if recurrance_choice == 'Y' else False
        else:
            print('Enter a valid choice between Y for yes or N for no')

def print_expense_message(expense: Expense):
    """
    Returns a formatted string for displaying an expense
    Retruns:

    """
    print('-----')
    print(f'Expense Description: {expense.description} \nExpense Amount: {expense.amount} \nExpense category: {expense.category} \nExpense date: {expense.date} \nExpense recurrance: {expense.is_recurring}')
    print('-----')