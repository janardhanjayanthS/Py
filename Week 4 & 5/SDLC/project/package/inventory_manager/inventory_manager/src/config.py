from __future__ import annotations
from typing import Any


class Singleton(type):
    _instances = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            print(f'Creating object of: {cls.__name__}')
            cls._instances[cls] = super().__call__(*args, **kwds)
        return cls._instances[cls]


class ConfigLoader(metaclass=Singleton):
    def __init__(self) -> None:
        self.low_quantity_threshold = 10

    def get_low_quality_threshold(self) -> int:
        return self.low_quantity_threshold
