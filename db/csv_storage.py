import csv
import os
import json



class CSVStorage:
    def __init__(self, filename):
        self.filename = filename               # получаем имя файла и заносим в объект
        file_exist = os.path.isfile(filename)  # в объект 'file_exist' заносим информацию о том есть файл или нет
        self.file = open(self.filename, "a+", encoding='utf-8')  # открывается файл в режиме дозаписи

        if file_exist:                         # если файл существует при открытии программы то
            self.last_id = self.get_last_id()  # получаем последний id (будет равен результату метода get_last_id())
        else:                                  # иначе, если файл не существует
            self.last_id = "0"                 # последний id будет равен 0 ! для того, чтобы первая строчка была с 1

        fields = ["id", "author", "title", "year", "genre", "ISBN"] # определяются поля
        writer = csv.DictWriter(self.file, fieldnames=fields)       # через 'DictWriter' эти поля записываются в файл
        if not file_exist:                                          # если файл не существовал
            writer.writeheader()                                    # то он записывется, если существовал то заголовки второй раз не пишутся


    # МЕТОД ПОЛУЧЕНИЯ ПОСЛЕДНЕГО 'id'
    def get_last_id(self):
        data = self.read_data()
        if data:                         # если 'data' есть, т.е. файл был не пустой, то:
            last_id = data[-1].get("id") # получаем 'last_id' как последняя строчка и в этой последней строчке ключик 'id'
            return last_id               # и возвращаем его
        else:                            # иначе
            return "0"                   # возвращаем '0' (данные есть, но строчек с книгами нет)


    def write_data(self, book: dict):
        writer = csv.DictWriter(self.file, fieldnames=book.keys())
        writer.writerow(book)

    # МЕТОД УВЕЛИЧЕНИЯ 'ID'
    def increment_last_id(self):
        self.last_id = str(int(self.last_id) + 1) # берем 'last_id' переводим его в цыфру, добавляем 1 и переводим обратно в строку, чтобы он таким же и остался

    # МЕТОД ВОЗВРАЩЕНИЯ СПИСКА СЛОВАРЕЙ (1 слой-слой данных)
    def read_data(self):
        self.file.seek(0)                   # перемещение курсора в начало файла
        reader = csv.DictReader(self.file)  # 'csv.DictReader' считывает файл
        return list(reader)                 # и визвращает список словарей


    def dump_books_to_json(self, filename):
        books = self.read_data()
        data = {}
        for book in books:
            data[book.pop("id")] = book
        with open (f"{filename}.json", 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)




