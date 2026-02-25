class Bottle:
    def __init__(self, material: str, quantity: float, is_full=False) -> None:
        """
        Args:
            material: material which is used to make bottle
            quantity: liters of liquid the bottle can contian
            is_full: is the bottle ful?
        Attributes:
            material: material which is used to make bottle
            quantity: liters of liquid the bottle can contian
            is_full: default False, denotes is the bottle full
        """
        self.material: str = material
        self.quantity: float = quantity
        self.is_full: bool = is_full

    def display_information(self) -> None:
        """
        Prints Details about current bottle
        """
        print(
            f"Bottle is made up of {self.material} and can hold {self.quantity} liter(s) of contents"
        )

    def is_empty(self) -> bool:
        """
        checks if the bottle is empty
        Returns:
            True if bottle is empty else false
        """
        return True if not self.is_full else False


if __name__ == "__main__":
    b = Bottle(material="metal", quantity=1.5)
    b.display_information()
    print(f"is bottle empty: {b.is_empty()}")
