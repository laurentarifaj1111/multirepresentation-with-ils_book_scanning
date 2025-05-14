from ast import Index
from collections import OrderedDict

from hill_climbing_with_greedy_initial.models.Instance import Instance


class SolutionRepresentation:
    def __init__(self):
        self.books_to_scan = OrderedDict()  # lib_id -> list of book IDs
        self.unscanned_books = OrderedDict()  # lib_id -> list of book IDs
        self.fitness = 0

    def clone(self):
        cloned = SolutionRepresentation()
        cloned.books_to_scan = self._deep_copy_map(self.books_to_scan)
        cloned.unscanned_books = self._deep_copy_map(self.unscanned_books)
        cloned.fitness = self.fitness
        return cloned

    def get_books_to_scann(self):
        return [book_id for book_list in self.books_to_scan.values() for book_id in book_list]

    # def get_unsigned_libraries(self, instance: Instance):
    #     books_to_scan = set(self.books_to_scan.keys())
    #     unscanned_books = set(self.unscanned_books.keys())
    #     result = unscanned_books - books_to_scan
    #     return result

    def get_unsigned_libraries(self, instance:Instance):
        signed_libs_ids = set(self.books_to_scan.keys())
        unscanned_books = set()
        for lib in instance.libraries:
            if lib.id not in signed_libs_ids:
                unscanned_books.add(lib.id)
        return unscanned_books
    # #

    @staticmethod
    def _deep_copy_map(original):
        return OrderedDict((k, list(v)) for k, v in original.items())

