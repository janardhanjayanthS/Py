import json
import os
import random
from typing import Literal, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from log import get_logger
from mangum import Mangum
from pydantic import BaseModel

logger = get_logger(__name__)


class Book(BaseModel):
    name: str
    genre: Literal["fiction", "non-fiction"]
    price: float
    book_id: Optional[str] = uuid4().hex


BOOKS_FILE = "books.json"
BOOKS = []

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        BOOKS = json.load(f)

app = FastAPI()
handler = Mangum(app)


@app.get("/")
async def root():
    logger.info("Hit root endpoint!!!")
    return {"message": "Welcome to my bookstore app!"}


@app.get("/random-book")
async def random_book():
    logger.info("returning a random books")
    return random.choice(BOOKS)


@app.get("/list-books")
async def list_books():
    logger.info("listing all books")
    return {"books": BOOKS}


@app.get("/book_by_index/{index}")
async def book_by_index(index: int):
    if index < len(BOOKS):
        logger.info("Book index found")
        return BOOKS[index]
    else:
        logger.error("Book index out of range")
        raise HTTPException(404, f"Book index {index} out of range ({len(BOOKS)}).")


@app.post("/add-book")
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOKS.append(json_book)

    with open(BOOKS_FILE, "w") as f:
        json.dump(BOOKS, f)

    logger.info("Book added successfully to JSON file")

    return {"book_id": book.book_id}


@app.get("/get-book")
async def get_book(book_id: str):
    for book in BOOKS:
        if book.book_id == book_id:
            logger.info(f"Book with {book_id} found successfully")
            return book

    logger.error(f"Book with {book_id} not found")
    raise HTTPException(404, f"Book ID {book_id} not found in database.")
