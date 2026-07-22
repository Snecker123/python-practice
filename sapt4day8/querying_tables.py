from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ex import Genre, Author, Tag, Book, BookDetail

engine = create_engine('postgresql://postgres:admin@localhost/postgres')
Session = sessionmaker(bind=engine)
session = Session()

print("1. Books written by authors based in Canada")
canadian_authors_books = session.query(Book).join(Book.author).filter(Author.country == 'Canada').all()
for book in canadian_authors_books:
    print(f"Book by a Canadian author: {book.title}")

print("\n==============================================\n")

print("2. Books written by 'Neil Gaiman'")
gaiman_books = session.query(Book).join(Book.author).filter(Author.name == 'Neil Gaiman').all()
for book in gaiman_books:
    print(f"Gaiman book: {book.title}")

print("\n==============================================\n")

print("3. Books ordered by price descending")
books_by_price = (
    session.query(Book, BookDetail)
    .join(Book.detail)
    .order_by(desc(BookDetail.price))
    .all()
)
for book, detail in books_by_price:
    print(f"{book.title}: ${detail.price:.2f}")

print("\n==============================================\n")

print("4. Top 5 highest-rated books")
top_rated = (
    session.query(Book, BookDetail)
    .join(Book.detail)
    .order_by(desc(BookDetail.rating))
    .limit(5)
    .all()
)
for book, detail in top_rated:
    print(f"{book.title} - rating {detail.rating}")

print("\n==============================================\n")

print("5. Books that have at least one tag")
tagged_books = session.query(Book).filter(Book.tags.any()).all()
for book in tagged_books:
    print(f"Tagged book: {book.title}")

print("\n==============================================\n")

print("6. List all genres assigned to more than 5 books")
popular_genres = (
    session.query(Genre.name, func.count(Book.id))
    .join(Genre.books)
    .group_by(Genre.id)
    .having(func.count(Book.id) > 5)
    .all()
)
for genre_name, count in popular_genres:
    print(f"Genre '{genre_name}' has {count} books")

print("\n==============================================\n")

print("7. Books with author info")
books_with_authors = (
    session.query(Book, Author.name, Author.country)
    .join(Book.author)
    .all()
)
for book, author_name, country in books_with_authors:
    print(f"{book.title} by {author_name} ({country})")

print("\n==============================================\n")

print("# 8. Authors and book counts")
author_book_counts = (
    session.query(Author.name, func.count(Book.id).label('book_count'))
    .join(Author.books)
    .group_by(Author.id)
    .order_by(desc('book_count'))
    .all()
)
for author_name, count in author_book_counts:
    print(f"{author_name} wrote {count} book(s) in this dataset")

print("\n==============================================\n")

print("# 9. Total stock value (price * availability) per genre")
stock_value_by_genre = (
    session.query(Genre.name, func.sum(BookDetail.price * BookDetail.availability))
    .join(Genre.books)
    .join(Book.detail)
    .group_by(Genre.id)
    .all()
)
for genre_name, total_value in stock_value_by_genre:
    print(f"{genre_name} total stock value: ${total_value:.2f}")

print("\n==============================================\n")

print("# 10. Books with genre and author names")
book_details_full = (
    session.query(Book.id, Book.title, Genre.name, Author.name)
    .join(Book.genre)
    .join(Book.author)
    .all()
)
for book_id, title, genre_name, author_name in book_details_full:
    print(f"Book {book_id} '{title}' [{genre_name}] - Author: {author_name}")

print("\n==============================================\n")

print("# 11. Average price per genre (only genres with books)")
avg_price_per_genre = (
    session.query(Genre.name, func.avg(BookDetail.price))
    .join(Genre.books)
    .join(Book.detail)
    .group_by(Genre.id)
    .all()
)
for genre_name, avg_price in avg_price_per_genre:
    print(f"{genre_name} - Average Price: ${avg_price:.2f}")

print("\n==============================================\n")

print("# 12. Books with at least 2 tags")
books_with_many_tags = (
    session.query(Book.title, func.count(Tag.id))
    .join(Book.tags)
    .group_by(Book.id)
    .having(func.count(Tag.id) > 1)
    .all()
)
for title, tag_count in books_with_many_tags:
    print(f"{title} has {tag_count} tags")

print("\n==============================================\n")

print("13. List all authors who have written books in every available genre")

total_genres = session.query(func.count(Genre.id)).scalar()

results = (
    session.query(Author.name, func.count(func.distinct(Book.genre_id)).label("used_genres"))
    .join(Author.books)
    .group_by(Author.id)
    .having(func.count(func.distinct(Book.genre_id)) == total_genres)
    .all()
)

if results:
    for author_name, count in results:
        print(f"{author_name} has written in all {count} genres")
else:
    print("No author has written in every genre (expected with only 10 authors and 29 genres)")

print("\n==============================================\n")

print("14. Books priced above their own genre's average price (subquery)")

# Subquery: average price per genre, computed independently of the outer query.
genre_avg_price_subq = (
    session.query(
        Book.genre_id.label("genre_id"),
        func.avg(BookDetail.price).label("avg_price")
    )
    .join(Book.detail)
    .group_by(Book.genre_id)
    .subquery()
)

above_avg_books = (
    session.query(Book.title, Genre.name, BookDetail.price, genre_avg_price_subq.c.avg_price)
    .join(Book.detail)
    .join(Book.genre)
    .join(genre_avg_price_subq, Book.genre_id == genre_avg_price_subq.c.genre_id)
    .filter(BookDetail.price > genre_avg_price_subq.c.avg_price)
    .order_by(Genre.name)
    .all()
)

for title, genre_name, price, avg_price in above_avg_books:
    print(f"{title} [{genre_name}]: ${price:.2f} (genre avg: ${avg_price:.2f})")

print("\n==============================================\n")

print("15. Author with the highest total stock value across their books (subquery)")

# Subquery: total stock value (price * availability) per author.
author_stock_value_subq = (
    session.query(
        Book.author_id.label("author_id"),
        func.sum(BookDetail.price * BookDetail.availability).label("total_value")
    )
    .join(Book.detail)
    .group_by(Book.author_id)
    .subquery()
)

top_author = (
    session.query(Author.name, author_stock_value_subq.c.total_value)
    .join(author_stock_value_subq, Author.id == author_stock_value_subq.c.author_id)
    .order_by(desc(author_stock_value_subq.c.total_value))
    .first()
)

if top_author:
    author_name, total_value = top_author
    print(f"{author_name} holds the highest total stock value: ${total_value:.2f}")
else:
    print("No author has any books with stock value.")


"""
  14. List every book whose price is above the average price of its own genre.
      For each result, print the book's title, its genre, its price, and that genre's average price.
  15. Find the single author whose books have the highest combined stock value
      (price × availability, summed across all of that author's books).
      Print just that one author's name and their total stock value.
"""