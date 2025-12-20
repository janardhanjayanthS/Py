from pydantic import BaseModel


class BookInReadingList(BaseModel):
    """Represents a specific book and its daily reading goals within a list.

    This model tracks how many pages a user intends to read for a specific
    book, serving as a constituent part of a larger weekly reading plan.

    Attributes:
        title: The full title of the book.
        pages_per_day: The target number of pages to be read each day to
            stay on track.
    """

    title: str
    pages_per_day: int


class ReadingList(BaseModel):
    """Defines a structured weekly reading schedule.

    This model aggregates multiple books into a specific weekly timeframe,
    allowing for organized tracking of reading progress.

    Attributes:
        week: The numerical identifier for the week (e.g., 1, 2, 3).
        books: A collection of BookInReadingList objects associated
            with this specific week.
    """

    week: int
    books: list[BookInReadingList]

