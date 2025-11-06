from datetime import timedelta, datetime



diff = datetime.now() - timedelta(days=10)
str_diff = datetime.strftime(diff, "%d-%m-%Y")
print(diff, type(diff))
print(str_diff, type(str_diff))