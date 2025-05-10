from typing import List, Set, Dict
from collections import OrderedDict, defaultdict

from greedy_with_calculated_initial.models.Library import Library


class Instance:
    def __init__(self, books_num=0, libs_num=0, scanning_days=0, libraries=Library):
        self.books_num = books_num
        self.libs_num = libs_num
        self.scanning_days = scanning_days
        self.libraries = libraries if libraries is not None else []

    def get_unique_books(self) -> Set[int]:
        unique_books = set()
        for library in self.libraries:
            book_ids = {book.id for book in library.books}
            unique_books.update(book_ids)
        return unique_books

    def get_libs_as_map(self) -> Dict[int, 'Library']:
        return {library.id: library for library in self.libraries}

    def get_duplicate_books_with_signed_libraries(
        self,
        signed_libraries: "OrderedDict[int, List[int]]",
        unsigned_libraries: Set[int]
    ) -> Dict[int, List['Library']]:
        signed_book_ids = set(
            book_id for book_ids in signed_libraries.values() for book_id in book_ids
        )

        result = defaultdict(list)

        for library in self.libraries:
            if library.id in signed_libraries and library.id in unsigned_libraries:
                for book in library.books:
                    if book.id in signed_book_ids:
                        result[book.id].append(library)

        # Only return entries where the same book appears in multiple libraries
        return {book_id: libs for book_id, libs in result.items() if len(libs) > 1}
