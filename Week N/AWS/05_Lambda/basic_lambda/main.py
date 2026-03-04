from random import choice


def get_random_drink() -> str:
    drinks = ["coffee", "tea", "water", "juice"]
    return choice(drinks)


if __name__ == "__main__":
    print(f"Random drink: {get_random_drink()}")
