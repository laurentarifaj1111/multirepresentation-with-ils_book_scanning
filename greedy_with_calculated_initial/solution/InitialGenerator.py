from typing import Set

from greedy_with_calculated_initial.models.Library import Library
from greedy_with_calculated_initial.models.SolutionRepresentation import SolutionRepresentation


class InitialSolutionGenerator:

    @staticmethod
    def generate_initial_solution(instance):
        libraries = list(instance.libraries)
        solution = SolutionRepresentation()
        unique_books = set(instance.get_unique_books())
        modifiable_libraries = list(libraries)

        total_days = instance.scanning_days
        current_day = 0

        while modifiable_libraries:
            modifiable_libraries.sort(key =InitialSolutionGenerator.get_library_comparator_v2(total_days, current_day, unique_books))

            library = modifiable_libraries.pop(0)

            if current_day + library.signup_time >= total_days:
                continue

            current_day += library.signup_time
            max_books = (total_days - current_day) * library.books_per_day

            unique_per_lib = [book for book in library.books if book.id in unique_books]
            sorted_books = sorted(unique_per_lib, key=lambda b: b.score, reverse=True)

            selected_books = []
            unselected_books = []

            for book in sorted_books:
                if book.id not in unique_books:
                    unselected_books.append(book.id)
                elif len(selected_books) < max_books:
                    selected_books.append(book.id)
                    unique_books.remove(book.id)
                    solution.fitness += book.score
                else:
                    unselected_books.append(book.id)
            if len(selected_books) > 0:
                solution.books_to_scan[library.id] = selected_books
            solution.unscanned_books[library.id] = unselected_books

        return solution

    @staticmethod
    def get_library_comparator_v2(scanning_days: int, current_day: int, unique_books: Set[int]):
        def comparator(library: Library):
            InitialSolutionGenerator.calculate_library_score_v2(scanning_days, current_day, library, unique_books)
            return -library.score, library.id  # Negative for descending sort
        return lambda lib: comparator(lib)

    @staticmethod
    def calculate_library_score_v2(scanning_days: int, current_day: int, library: Library, unique_books: Set[int]):
        active_days = scanning_days - current_day - library.signup_time
        if active_days <= 0:
            library.score = 0
            return

        available_books = [book for book in library.books if book.id in unique_books]
        scanned_books = min(active_days * library.books_per_day, len(available_books))
        sorted_scores = sorted([book.score for book in available_books], reverse=True)
        library.score = sum(sorted_scores[:scanned_books]) / library.signup_time if library.signup_time else 0
