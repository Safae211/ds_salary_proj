import requests
from bs4 import BeautifulSoup
import csv

# URL of the site
BASE_URL = "https://books.toscrape.com/"

# Send HTTP request
response = requests.get(BASE_URL)
response.encoding = "utf-8"
response.raise_for_status()  # Raise error if something goes wrong

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find all book containers
books = soup.find_all("article", class_="product_pod")

# Prepare CSV file
with open("books.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Price", "Availability"])  # Header row

    # Loop through each book and extract data
    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        availability = book.find("p", class_="instock availability").text.strip()

        writer.writerow([title, price, availability])
        print(title, "|", price, "|", availability)

print("\n✅ Scraping complete! Data saved in books.csv")