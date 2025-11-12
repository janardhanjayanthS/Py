from datetime import timedelta, datetime
from enum import Enum
from pydantic import BaseModel


diff = datetime.now() - timedelta(days=10)
str_diff = datetime.strftime(diff, "%d-%m-%Y")
# print(diff, type(diff))
# print(str_diff, type(str_diff))


class Sample(BaseModel):
    name: str


# class syntax
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

    @classmethod
    def get_values(cls) -> list:
        return [enum.value for enum in cls]


if __name__ == "__main__":
    # s = Sample(name="yelp")
    # print(s)
    # print(type(s))
    print(Color)
    print(Color.get_values())
