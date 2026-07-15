import csv
import random
import re
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Float, Column, Integer, String, ForeignKey, CheckConstraint, Table

Base = declarative_base()


# --- 1. SCHEMAS AND MODELS ---

class Genres(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country = Column(String(50), nullable=True)


class tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    upc = Column(String, nullable=False, unique=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)


class Book_Details(Base):
    __tablename__ = "book_details"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), unique=True, nullable=False)
    rating = Column(Integer, CheckConstraint("rating >= 1 AND rating <= 5"), nullable=False)
    price = Column(Float, CheckConstraint("price >= 0"), nullable=False)
    availability = Column(Integer, CheckConstraint("availability >= 0"), nullable=False)


# A "book_tags" join table (Part 1, #6)
book_tags = Table(
    "book_tags",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

# --- 2. ENGINE SETUP AND GENERATION ---

engine = create_engine('postgresql://postgres:admin@localhost/postgres')
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# --- 3. SEED SYNTHETIC DATA ---

# Generate 10 synthetic authors
authors_data = [
    {"name": f"Author {i}", "country": "Canada" if i % 3 == 0 else "USA"}
    for i in range(1, 11)
]
session.execute(Author.__table__.insert(), authors_data)
session.commit()

# Retrieve generated author IDs
author_ids = [r[0] for r in session.query(Author.id).all()]

# Generate 10 synthetic tags
tags_list = ["bestseller", "award-winning", "series", "classic", "recommended",
             "must-read", "popular", "trending", "new-release", "choice"]
tags_data = [{"name": name} for name in tags_list]
session.execute(tags.__table__.insert(), tags_data)
session.commit()

# Retrieve generated tag IDs
tag_ids = [r[0] for r in session.query(tags.id).all()]

# --- 4. PARSE CSV AND INSERT BOOKS ---

csv_file_path = r"C:\Users\Raluca\PycharmProjects\PythonPractice\sapt4day7\books.csv"

with open(csv_file_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    genre_cache = {}

    for row in reader:
        # Look up or insert Genre dynamically
        genre_name = row['genre']
        if genre_name not in genre_cache:
            res = session.execute(Genres.__table__.insert().values(name=genre_name).returning(Genres.id))
            genre_cache[genre_name] = res.scalar()

        # Assign a random synthetic author ID
        assigned_author_id = random.choice(author_ids)

        # Insert Book row
        book_res = session.execute(
            Book.__table__.insert().values(
                title=row['title'],
                upc=row['upc'],
                genre_id=genre_cache[genre_name],
                author_id=assigned_author_id
            ).returning(Book.id)
        )
        new_book_id = book_res.scalar()

        # Extract integer count from availability string "In stock (X available)"
        avail_match = re.search(r'\d+', row['availability'])
        avail_count = int(avail_match.group()) if avail_match else 0

        # Insert Book_Details row
        session.execute(
            Book_Details.__table__.insert().values(
                book_id=new_book_id,
                rating=int(row['rating']),
                price=float(row['price']),
                availability=avail_count
            )
        )

        # Assign a random number of tags (0 to 3) to the book
        num_tags = random.randint(0, 3)
        chosen_tags = random.sample(tag_ids, num_tags)
        for t_id in chosen_tags:
            session.execute(book_tags.insert().values(book_id=new_book_id, tag_id=t_id))

session.commit()
print("Seeding Complete!")
