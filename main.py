import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

folder = "books"

if not os.path.exists(folder):
    os.makedirs(folder, exist_ok=True)

def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError
        
def download_txt(response, filename, folder='books/'):
    with open(file_path, 'wb') as file:
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

        filename = f'{number}.{sanitize_filename(book_name)}.txt'
        file_path = os.path.join(folder, filename)

        print('название книги:', book_name, 'Автор:', author)
        download_txt(response, filename, folder='books/')

    except requests.HTTPError:
        print("такой книги нет")

