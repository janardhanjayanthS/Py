from abc import ABC, abstractmethod


class Price(ABC):
    @abstractmethod
    def get_amount(self) -> float:
        pass


class ConcretePrice(Price):
    def __init__(self, amount: float) -> None:
        self.amount: float = amount

    def get_amount(self) -> float:
        return self.amount


class Decorator(Price):
    def __init__(self, price: Price) -> None:
        self._price = price

    def get_amount(self) -> float:
        self._price.get_amount()


class TaxDecorator(Decorator):
    def __init__(self, price: Price, tax_percentage: float) -> None:
        super().__init__(price)
        self.tax_percentage = tax_percentage

    def get_amount(self) -> float:
        return self._price.get_amount() + (
            self._price.get_amount() * self.tax_percentage
        )


class DiscountDecorator(Decorator):
    def __init__(self, price: Price, discount_percentage: float) -> None:
        super().__init__(price)
        self.discount_percentage = discount_percentage

    def get_amount(self) -> float:
        return self._price.get_amount() - (
            self._price.get_amount() * self.discount_percentage
        )


if __name__ == "__main__":
    price_object = ConcretePrice(amount=200)
    print(price_object.get_amount())
    price_object = DiscountDecorator(price=price_object, discount_percentage=0.1)
    print(price_object.get_amount())
    price_object = TaxDecorator(price=price_object, tax_percentage=0.8)
    print(price_object.get_amount())
