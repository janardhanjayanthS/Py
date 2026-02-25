# Scope

# 1
# x = "global x"

# def outer():
#     x = "outer x"

#     def inner():
#         x = "inner x"
#         print("Inside inner():", x)

#     inner()
#     print("Inside outer():", x)

# outer()
# print("In global scope:", x)




# 2:
# x = "global x"

# def outer():
#     # global x
#     x = "outer x"

#     def inner():
#         # nonlocal x
#         # x = "changed by inner()"
#         print("Inside inner():", x)

#     inner()
#     print("Inside outer():", x)

# outer()
# print("In global scope:", x)


# args and kwargs

def sum_numbers(*args):
    """
    Returns the sum of all the numbers in *args
    """
    print(args, type(args))
    result = 0
    for number in args:
        result += number

    return result

# print(sum_numbers(1))
# print(sum_numbers(1, 3, 5, 6, 7, 65))



def display(**kwargs):
    """
    Displays contents from **kwargs
    """
    print(type(kwargs))
    for key, value in kwargs.items():
        print(f'{key}: {value}')



display(name='Lenovo', color='matt black', model='thinkpad e16 gen3', processor='core ultra 7 255h')
