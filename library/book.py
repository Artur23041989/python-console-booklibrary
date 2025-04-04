from datetime import datetime
import uuid
from core.enums import GENRES


class Book:
    def __init__(self, title, author, year, genre):
        """
        Конструктор класса Book
        :param title: Название книги
        :param author: Автор книги
        :param year: Год издания книги
        :param genre: Жанр книги (по умолчанию None)
        :param isbn: ISBN книги (по умолчанию None)
        """
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.__isbn = uuid.uuid4().hex[:9]
        self.id = None

    def get_info(self):
        """
        Возвращает строки с информацией о книге
        :return: Строка с информацией о книге
        """
        info = f"{self.title} - {self.author} ({self.year})"
        if self.genre:
            info += f", Жанр: {self.genre}"

        info += f", ISBN: {self.__isbn}"
        return info

    @staticmethod
    def is_valid_year(year):
        if isinstance(year, int):
            if 1445 < year <= datetime.today().year:
                return True
            else:
                return False
        elif isinstance(year, str):
            if year.isdigit():
                if 1445 < int(year) <= datetime.today().year:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def is_older_than(self, year):
        """
        Проверяет, была ли книга издана до указанного года
        :param year: год издания
        :return: bool
        """
        if self.is_valid_year(year):
            return self._year < year
        else:
            raise ValueError('Неверное значение для года издания!')

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, new_year):
        if self.is_valid_year(new_year):
            self._year = new_year
        else:
            raise ValueError('Неверное значение для года издания!')

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, genre):
        if genre.lower() in GENRES:
            self._genre = genre
        else:
            raise ValueError("Неизвестный жанр")

    @property
    def isbn(self):
        return self.__isbn

    @isbn.setter
    def isbn(self, isbn):
        self.__isbn = isbn

    def get_book_age(self):
        current_year = datetime.today().year
        return current_year - self._year

    def to_dict(self): # возвращает объект в виде словаря
        data = {"id": self.id,
                "author": self.author,
                "title": self.title,
                "year": self.year,
                "genre": self.genre,
                "ISBN": self.__isbn
                }
        return data


    # МЕТОД, КОТОРЫЙ ДЕЛАЕТ ИЗ СЛОВАРЯ ОБЪЕКТ КНИГИ
    @classmethod
    def from_dict(cls, book_data):
        book = Book(                  # создаем объект книги из словаря
            author=book_data["author"],
            title=book_data["title"],
            year=book_data["year"],
            genre=book_data["genre"]
        )
        book.isbn = book_data["ISBN"] # потому что это приватный атрибут
        book.id = book_data["id"]     # делаем так, потому что 'id' нет в параметрах конструктора
        return book # возвращает книгу










