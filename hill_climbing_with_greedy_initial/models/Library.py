from typing import List, Set

from hill_climbing_with_greedy_initial.models.Book import Book


class Library:
    def __init__(self, id: int, signup_time: int, books_per_day: int, books: List[Book] = None):
        self.id = id
        self.score = 0.0
        self.signup_time = signup_time
        self.books_per_day = books_per_day
        self.books = books if books is not None else []

    def add_book(self, book: Book):
        self.books.append(book)

    def find_unsigned_books_of_lib(self, unique_books: Set[int]) -> List[Book]:
        return [book for book in self.books if book.id in unique_books]

    def __str__(self):
        return f"Library(id={self.id}, signup_time={self.signup_time}, books_per_day={self.books_per_day}, books={self.books})"