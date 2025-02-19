import logging
from abc import ABC, abstractmethod
from typing import List

logging.basicConfig(level=logging.INFO)


class Book:
    """
    Represents a book with a title, author, and year of publication.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        year (str): The year the book was published.
    """

    def __init__(self, title: str, author: str, year: str) -> None:
        self.title = title
        self.author = author
        self.year = year

    def __str__(self) -> str:
        return f'Title: {self.title}, Author: {self.author}, Year: {self.year}'


class LibraryInterface(ABC):
    """
    Abstract base class for a library interface.
    """

    @abstractmethod
    def add_book(self, book: Book) -> None:
        """
        Adds a book to the library.

        Args:
            book (Book): The book to add.
        """
        pass

    @abstractmethod
    def remove_book(self, title: str) -> None:
        """
        Removes a book from the library by its title.

        Args:
            title (str): The title of the book to remove.
        """
        pass

    @abstractmethod
    def show_books(self) -> None:
        """
        Displays all books in the library.
        """
        pass


class Library(LibraryInterface):
    """
    Concrete implementation of the LibraryInterface.
    """

    def __init__(self) -> None:
        self.books: List[Book] = []

    def add_book(self, book: Book) -> None:
        self.books.append(book)
        logging.info(f'\nBook added: {book}')

    def remove_book(self, title: str) -> None:
        self.books = [book for book in self.books if book.title != title]
        logging.info(f'\nBook removed: {title}')

    def show_books(self) -> None:
        for book in self.books:
            logging.info(f'\n{book}')


class LibraryManager:
    """
    Manages library operations using a LibraryInterface.

    Attributes:
        library (LibraryInterface): The library interface to manage.
    """

    def __init__(self, library: LibraryInterface) -> None:
        self.library = library

    def add_book(self, title: str, author: str, year: str) -> None:
        book = Book(title, author, year)
        self.library.add_book(book)

    def remove_book(self, title: str) -> None:
        self.library.remove_book(title)

    def show_books(self) -> None:
        self.library.show_books()


def main() -> None:
    """
    Main function to run the library manager.
    """
    library = Library()
    manager = LibraryManager(library)

    while True:
        command = input("Enter command (add, remove, show, exit): ").strip().lower()

        match command:
            case "add":
                title = input("Enter book title: ").strip()
                author = input("Enter book author: ").strip()
                year = input("Enter book year: ").strip()
                manager.add_book(title, author, year)
            case "remove":
                title = input("Enter book title to remove: ").strip()
                manager.remove_book(title)
            case "show":
                manager.show_books()
            case "exit":
                break
            case _:
                logging.warning("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
