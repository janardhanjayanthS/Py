
# def promt_category() -> str | None:
#     """
#     prompts for category, if the category is invalid
#     it is called
#     """
#     category_dict = {
#         1: 'food',
#         2: 'transport',
#         3: 'entertainment',
#         4: 'utilities',
#         5: 'other'
#     }
#     for i, value in category_dict.items():
#         print(f'{i}. {value}')

#     while True:
#         try:
#             choice: int = int(input('Enter catergory 1 - 5'))
#             if choice in category_dict.keys():
#                 return category_dict[choice]
#             else:
#                 print('Enter a valid number from 1 to 5')
#         except ValueError:
#             print('Enter a valid number from 1 to 5')

# print(promt_category())

from datetime import datetime as dt

# current_date = dt.now().date()
# print(current_date, type(current_date), str(current_date))

date: str = input("Enter date in 'YYYY-MM-DD' format: ")
date_object: dt = dt.strptime(date, "%Y-%m-%d")
