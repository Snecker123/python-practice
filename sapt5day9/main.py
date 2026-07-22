"""
FastAPI REST API for the bookstore database.

Reuses the SQLAlchemy models (Genre, Author, Tag, Book, BookDetail) defined
in ex.py -- they are imported directly, not redefined here.

Run with:
    uvicorn main:app --reload

Then open http://127.0.0.1:8000/docs to try the endpoints interactively.
"""

EX_PY_FOLDER = r"C:\Users\Raluca\PycharmProjects\PythonPractice\sapt4day8"

import sys
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session, sessionmaker

sys.path.insert(0, EX_PY_FOLDER)

# Import the already-defined models/engine instead of redefining the tables.
from ex import Author, Book, BookDetail, Genre, Tag, engine

app = FastAPI(title="Bookstore REST API")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

# ---- Genres / Authors / Tags (read-only) ----

class GenreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class AuthorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    country: Optional[str] = None


class TagOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


# ---- Books ----

class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    upc: str
    genre_id: int
    author_id: int


class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    upc: str = Field(min_length=1)
    genre_id: int
    author_id: int


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    upc: Optional[str] = Field(default=None, min_length=1)
    genre_id: Optional[int] = None
    author_id: Optional[int] = None


# ---- Book details ----

class BookDetailOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    book_id: int
    rating: int
    price: float
    availability: int


class BookDetailCreate(BaseModel):
    book_id: int
    rating: int = Field(ge=1, le=5)
    price: float = Field(ge=0)
    availability: int = Field(ge=0)


class BookDetailUpdate(BaseModel):
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    price: Optional[float] = Field(default=None, ge=0)
    availability: Optional[int] = Field(default=None, ge=0)


# ---------------------------------------------------------------------------
# HATEOAS helpers (bonus)
# ---------------------------------------------------------------------------

def book_to_hateoas(book: Book) -> dict:
    data = BookOut.model_validate(book).model_dump()
    data["_links"] = {
        "self": {"type": "GET", "href": f"/books/{book.id}"},
        "update": {"type": "PUT", "href": f"/books/{book.id}"},
        "delete": {"type": "DELETE", "href": f"/books/{book.id}"},
        "genre": {"type": "GET", "href": "/genres"},
        "author": {"type": "GET", "href": "/authors"},
        "details": {"type": "GET", "href": "/book-details"},
    }
    return data


def book_detail_to_hateoas(detail: BookDetail) -> dict:
    data = BookDetailOut.model_validate(detail).model_dump()
    data["_links"] = {
        "self": {"type": "GET", "href": f"/book-details/{detail.id}"},
        "delete": {"type": "DELETE", "href": f"/book-details/{detail.id}"},
        "book": {"type": "GET", "href": f"/books/{detail.book_id}"},
    }
    return data


# ---------------------------------------------------------------------------
# PART 1: BOOKS
# ---------------------------------------------------------------------------

@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return [book_to_hateoas(b) for b in books]


@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_to_hateoas(book)


@app.post("/books", status_code=201)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    genre = db.get(Genre, payload.genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    author = db.get(Author, payload.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    existing = db.query(Book).filter(Book.upc == payload.upc).first()
    if existing:
        raise HTTPException(status_code=409, detail="A book with this UPC already exists")

    book = Book(
        title=payload.title,
        upc=payload.upc,
        genre_id=payload.genre_id,
        author_id=payload.author_id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book_to_hateoas(book)


@app.put("/books/{book_id}")
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = payload.model_dump(exclude_unset=True)

    if "genre_id" in update_data:
        genre = db.get(Genre, update_data["genre_id"])
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")

    if "author_id" in update_data:
        author = db.get(Author, update_data["author_id"])
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")

    if "upc" in update_data:
        conflict = (
            db.query(Book)
            .filter(Book.upc == update_data["upc"], Book.id != book_id)
            .first()
        )
        if conflict:
            raise HTTPException(status_code=409, detail="A book with this UPC already exists")

    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book_to_hateoas(book)


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Book.detail relationship is configured with cascade="all, delete-orphan",
    # so deleting the book through the ORM session also deletes its book_details row.
    db.delete(book)
    db.commit()
    return None


# ---------------------------------------------------------------------------
# PART 2: BOOK DETAILS
# ---------------------------------------------------------------------------

@app.get("/book-details")
def get_book_details(db: Session = Depends(get_db)):
    details = db.query(BookDetail).all()
    return [book_detail_to_hateoas(d) for d in details]


@app.get("/book-details/{detail_id}")
def get_book_detail(detail_id: int, db: Session = Depends(get_db)):
    detail = db.get(BookDetail, detail_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Book detail not found")
    return book_detail_to_hateoas(detail)


@app.post("/book-details", status_code=201)
def create_book_detail(payload: BookDetailCreate, db: Session = Depends(get_db)):
    book = db.get(Book, payload.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    existing = db.query(BookDetail).filter(BookDetail.book_id == payload.book_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="This book already has a book_details entry")

    detail = BookDetail(
        book_id=payload.book_id,
        rating=payload.rating,
        price=payload.price,
        availability=payload.availability,
    )
    db.add(detail)
    db.commit()
    db.refresh(detail)
    return book_detail_to_hateoas(detail)


@app.put("/book-details/{detail_id}")
def update_book_detail(detail_id: int, payload: BookDetailUpdate, db: Session = Depends(get_db)):
    detail = db.get(BookDetail, detail_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Book detail not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(detail, field, value)

    db.commit()
    db.refresh(detail)
    return book_detail_to_hateoas(detail)


@app.delete("/book-details/{detail_id}", status_code=204)
def delete_book_detail(detail_id: int, db: Session = Depends(get_db)):
    detail = db.get(BookDetail, detail_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Book detail not found")

    db.delete(detail)
    db.commit()
    return None


# ---------------------------------------------------------------------------
# PART 3: GENRES, AUTHORS, TAGS (read-only)
# ---------------------------------------------------------------------------

@app.get("/genres", response_model=List[GenreOut])
def get_genres(db: Session = Depends(get_db)):
    return db.query(Genre).all()


@app.get("/authors", response_model=List[AuthorOut])
def get_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()


@app.get("/tags", response_model=List[TagOut])
def get_tags(db: Session = Depends(get_db)):
    return db.query(Tag).all()
