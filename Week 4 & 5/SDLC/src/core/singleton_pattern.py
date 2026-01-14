from typing import Any


class Singleton(type):
    """Metaclass that ensures only one instance of each class exists.

    Implements the singleton pattern by maintaining a registry of instances
    and returning the existing instance when a class is instantiated multiple times.
    """

    _instances = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Control instance creation to enforce singleton pattern.

        Args:
            *args: Positional arguments for class constructor.
            **kwargs: Keyword arguments for class constructor.

        Returns:
            The singleton instance of the class.
        """
        if cls not in cls._instances:
            print(f"creating instance of {cls.__name__}")
            cls._instances[cls] = super().__init__(*args, **kwargs)
        return cls._instances[cls]
