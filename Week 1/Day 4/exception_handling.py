

def divide(numerator: int | float, denomiator: int | float) -> None:
    """
    Divides numerator by denominator and prints the result if there are no errors
    """

    try:
        quotient = numerator / denomiator
    except ZeroDivisionError as e:
        print(f'Cannot divide a number by zero: {e}')
    except TypeError as e:
        print(f'The numerator and denominator values must be numbers: {e}')
    else:
        quotient = numerator / denomiator
        print(f'{numerator} divided by {denomiator} is {quotient}')
    finally:
        print('--x---')

divide(5, 3)
divide(5, 0)
# divide('b', 'a')
print(100, 20)
