import json
import os
import random
import uuid
from typing import Literal, Optional
from uuid import uuid4

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from log import correlation_id, get_logger
from mangum import Mangum
from pydantic import BaseModel
from utility import lifespan

app = FastAPI(lifespan=lifespan)
handler = Mangum(app)


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


@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    """Middleware for logging requests with correlation IDs.

    Args:
        request: Incoming HTTP request.
        call_next: Next middleware in the chain.

    Returns:
        HTTP response with correlation ID tracking.
    """
    request_id = str(uuid.uuid4())
    token = correlation_id.set(request_id)

    logger.info("Request started", path=request.url.path, method=request.method)

    try:
        response = await call_next(request)
        return response
    finally:
        correlation_id.reset(token)


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

