"""
Contains Abstract Factory Pattern implementation for Sofa example from: https://refactoring.guru/design-patterns/abstract-factory
"""

from abc import ABC, abstractmethod
from typing import Optional


# abstract products
class Chair(ABC):
    @abstractmethod
    def has_cushion(self) -> bool:
        pass

    @abstractmethod
    def leg_count(self) -> int:
        pass


class Sofa(ABC):
    @abstractmethod
    def cushion_type(self) -> str:
        pass

    @abstractmethod
    def seating_capacity(self) -> float:
        pass


class CoffeeTable(ABC):
    @abstractmethod
    def tabletop_material(self) -> str:
        pass

    @abstractmethod
    def is_tabletop_transparent(self) -> bool:
        pass


# Concrete products
class ArtDecoChair(Chair):
    def has_cushion(self) -> bool:
        return True

    def leg_count(self) -> int:
        return 4


class ArtDecoSofa(Sofa):
    def cushion_type(self) -> str:
        return "cotton"

    def seating_capacity(self) -> float:
        return 3.5


class ArtDecoCoffeTable(CoffeeTable):
    def tabletop_material(self) -> str:
        return "wood"

    def is_tabletop_transparent(self) -> bool:
        return False


class ModernChair(Chair):
    def has_cushion(self) -> bool:
        return False

    def leg_count(self) -> int:
        return 6


class ModernSofa(Sofa):
    def cushion_type(self) -> str:
        return "memory foam"

    def seating_capacity(self) -> float:
        return 6


class ModernCoffeTable(CoffeeTable):
    def tabletop_material(self) -> str:
        return "glass"

    def is_tabletop_transparent(self) -> bool:
        return True


# Abstract factory:
class Factory(ABC):
    @abstractmethod
    def create_chair(self) -> Chair:
        pass

    @abstractmethod
    def create_coffeetable(self) -> CoffeeTable:
        pass

    @abstractmethod
    def create_sofa(self) -> Sofa:
        pass


# Concrete Factory


class ModernFactory(Factory):
    def create_chair(self) -> Chair:
        return ModernChair()

    def create_sofa(self) -> Sofa:
        return ModernSofa()

    def create_coffeetable(self) -> CoffeeTable:
        return ModernCoffeTable()


class ArtDecoFactory(Factory):
    def create_chair(self) -> Chair:
        return ArtDecoChair()

    def create_sofa(self) -> Sofa:
        return ArtDecoSofa()

    def create_coffeetable(self) -> CoffeeTable:
        return ArtDecoCoffeTable()


# Example client -> this client knows only about the Abstract classes
#   (product/factory) never the concrete implementation


class TheClient:
    def __init__(self, factory: Factory) -> None:
        self.factory = factory
        self.chair: Optional[Chair] = None
        self.coffee_table: Optional[CoffeeTable] = None
        self.sofa: Optional[Sofa] = None

    def place_chair(self) -> None:
        if self.chair is None:
            self.chair = self.factory.create_chair()
        print(f"Placed chair - {self.chair} - here")

    def coffee_on_table(self) -> None:
        if self.coffee_table is None:
            self.coffee_table = self.factory.create_coffeetable()
            print(f"Created a new coffee table: {self.coffee_table}")

        print(f"Placed real hot coffee on: {self.coffee_table}")

    def get_sofa(self) -> Sofa:
        if self.sofa is None:
            self.sofa = self.factory.create_sofa()
        return self.sofa


# Usage examples:
def demonstrate_modern_furniture():
    """Demonstrate creating modern furniture using ModernFactory."""
    print("=== Modern Furniture Set ===")

    # Create modern factory
    modern_factory = ModernFactory()

    # Create and use modern furniture
    chair = modern_factory.create_chair()
    sofa = modern_factory.create_sofa()
    coffee_table = modern_factory.create_coffeetable()

    print(f"Chair has cushion: {chair.has_cushion()}")
    print(f"Chair leg count: {chair.leg_count()}")
    print(f"Sofa cushion type: {sofa.cushion_type()}")
    print(f"Sofa seating capacity: {sofa.seating_capacity()}")
    print(f"Coffee table material: {coffee_table.tabletop_material()}")
    print(f"Coffee table is transparent: {coffee_table.is_tabletop_transparent()}")
    print()


def demonstrate_artdeco_furniture():
    """Demonstrate creating Art Deco furniture using ArtDecoFactory."""
    print("=== Art Deco Furniture Set ===")

    # Create Art Deco factory
    artdeco_factory = ArtDecoFactory()

    # Create and use Art Deco furniture
    chair = artdeco_factory.create_chair()
    sofa = artdeco_factory.create_sofa()
    coffee_table = artdeco_factory.create_coffeetable()

    print(f"Chair has cushion: {chair.has_cushion()}")
    print(f"Chair leg count: {chair.leg_count()}")
    print(f"Sofa cushion type: {sofa.cushion_type()}")
    print(f"Sofa seating capacity: {sofa.seating_capacity()}")
    print(f"Coffee table material: {coffee_table.tabletop_material()}")
    print()


def demonstrate_client_usage():
    """Demonstrate how client uses the factory without knowing concrete types."""
    print("=== Client Usage Examples ===")

    # Client can work with any factory
    factories = [ModernFactory(), ArtDecoFactory()]
    styles = ["Modern", "Art Deco"]

    for factory, style in zip(factories, styles):
        print(f"\n--- {style} Style ---")
        client = TheClient(factory)

        # Client uses furniture without knowing concrete types
        sofa = client.get_sofa()
        print(f"Client got sofa with {sofa.cushion_type()} cushions")
        print(f"Sofa can seat {sofa.seating_capacity()} people")

        client.coffee_on_table()
        client.place_chair()


if __name__ == "__main__":
    print("Abstract Factory Pattern - Furniture Example")
    print("=" * 50)

    demonstrate_modern_furniture()
    demonstrate_artdeco_furniture()
    demonstrate_client_usage()
