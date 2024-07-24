import requests
import os

url = 'https://tululu.org/txt.php?id=32168'
response = requests.get(url)
response.raise_for_status()
folder = "books"

if not os.path.exists(folder):
    os.makedirs(folder)

filename = 'dvmn.svg'

file_path = os.path.join(folder, filename)

with open(file_path, 'wb') as file:
    file.write(response.content)