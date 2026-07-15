"""Build a simple web scraper using beautifulsoup and requests libraries.
The site you need to scrape is: https://books.toscrape.com/.
You will write a single modular script to perform three core actions:
	-Extract: Loop through the first 5 pages dynamically using requests.
	-Transform: Extract and normalize titles, convert star-ratings text ("Three")
	 to integers (3), and strip currency symbols (Â£) from prices.
	-The output CSV should have: title,genre,rating,upc,price,availability
	-Load: Write the completely sanitized dataset into a structured CSV.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"

current_page_url = url + "index.html"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

books = soup.find_all("article", class_= "product_pod")


books_table = {
    "title": [],
    "genre": [],
    "rating": [],
    "upc": [],
    "price": [],
    "availability": []
}

index = 0


while index < 5:
    response = requests.get(current_page_url)
    soup = BeautifulSoup(response.content, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    for book in books:
        #print(book)
        href = book.h3.a["href"]
        if "catalogue/" in href:
            book_page_url = url + "/" + href
        else:
            book_page_url = url + "/catalogue/" + href
        #print(book_page)


        book_soup = BeautifulSoup(requests.get(book_page_url).content, "html.parser")
        title = book.h3.a["title"]
        price_tag = book.find("p", class_="price_color")
        price = price_tag.text
        price_value = ""
        temp = price


        for i in range(0,len(price)):
            if price[i] == "," or price[i] == "." or price[i].isdigit():
                price_value = price_value + price[i]


        price_value = price_value.replace(",", "")


        rating_zero = book.find("p", class_="star-rating Zero")
        rating_one = book.find("p", class_="star-rating One")
        rating_two = book.find("p", class_="star-rating Two")
        rating_three = book.find("p", class_="star-rating Three")
        rating_four = book.find("p", class_="star-rating Four")
        rating_five = book.find("p", class_="star-rating Five")

        if rating_zero is not None:
            rating = 0
        elif rating_one is not None:
            rating = 1
        elif rating_two is not None:
            rating = 2
        elif rating_three is not None:
            rating = 3
        elif rating_four is not None:
            rating = 4
        else:
            rating = 5


        table = book_soup.find("table", class_= "table table-striped")
        upc = table.tr.td.text #???????????? de ce fara tbody ca in inspect

        breadcrumb = book_soup.find("ul", class_= "breadcrumb")
        genre = breadcrumb.find_all("li")[2].text.strip()


        availability_text = table.find_all("tr")[5].td.text
        print(availability_text)

        print(f"{title} {price_value} rating: {rating} \t upc: {upc}\ngenre = {genre}")




        books_table["title"].append(title)
        books_table["genre"].append(genre)
        books_table["rating"].append(rating)
        books_table["upc"].append(upc)
        books_table["price"].append(price_value)
        books_table["availability"].append(availability_text)

    next_button = soup.find("li", class_="next")
    if next_button:
        next_href = next_button.a["href"]
        if "catalogue/" in next_href:
            current_page_url = url + "/" + next_href
        else:
            current_page_url = url + "/catalogue/" + next_href

    index = index + 1



df = pd.DataFrame(books_table)
df.to_csv("books.csv", index=False)
