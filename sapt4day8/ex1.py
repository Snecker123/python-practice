import csv
import random
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Importăm modelele unificate direct din ex.py pentru a evita duplicarea lor
from ex import Base, engine, Genre, Author, Tag, Book, BookDetail, book_tags

# Resetăm complet tabelele din PostgreSQL
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# --- 3. SEED SYNTHETIC DATA ---

# Liste cu 10 Prenume, 10 Nume și 10 Țări diferite (L-am inclus fix pe Neil Gaiman pentru Query 2)
first_names = ["Neil", "Mircea", "Elena", "Amelie", "Yuki", "Carlos", "Hans", "Aisha", "Pierre", "Oliver"]
last_names = ["Gaiman", "Eliade", "Popescu", "Poulin", "Tanaka", "Garcia", "Müller", "Khan", "Dubois", "Brown"]
countries = ["UK", "Romania", "Canada", "France", "Japan", "Spain", "Germany", "India", "USA", "Australia"]

# Generăm exact 10 autori unici cu Nume, Prenume și Țară aleatorie
authors_data = []
for i in range(10):
    full_name = f"{first_names[i]} {last_names[i]}"
    country_name = countries[i]
    authors_data.append({"name": full_name, "country": country_name})

session.execute(Author.__table__.insert(), authors_data)
session.commit()

# REPARARE: Extragem doar primul element r[0] din fiecare Row pentru a avea numere simple (ex: 8 în loc de (8,))
author_ids = [r[0] for r in session.query(Author.id).all()]

# Generăm cele 10 tag-uri cerute
tags_list = ["bestseller", "award-winning", "series", "classic", "recommended",
             "must-read", "popular", "trending", "new-release", "choice"]
tags_data = [{"name": name} for name in tags_list]
session.execute(Tag.__table__.insert(), tags_data)
session.commit()

# REPARARE: Extragem doar primul element r[0] din fiecare Row pentru tag-uri
tag_ids = [r[0] for r in session.query(Tag.id).all()]

# --- 4. PARSE CSV AND INSERT BOOKS ---
csv_file_path = r"C:\Users\Raluca\PycharmProjects\PythonPractice\sapt4day7\books.csv"

with open(csv_file_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    genre_cache = {}

    for row in reader:
        # Căutăm sau inserăm Genul din mers
        genre_name = row['genre']
        if genre_name not in genre_cache:
            res = session.execute(Genre.__table__.insert().values(name=genre_name).returning(Genre.id))
            genre_cache[genre_name] = res.scalar()

        # Alocăm un autor la întâmplare din cei 10 generați mai sus (inclusiv Neil Gaiman)
        assigned_author_id = random.choice(author_ids)

        # Inserăm rândul în tabela books
        book_res = session.execute(
            Book.__table__.insert().values(
                title=row['title'],
                upc=row['upc'],
                genre_id=genre_cache[genre_name],
                author_id=assigned_author_id
            ).returning(Book.id)
        )
        new_book_id = book_res.scalar()

        # Extragem numărul din stringul de disponibilitate: "In stock (X available)"
        avail_match = re.search(r'\d+', row['availability'])
        avail_count = int(avail_match.group()) if avail_match else 0

        # Inserăm detalii în tabela book_details
        session.execute(
            BookDetail.__table__.insert().values(
                book_id=new_book_id,
                rating=int(row['rating']),
                price=float(row['price']),
                availability=avail_count
            )
        )

        # Alocăm aleatoriu între 0 și 3 tag-uri unice pentru fiecare carte
        num_tags = random.randint(0, 3)
        chosen_tags = random.sample(tag_ids, num_tags)
        for t_id in chosen_tags:
            session.execute(book_tags.insert().values(book_id=new_book_id, tag_id=t_id))

session.commit()
print("Seeding Complete! Neil Gaiman has been successfully integrated.")
