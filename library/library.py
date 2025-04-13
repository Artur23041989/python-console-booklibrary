from . import Book



class Library:
    def __init__(self, storage):
        self.books = {}           # создаем пустой словарь 'books'
        self.storage = storage    # хранилище
        self.last_id = None       # 'None' потому что при инициализации мы не указываем 'id'

    def _get_last_id_book(self):
        last_id = self.storage.get_last_id() # вызывается метод получения последнего 'id' из хранилища
        return last_id                       # и возвращается


    # МЕТОД УВЕЛИЧЕНИЯ 'id' ПОСЛЕДНЕЙ КНИГИ В ХРАНИЛИЩЕ
    def increment_book_id(self):
        self.last_id = int(self._get_last_id_book()) # получается сначала последний 'id'
        self.last_id += 1                            # потом он увеличивается для внутренней работы класса если программа не закрывается
        self.storage.increment_last_id()             # и увеличивается одновременно в хранилище


    # МЕТОД ДОБАВЛЕНИЯ КНИГИ В БИБЛИОТЕКУ
    def add_book(self, book: Book):
        if isinstance(book, Book):                   # если книга является книгой
            self.increment_book_id()                 # вызываем метод 'self.increment_book_id()' получение увеличения последнего 'id'
            book.id = str(self.last_id)              # заносим в объект 'book' атрибут 'id' и 'str(self.last_id)'
            self.storage.write_data(book.to_dict())  # вызываем метод записи 'storage.write_data(book.to_dict())'
            return book
        raise ValueError("Неверный формат книги!")

    def get_book_by_id(self, book_id):
        book = self.books.get(book_id)
        if book:
            return book
        raise ValueError("Такой книги нет")

    def get_book_by_isbn(self, isbn):
        results = []
        books = self.storage.read_data()
        for item in books:
            if isbn.lower() in item['ISBN'].lower(): # если подстрока 'isbn.lower()' содержится в строке 'item['ISBN']'
                results.append(Book.from_dict(item))
        return results

    # 2 слой данных
    def get_books(self):
        books = self.storage.read_data() # получаем список словарей и cохраняем в 'books'
        books_obj = []                   # будущий список книг, который будет получен из словарей
        for book in books:               # проходимся по каждому словарю из словарей
            books_obj.append(Book.from_dict(book)) # добавляем в список книг, именно объекта, объект книги
        return books_obj

    def get_books_by_author(self, author: str):
        results = []
        books = self.storage.read_data()  # получаем список словарей 'storage.read_data()'
        for item in books:                # для каждого словаря из словарей, которые мы получили
            if author.lower() in item['author'].lower(): # если автор, которого мы передали в параметре, содержится в словаре 'item'
                results.append(Book.from_dict(item))     # то тогда в результат добавлем книгу
        return results

    def get_books_by_title(self, title: str):
        results = []
        books = self.storage.read_data()
        for item in books:
            if title.lower() in item['title'].lower():
                results.append(Book.from_dict(item))
        return results

    def search_book(self, query):
        results = {}
        for id_, book in self.books.items():
            if query.lower() in book.author.lower():
                results[id_] = book
        return results

    def book_delete(self, isbn: str):
        books = self.storage.read_data() # получаем список словарей (получаем все книги)
        for i, book in enumerate(books): # проходимся по списку словарей и
            # удаляем словарь с нужным isbn
            if book["ISBN"].lower() == isbn.lower():
                books.pop(i)
        # очищаем файл (начиная с конца хедера (33))
        self.storage.file.seek(33)
        self.storage.file.truncate()
        for book in books: # добавляем заново книги из словаря в файл
            self.add_book(Book.from_dict(book)) # перед этим преобразуя в объект Book

    def get_book_count(self):
        count = self.storage.count_books()
        return count

    def check_book(self, isbn):
        books = self.storage.read_data() # получаем книги
        for item in books:
            if item["ISBN"].lower() == isbn.lower():
                return item["ISBN"]
        return None

    def dump_books_data(self, filename):
        self.storage.dump_books_to_json(filename)


