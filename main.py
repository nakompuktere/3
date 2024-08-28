import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
from urllib.parse import urlsplit
import argparse
import time
import json


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError
        
def download_txt(response, filename, file_path, folder='books/'):
    with open(file_path, 'wb') as file:
        file.write(response.content)

def download_image(picture_link, image_name, folder='images/'):
    response = requests.get(picture_link)
    response.raise_for_status()
    image_path = os.path.join(folder, image_name)
    with open(image_path, 'wb') as file:
        file.write(response.content)

def parse_book_page(book_response, book_url):
    soup = BeautifulSoup(book_response.text, 'lxml')
    title_tag = soup.find('h1').text.split('::')
    author = title_tag[1].strip()
    book_name = title_tag[0].strip()

    book_picture_link = soup.find(class_='bookimage').find('img')['src']
    picture_link = urljoin(book_url, book_picture_link)
    image_name = urlsplit(picture_link).path.split('/')[-1]

    comments_tags = soup.find_all(class_='texts')
   
    book_comments = []

    for book_comment in comments_tags:
        book_comment = book_comment.find(class_='black').text
        book_comments.append(book_comment)
    print(book_comments)
        
    genre_tag = soup.find_all(class_='d_book')[1]
    genre_links = genre_tag.find_all("a")

    genres = [genre.text for genre in genre_links]

    
    book_parameters = {
        "book_genres": genres,
        "picture_link": picture_link,
        "author": author,
        "book_name": book_name,
        "image_name": image_name,
        "book_comment": book_comments,
    }
    return book_parameters


def main():
    folder = "books"
    image_folder = "images"

    parser = argparse.ArgumentParser(
        description='скачивает книги'
    )
    parser.add_argument('--start_id', help='id начало скачивания книг', default=1, type=int)
    parser.add_argument('--end_id', help='конечный id книг', default=11, type=int)
    args = parser.parse_args()

    
    os.makedirs(folder, exist_ok=True)

    os.makedirs(image_folder, exist_ok=True)


    for number in range(args.start_id, args.end_id):
        url = f'https://tululu.org/txt.php'
        book_url = f"https://tululu.org/b{number}/"
        payload = {
            "id": number
        }
        try:
            response = requests.get(url, params=payload)
            response.raise_for_status()
            check_for_redirect(response)

            book_response = requests.get(book_url)
            book_response.raise_for_status()
            check_for_redirect(response)

            book_page = parse_book_page(book_response, book_url)

            filename = f'{number}.{sanitize_filename(book_page["book_name"])}.txt'
            file_path = os.path.join(folder, filename)
            
            download_txt(response, filename, file_path, folder='books/')
            download_image(book_page["picture_link"], book_page["image_name"], folder='images/')
            
        except requests.HTTPError:
            print("такой книги нет")
        
        except requests.ConnectionError:
            print("ошибка соединения")
            time.sleep(5)


if __name__ == "__main__":
    main()