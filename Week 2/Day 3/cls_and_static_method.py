from __future__ import annotations


class Temperature:
    def __init__(self, celsius: float) -> None:
        """
        Intiializes a temrature in celsius
        Args:
            celsius: temperature in degree celcius
        Attributes:
            celsius: temperature in degree celcius
        """
        self.celsius: float = celsius

    @classmethod
    def from_fahrenheit(cls, fahrenheit: float) -> Temperature:
        degree_celsius: float = round((fahrenheit - 32) * (5 / 9), 2)
        return Temperature(celsius=degree_celsius)

    @staticmethod
    def is_freezing(celsius: float) -> bool:
        """
        Checks if temperature(param) is freezing
        Args:
            celsius: temperature in degree celcius
        Returns:
            True if temp is <= 0 else False
        """
        return True if celsius <= 0 else False


if __name__ == "__main__":
    c = Temperature(500)
    print(c.celsius)
    c1 = Temperature.from_fahrenheit(256)
    print(c1.celsius)
    is_cold = Temperature.is_freezing(-90)
    print(is_cold)
