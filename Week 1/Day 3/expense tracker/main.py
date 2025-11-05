

from csv_utility import append_expense, get_expenses
from helpers import Expense
from prompts import *



def add_expense():
    """
    add a new expense to csv file
    """
    print('New expense details')
    description: str = input('Enter description: ')
    amount: int | float = prompt_amount()
    category: str = promt_category()
    date: str = prompt_date()
    is_recurring: bool = prompt_recurrance()
    print('Expense information')
    print(description)
    print(amount)
    print(category)
    print(date)
    print(is_recurring)
    append_expense(
        Expense(
            description=description,
            amount=amount,
            category=category,
            date=date,
            is_recurring=is_recurring
    ))


def display_expense():
    """
    Displays all the expenses that are stored in expenses.csv file
    """    
    expenses = get_expenses()
    if expenses:
        for expense in expenses:
            print_expense_message(Expense(
                description=expense['description'],
                amount=expense['amount'],
                category=expense['category'],
                date=expense['date'],
                is_recurring=expense['is_recurring']
            ))
    else:
        print('There are no expenses')

    

if __name__ == '__main__':
    
    while True:
        print('Expense Tracker: ')
        print('1. Add Expense')
        print('2. Display all expenses')

        choice = int(input('Enter Your choice from 1 to 3: '))

        if choice == 1:
            add_expense()  
        elif choice == 2:
            display_expense()       
        elif choice == 3:
            break
        else:
            print('Enter a valid choice between 1 and 3!') 