"""ART 1: SCHEMA
----------------------

1. "genres" table

   - id: integer, primary key
   - name: string, NOT NULL, UNIQUE
   - Relationship: one genre has many books (ONE-TO-MANY)

2. "authors" table

   - id: integer, primary key
   - name: string, not null
   - country: string, nullable
   - Relationship: one author has many books (ONE-TO-MANY)
   - IMPORTANT: Since the CSV has no author data, generate 10 synthetic authors (real
     or invented names, each with a name and a country)

3. "tags" table

   - id: integer, primary key
   - name: string, not null, unique
   - IMPORTANT: Since the CSV has no tag data, generate 10 synthetic tags (e.g.
     "bestseller", "award-winning", "series", etc.)

4. "books" table

   - id: integer, primary key
   - title: string, not null
   - upc: string, not null, UNIQUE
   - genre_id: foreign key to genres.id, NOT NULL (every book has exactly
     one genre)
   - author_id: foreign key to authors.id, NOT NULL (every book gets an
     author assigned from your synthetic author list)


5. "book_details" table

   - id: integer, primary key
   - book_id: foreign key to books.id, NOT NULL, UNIQUE
   - rating: integer, not null ("One" -> 1, "Two" -> 2, ... "Five" -> 5)
   - price: float, not null
   - availability: integer, not null
   - Add check constraints enforcing: rating is between 1 and 5, price is
     non-negative, and availability is non-negative.

6. A "book_tags" join table

   - book_id: foreign key to books.id
   - tag_id: foreign key to tags.id

   - IMPORTANT: Each book should be assigned a random number of tags (anywhere from 0
     to 3) from your synthetic tag list.


PART 2: QUERYING
----------------------------

  1. List all books written by authors based in a specific country (e.g. Canada).
  2. List all books written by a specific named author.
  3. List all books ordered by price, highest first.
  4. List the 5 highest-rated books.
  5. List all books that have at least one tag.
  6. List all genres that are assigned to more than 5 books, along with
     each genre's book count.
  7. For every book, print the book's title along with its author's name
     and country.
  8. For every author, print their name and how many books they've
     written in this dataset, ordered from most to fewest (including
     authors with zero books, if any).
  9. For each genre, compute the total stock value (price x availability,
     summed across all books in that genre).
  10. For every book, print its title, genre name, and author name
      together in one row.
  11. For each genre that has at least one book, compute the average price
      of books in that genre.
  12. List all books that have more than one tag, along with their tag
      count.
  13. List any author who has written at least one book in EVERY genre
      present in the database (might be an empty result)

Notes:
  - Use func.count, func.sum, func.avg, and func.distinct from sqlalchemy
    for aggregate queries.
  - Query 13 should compute the total number of genres dynamically (don't
    hardcode the count), and should handle the case where no author
    satisfies the condition without crashing.
"""
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import create_engine, Float, Column, Integer, String, ForeignKey, CheckConstraint, Table

Base = declarative_base()

# Tabelul asociativ Many-to-Many pentru cărți și tag-uri
book_tags = Table(
    "book_tags",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)


class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    # Relație către cărți
    books = relationship("Book", back_populates="genre", cascade="all, delete-orphan")


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country = Column(String(50), nullable=True)

    # Relație către cărți
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    # Relație către cărți
    books = relationship("Book", secondary=book_tags, back_populates="tags")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    upc = Column(String, nullable=False, unique=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    # Relațiile mapate exact cum le apelezi în querying_tables.py
    genre = relationship("Genre", back_populates="books")
    author = relationship("Author", back_populates="books")
    detail = relationship("BookDetail", back_populates="book", uselist=False, cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=book_tags, back_populates="books")


class BookDetail(Base):
    __tablename__ = "book_details"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), unique=True, nullable=False)
    rating = Column(Integer, CheckConstraint("rating >= 1 AND rating <= 5"), nullable=False)
    price = Column(Float, CheckConstraint("price >= 0"), nullable=False)
    availability = Column(Integer, CheckConstraint("availability >= 0"), nullable=False)

    book = relationship("Book", back_populates="detail")


engine = create_engine('postgresql://postgres:admin@localhost/postgres')