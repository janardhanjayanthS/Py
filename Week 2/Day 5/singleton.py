from __future__ import annotations
from typing import Any


class Singleton(type):
    _instances = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            print(f'Creating object of: {cls.__name__}')
            cls._instances[cls] = super().__call__(*args, **kwds)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    def __init__(self) -> None:
        self.logfile_path = 'path/tp/logfile'

    def __str__(self) -> str:
        return f'path to log file: {self.logfile_path}'

    def log(self, message: str) -> None:
        if message:
            print(f'Logging - {message} - to {self.logfile_path}')
        else:
            raise Exception(f'Message: {message}, cannot be empty')

if __name__ == '__main__':
    l1 = Logger()
    l2 = Logger()

    print(l1 is l2)
    print(id(l1))
    print(id(l2))

    l1.log('this is a log message')
