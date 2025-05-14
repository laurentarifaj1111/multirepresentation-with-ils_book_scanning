import random

from hill_climbing_with_greedy_initial.solution.TweakOperatorParams import TweakOperatorParams
from hill_climbing_with_greedy_initial.solution.Utils import Utils
from hill_climbing_with_greedy_initial.models.Instance import Instance
from hill_climbing_with_greedy_initial.models.SolutionRepresentation import SolutionRepresentation


# Replaces a random signed library with an unsigend library
class ReplaceLibsTweakOperator:
    def tweak(self, solution: SolutionRepresentation, instance: Instance) -> SolutionRepresentation:
        books_to_scan = solution.books_to_scan
        signed_libs = set(books_to_scan.keys())

        # Find unsigned libraries
        unsigned_libs = {lib.id for lib in instance.libraries if lib.id not in signed_libs}
        if not unsigned_libs:
            return solution  # Nothing to replace

        signed_libs_list = list(signed_libs)
        unsigned_libs_list = list(unsigned_libs)

        signed_index = random.randint(0, len(signed_libs_list) - 1)
        unsigned_index = random.randint(0, len(unsigned_libs_list) - 1)

        signed_lib_id = signed_libs_list[signed_index]
        unsigned_lib_id = unsigned_libs_list[unsigned_index]

        libs_map = instance.get_libs_as_map()

        # Replace the signed lib with the unsigned lib
        new_libs_order = list(signed_libs_list)
        for i, lib_id in enumerate(new_libs_order):
            if lib_id == signed_lib_id:
                new_libs_order[i] = unsigned_lib_id

        # Rebuild the final list considering signup time constraints
        final_list = []
        signup_time_accumulator = 0

        for lib_id in new_libs_order:
            signup_time = libs_map[lib_id].signup_time
            if signup_time_accumulator + signup_time < instance.scanning_days:
                signup_time_accumulator += signup_time
                final_list.append(lib_id)

        return Utils.generate_solution_for_libs_listed(instance, final_list)

# Reorder 2 random signed libraries
class ReorderLibsTweakOperator:
    def tweak(self, solution: SolutionRepresentation, instance: Instance) -> SolutionRepresentation:
        books_to_scan = solution.books_to_scan
        libs = list(books_to_scan.keys())

        if len(libs) < 2:
            return solution  # Nothing to swap

        first_index = random.randint(0, len(libs) - 1)
        second_index = random.randint(0, len(libs) - 1)

        swapped_libs_order = Utils.swap_by_index(books_to_scan, first_index, second_index)
        return Utils.generate_solution_for_libs_listed(instance, swapped_libs_order)

# Shuffles signed libraries
class ShuffleLibsTweakOperator:
    def tweak(self, solution: SolutionRepresentation, instance: Instance) -> SolutionRepresentation:
        books_to_scan = solution.books_to_scan
        libs = list(books_to_scan.keys())

        if len(libs) < 2:
            return solution  # No point in shuffling if fewer than 2 libraries

        random.shuffle(libs)  # Shuffle in-place
        return Utils.generate_solution_for_libs_listed(instance, libs)

# Swaps books between 2 signed libraries with same book
class SwapBooksTweakOperator:
    def tweak(self, solution: SolutionRepresentation, instance: Instance, params: TweakOperatorParams) -> SolutionRepresentation:
        rand = random.Random()
        clone = solution.clone()

        # Get signed library IDs that still have unscanned books
        available_libs = {lib_id for lib_id, books in clone.unscanned_books.items() if books}

        duplicate_books_with_signed_libraries = instance.get_duplicate_books_with_signed_libraries(
            clone.books_to_scan, available_libs
        )

        if not duplicate_books_with_signed_libraries:
            return clone

        entries = list(duplicate_books_with_signed_libraries.items())
        random_entry = entries[rand.randint(0, len(entries) - 1)]

        book_to_move = random_entry[0]
        libraries_with_book = random_entry[1]

        library_with_scanned_book = self.get_library_with_scanned_book(clone, book_to_move)

        if library_with_scanned_book is None:
            return clone

        from_lib = next((lib for lib in instance.libraries if lib.id == library_with_scanned_book), None)
        if from_lib is None:
            return clone

        signed_libraries_containing_book = [lib for lib in libraries_with_book if lib.id != library_with_scanned_book]
        if not signed_libraries_containing_book:
            return clone

        to_lib = signed_libraries_containing_book[rand.randint(0, len(signed_libraries_containing_book) - 1)]

        from_lib_books = clone.books_to_scan.get(from_lib.id, [])
        to_lib_books = clone.books_to_scan.get(to_lib.id, [])

        # Calculate days before toLib
        lib_ids_until_to_lib = []
        for lib_id in clone.books_to_scan.keys():
            if lib_id == to_lib.id:
                break
            lib_ids_until_to_lib.append(lib_id)

        signup_sum = sum(
            lib.signup_time for lib in instance.libraries if lib.id in lib_ids_until_to_lib
        )
        signup_sum += to_lib.signup_time
        active_days = instance.scanning_days - signup_sum
        to_lib_capacity = min(active_days * to_lib.books_per_day, len(to_lib_books))

        delta_fitness = 0
        added_to_to_lib = False
        replaced_book = None
        book_scores = params.book_scores

        if len(to_lib_books) < to_lib_capacity:
            to_lib_books.append(book_to_move)
            added_to_to_lib = True
            delta_fitness += book_scores.get(book_to_move, 0)
        else:
            if to_lib_books:
                candidate = to_lib_books.pop()
                clone.books_to_scan[to_lib.id] = to_lib_books
                # If candidate is no longer present anywhere
                all_signed_books = {book for books in clone.books_to_scan.values() for book in books}
                if candidate not in all_signed_books:
                    replaced_book = candidate
                    to_lib_books.append(book_to_move)
                    delta_fitness += book_scores.get(book_to_move, 0)
                    delta_fitness -= book_scores.get(replaced_book, 0)

        if not added_to_to_lib and replaced_book is None:
            return clone

        # Remove book from fromLib
        if book_to_move in from_lib_books:
            from_lib_books.remove(book_to_move)
        delta_fitness -= book_scores.get(book_to_move, 0)

        # Try to refill fromLib with an unscanned book
        unscanned = clone.unscanned_books.get(from_lib.id, [])
        for candidate in list(unscanned):  # Copy to avoid concurrent modification
            all_signed_books = {book for books in clone.books_to_scan.values() for book in books}
            if candidate not in all_signed_books:
                from_lib_books.append(candidate)
                unscanned.remove(candidate)
                delta_fitness += book_scores.get(candidate, 0)
                break

        clone.fitness += delta_fitness
        return clone

    def get_library_with_scanned_book(self, solution: SolutionRepresentation, book_id: int):
        for lib_id, books in solution.books_to_scan.items():
            if book_id in books:
                return lib_id
        return None