# Парсер книг с сайта tululu.org

Скачивает книги и информацию о них с сайта [tutulu.org](https://tululu.org/)

### Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Как запустить

Чтобы запустить программу следует ввести в терминал:
```
python parse_tutulu_books.py
```
Можно сделать выбор с какой по какую книгу вам надо скачать.
Для этого используйте `--start_page` и `--end_page`.
Следует ввести id начала и конца
```
python parse_tutulu_books --start_id 5 --end_page 12
```
Можно выбрать путь к каталогу с результатами парсинга.
Для этого используйте `--dest_folder`.
```
python parse_tutulu_books --dest_folder folder_name
```
Можно не скачивать картинки или книги.
Для этого используйте `--skip_imgs` и `--skip_txt`.
```
python parse_tutulu_books --skip_imgs --skip_txt
```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).