
from hill_climbing_with_greedy_initial.models.Book import Book
from hill_climbing_with_greedy_initial.models.Instance import Instance
from hill_climbing_with_greedy_initial.models.Library import Library


class InstanceProvider:

    @staticmethod
    def get_instance(file_path: str) -> Instance:
        with open(file_path, "r") as file:
            first_line = file.readline().split()
            books_num = int(first_line[0])
            libs_num = int(first_line[1])
            days_num = int(first_line[2])

            book_scores = list(map(int, file.readline().split()))
            books = [Book(i, score) for i, score in enumerate(book_scores)]

            libraries = []

            for i in range(libs_num):
                lib_meta = list(map(int, file.readline().split()))
                num_books, signup_time, books_per_day = lib_meta

                book_ids = list(map(int, file.readline().split()))
                lib_books = [books[book_id] for book_id in book_ids]

                library = Library(i, signup_time, books_per_day, lib_books)
                libraries.append(library)

            instance = Instance()
            instance.books_num = books_num
            instance.libs_num = libs_num
            instance.scanning_days = days_num
            instance.libraries = libraries

            return instance
