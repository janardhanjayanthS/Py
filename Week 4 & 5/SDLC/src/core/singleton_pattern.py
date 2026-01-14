from typing import Any


class Singleton(type):
    _instances = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            print(f"creating instance of {cls.__name__}")
            cls._instances[cls] = super().__init__(*args, **kwargs)
        return cls._instances[cls]
