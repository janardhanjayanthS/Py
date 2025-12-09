from pydantic import BaseModel

class BookInReadingList(BaseModel):
    title: str  
    pages_per_day: int

class ReadingList(BaseModel):
    week: int
    books: list[BookInReadingList]