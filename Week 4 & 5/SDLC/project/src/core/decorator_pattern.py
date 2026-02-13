from abc import ABC, abstractmethod


class Price(ABC):
    """Abstract base class for price calculations."""

    @abstractmethod
    def get_amount(self) -> float:
        """Calculate and return the price amount.

        Returns:
            Calculated price amount.
        """


class ConcretePrice(Price):
    """Concrete implementation of base price."""

    def __init__(self, amount: float) -> None:
        """Initialize with base amount.

        Args:
            amount: Base price amount.
        """
        self.amount: float = amount

    def get_amount(self) -> float:
        """Return the base amount.

        Returns:
            Base price amount.
        """


class Decorator(Price):
    """Base decorator class for price modifications."""

    def __init__(self, price: Price) -> None:
        """Initialize with price to decorate.

        Args:
            price: Price object to decorate.
        """
        self._price = price

    def get_amount(self) -> float:
        """Delegate to decorated price.

        Returns:
            Decorated price amount.
        """


class TaxDecorator(Decorator):
    """Decorator that adds tax to the base price."""

    def __init__(self, price: Price, tax_percentage: float) -> None:
        """Initialize with tax rate.

        Args:
            price: Base price to decorate.
            tax_percentage: Tax rate as decimal (e.g., 0.1 for 10%).
        """
        super().__init__(price)
        self.tax_percentage = tax_percentage

    def get_amount(self) -> float:
        """Calculate price with tax.

        Returns:
            Price amount including tax.
        """
        return self._price.get_amount() + (
            self._price.get_amount() * self.tax_percentage
        )


class DiscountDecorator(Decorator):
    """Decorator that applies discount to the base price."""

    def __init__(self, price: Price, discount_percentage: float) -> None:
        """Initialize with discount rate.

        Args:
            price: Base price to decorate.
            discount_percentage: Discount rate as decimal (e.g., 0.1 for 10%).
        """
        super().__init__(price)
        self.discount_percentage = discount_percentage

    def get_amount(self) -> float:
        """Calculate price with discount.

        Returns:
            Price amount after discount.
        """
        return self._price.get_amount() - (
            self._price.get_amount() * self.discount_percentage
        )
