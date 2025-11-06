from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        """
        Calculates area for a shape
        """
        pass


class Square(Shape):
    def __init__(self, side: float) -> None:
        """
        Args:
            side: lenght of side of a square
        Attributes:
            side: lenght of side of a square
        """
        super().__init__()
        self.side: float = side

    def area(self) -> float:
        return self.side**2


class rectangel(Shape):
    def __init__(self, length: float, width: float) -> None:
        """
        Args:
            length: length of longer side of rectangle
            width: length of shorted side of rectangle
        Attributes:
            length: length of longer side of rectangle
            width: length of shorted side of rectangle
        """
        super().__init__()
        self.lenght = length
        self.width = width

    def area(self) -> float:
        return self.lenght * self.width


class Triangle(Shape):
    def __init__(self, height, base) -> None:
        """
        Args:
            height: height of triangle
            base: length of base of rectangle
        Attributes:
            height: height of triangle
            base: length of base of rectangle
        """
        super().__init__()
        self.height = height
        self.base = base

    def area(self) -> float:
        return (self.base * self.height) / 2


if __name__ == "__main__":
    square_5 = Square(side=5)
    rectangle = rectangel(length=10, width=7)
    triangle = Triangle(height=15, base=1000)
    shapes = [square_5, rectangle, triangle]
    
    for shape in shapes:
        print(f'Area of {shape.__class__.__name__} with dimensions {shape.__dict__} is {shape.area()} units')