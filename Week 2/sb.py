from datetime import timedelta, datetime
from pydantic import BaseModel



diff = datetime.now() - timedelta(days=10)
str_diff = datetime.strftime(diff, "%d-%m-%Y")
# print(diff, type(diff))
# print(str_diff, type(str_diff))

class Sample(BaseModel):
    name: str


if __name__ == '__main__':
    s = Sample(name='yelp')
    print(s)
    print(type(s))
    