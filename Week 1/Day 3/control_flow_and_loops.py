
def check_leap_year(year: int) -> bool:
    """
    Checks if the given year is a leap year or not
    Args: 
        year: year to check
    Returns:
        True if leap year else false
    """
    if ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0):
        return True
    return False

# print(check_leap_year(2000))
# print(check_leap_year(1900))
# print(check_leap_year(2020))
# print(check_leap_year(2023))


def get_age_group(age: int) -> str:
    """
    Classifies the give age into an age group
    Args:
        age: age to classify
    Returns:
        returns a specific age group corresponding to the
        given age
    """
    if age < 0:
        return 'invalid'
    elif age < 3:
        return 'infant'
    elif age < 13:
        return 'kid'
    elif age < 20:
        return 'teen'
    elif age < 80:
        return 'adult'
    else:
        return 'elder'

# print(get_age_group(14))
# print(get_age_group(22))
# print(get_age_group(50))
# print(get_age_group(-1))
# print(get_age_group(100))

# loops


listt: list[int] = [1, 2, 3, 4, 5]

for i in range(len(listt)):
    listt[i] **= 2

print(listt)


counter = 0

while counter < 10:
    print(counter)
    counter += 1

print('counter after while loop: ', counter)



