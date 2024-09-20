import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlsplit
from parse_tutulu_books import parse_book_page
from parse_tutulu_books import download_image
from parse_tutulu_books import download_txt
from parse_tutulu_books import check_for_redirect
from pathvalidate import sanitize_filename
import os
import json
import argparse
import time


def main():
    parser = argparse.ArgumentParser(
        description='скачивает фентези книги и информацию про них'
    )
    parser.add_argument('--start_page', help='страница с которой начнется скачивание', type=int, default=0)
    parser.add_argument('--end_page', help='страница на которой закончится скачивание', type=int, default=5)
    parser.add_argument('--dest_folder', help='путь к каталогу с результатами парсинга: картинкам, книгам, JSON', default="parse_folder")
    parser.add_argument('--skip_imgs', help='не скачивать картинки', action='store_true')
    parser.add_argument('--skip_txt', help='не скачивать книги', action='store_true')

    book_description = []
    args = parser.parse_args()

    image_folder = f"{args.dest_folder}/images"
    books_folder = f"{args.dest_folder}/books"

    os.makedirs(args.dest_folder, exist_ok=True)

    os.makedirs(books_folder, exist_ok=True)

    os.makedirs(image_folder, exist_ok=True)

    for number in range(args.start_page, args.end_page):
        url = f"https://tululu.org/l55/{number}/"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        book_selector = "table.d_book"

        books = soup.select(book_selector)
        
        for book in books:
            book_link = book.find("a")["href"]
            book_id = book_link[2:-1]
            txt_url = "https://tululu.org/txt.php"
            payload = {
                "id": book_id
            }
            try:
                text_response = requests.get(txt_url, params=payload)
                text_response.raise_for_status()
                check_for_redirect(text_response)

                book_link = urljoin(url, book_link)

                book_response = requests.get(book_link)
                book_response.raise_for_status()
                check_for_redirect(book_response)

                soup = BeautifulSoup(book_response.text, 'lxml')

                book_parameters = parse_book_page(book_response, book_link)
                book_parameters["book_path"] = f"{books_folder}/{book_parameters["book_name"]}"
                book_parameters["image_path"] = f"{image_folder}/{book_parameters["image_name"]}"

                book_description.append(book_parameters)
                filename = f'{number}.{sanitize_filename(book_parameters["book_name"])}.txt'
                file_path = os.path.join(books_folder, filename)

                if not args.skip_txt:
                    download_txt(text_response, filename, file_path, folder=books_folder)

                if not args.skip_imgs:
                    download_image(book_parameters["picture_link"], book_parameters["image_name"], folder=image_folder)

            except requests.HTTPError:
                print("такой книги нет")
            
            except requests.ConnectionError:
                print("ошибка соединения")
                time.sleep(5)

    with open(f"{args.dest_folder}/books_description.json", "w", encoding='utf8') as file:
        json.dump(book_description, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()