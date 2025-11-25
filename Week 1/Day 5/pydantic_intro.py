from pydantic import BaseModel, PositiveFloat, Field
from datetime import datetime as dt


class Book(BaseModel):
    title: str
    author: str
    price: PositiveFloat
    published_year: int = Field(
        ge=1900,
        le=dt.now().year,
        description="published year must be between 1900 and current year"
    )
    in_stock: bool
    isbn: str = Field(
        max_length=13,
        min_length=13
    )

    def info(self):
        return f'{self.title} by {self.author} ({self.published_year})'

class Library(BaseModel):
    name: str
    books: list[Book]


if __name__ == '__main__':
    book1 = Book(
        title='Meditations',
        author="Marcus Aurelius",
        price=150.00,
        published_year="1901",
        in_stock=True,
        isbn="8i8iuy6t5r4ed"
    )

    # book_inv = Book(
    #     title='Beyond good and evil',
    #     author="Marcus Aurelius",
    #     price='2000',
    #     published_year=1800,
    #     in_stock=True
    # )


    # book2 = Book(
    #     title='Ikigai',
    #     author="Hector Gracia and Fransec Miralles",
    #     price='99',
    #     published_year=1999,
    #     in_stock=False,
    #     isbn="66666"
    # )

    library = Library(
        name="Central Library",
        books=[
            book1,
            # book2,
            # book_inv
        ]
    )

    print(book1)
    print(book1.info())
