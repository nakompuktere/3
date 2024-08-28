import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlsplit
from main import parse_book_page
from main import download_image
from main import download_txt
from pathvalidate import sanitize_filename
import os
import json


all_info_book = []

for number in range(4):
    url = f"https://tululu.org/l55/{number}/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    books = soup.find_all(class_="d_book")
    for book in books:
        book_link = book.find("a")["href"]

        book_link = urljoin(url, book_link)
        # print(book_link)

        book_response = requests.get(book_link)
        response.raise_for_status()

        book_parameters = parse_book_page(book_response, book_link)
        # print(book_parameters)

        all_info_book.append(book_parameters)

        image_folder = "images"
        folder = "books"

        os.makedirs(folder, exist_ok=True)

        os.makedirs(image_folder, exist_ok=True)

        filename = f'{number}.{sanitize_filename(book_parameters["book_name"])}.txt'
        file_path = os.path.join(folder, filename)

        download_image(book_parameters["picture_link"], book_parameters["image_name"], folder='images/')
        download_txt(book_response, filename, file_path, folder='books/')



with open("books_description.json", "w", encoding='utf8') as file:
    json.dump(all_info_book, file, ensure_ascii=False, indent=4)