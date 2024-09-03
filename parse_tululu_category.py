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
import argparse


all_info_book = []

parser = argparse.ArgumentParser(
    description='скачивает фентези книги и информацию про них'
)
parser.add_argument('--start_page', help='страница с которой начнется скачивание', type=int, default=0)

parser.add_argument('--end_page', help='страница на которой закончится скачивание', type=int, default=5)

parser.add_argument('--dest_folder', help='путь к каталогу с результатами парсинга: картинкам, книгам, JSON', default="")

parser.add_argument('--skip_imgs', help='не скачивать картинки', action='store_true')

parser.add_argument('--skip_txt', help='не скачивать книги', action='store_true')

args = parser.parse_args()

for number in range(args.start_page, args.end_page):
    url = f"https://tululu.org/l55/{number}/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    book_selector = "table.d_book"

    books = soup.select(book_selector)
    
    for book in books:
        book_link = book.find("a")["href"]

        book_link = urljoin(url, book_link)
        print(book_link)

        book_response = requests.get(book_link)
        book_response.raise_for_status()

        book_parameters = parse_book_page(book_response, book_link)

        all_info_book.append(book_parameters)

        image_folder = f"./{args.dest_folder}/images"
        folder = f"./{args.dest_folder}/books"

        os.makedirs(folder, exist_ok=True)

        os.makedirs(image_folder, exist_ok=True)

        filename = f'{number}.{sanitize_filename(book_parameters["book_name"])}.txt'
        file_path = os.path.join(folder, filename)

        if not args.skip_txt:
            download_txt(book_response, filename, file_path, folder=folder)

        elif not args.skip_imgs:
            download_image(book_parameters["picture_link"], book_parameters["image_name"], folder=image_folder)



with open("books_description.json", "w", encoding='utf8') as file:
    json.dump(all_info_book, file, ensure_ascii=False, indent=4)


