import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
from urllib.parse import urlsplit


folder = "books"
image_folder = "images"

if not os.path.exists(folder):
    os.makedirs(folder, exist_ok=True)

if not os.path.exists(image_folder):
    os.makedirs(image_folder, exist_ok=True)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError
        
def download_txt(response, filename, folder='books/'):
    with open(file_path, 'wb') as file:
        file.write(response.content)

def download_image(picture_link, image_name, folder='images/'):
    response = requests.get(picture_link)
    response.raise_for_status()
    image_path = os.path.join(folder, image_name)
    with open(image_path, 'wb') as file:
        file.write(response.content)


for number in range(1, 11):
    url = f'https://tululu.org/txt.php?id={number}'
    book_url = f"https://tululu.org/b{number}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        check_for_redirect(response)

        book_response = requests.get(book_url)
        book_response.raise_for_status()
        soup = BeautifulSoup(book_response.text, 'lxml')
        title_tag = soup.find('h1').text.split('::')
        author = title_tag[1].strip()
        book_name = title_tag[0].strip()

        book_picture_link = soup.find(class_='bookimage').find('img')['src']
        picture_link = urljoin(book_url, book_picture_link)
        image_name = urlsplit(picture_link).path.split('/')[-1]


        filename = f'{number}.{sanitize_filename(book_name)}.txt'
        file_path = os.path.join(folder, filename)


        book_comments = soup.find_all(class_='texts')
        for book_comment in book_comments:
            book_comment = book_comment.find(class_='black')
            print(book_comment.text)


        download_txt(response, filename, folder='books/')
        download_image(picture_link, image_name, folder='images/')
        
    except requests.HTTPError:
        print("такой книги нет")

