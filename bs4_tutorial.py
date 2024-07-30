import requests


url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()


from bs4 import BeautifulSoup


soup = BeautifulSoup(response.text, 'lxml')

title_tag = soup.find('main').find('header').find('h1')
title_text = title_tag.text
print(soup.find(class_='entry-content').text)

print(title_text)

print(soup.find('img', class_='attachment-post-image')['src'])