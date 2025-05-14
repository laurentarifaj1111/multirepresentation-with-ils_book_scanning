import json
import os
from collections import OrderedDict
from typing import List, Dict

from ils.models import Solution
from ils.models.library import Library
from hill_climbing_with_greedy_initial.models.Instance import Instance
from hill_climbing_with_greedy_initial.models.SolutionRepresentation import SolutionRepresentation


current_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(current_dir, '../', '../'))
input_dir = os.path.join(root_dir, 'input')

class Utils:

    @staticmethod
    def generate_solution_for_libs_listed(instance: Instance, libs: List[int]) -> SolutionRepresentation:
        solution = SolutionRepresentation()
        libs_map: Dict[int, Library] = {lib.id: lib for lib in instance.libraries}
        current_day = 0
        total_days = instance.scanning_days
        unique_books = set(instance.get_unique_books())

        for lib_id in libs:
            selected_books = []
            unselected_books = []
            score = 0
            library = libs_map[lib_id]

            unique_per_lib = [book for book in library.books if book.id in unique_books]
            sorted_books = sorted(unique_per_lib, key=lambda b: b.score, reverse=True)

            current_day += library.signup_time
            remaining_days = total_days - current_day
            max_books = remaining_days * library.books_per_day

            for book in sorted_books:
                if len(selected_books) < max_books:
                    selected_books.append(book.id)
                    unique_books.remove(book.id)
                    score += book.score
                else:
                    unselected_books.append(book.id)

            if len(unselected_books) > 0:
                solution.books_to_scan[library.id] = selected_books
            solution.unscanned_books[library.id] = unselected_books
            solution.fitness += score

        return solution

    @staticmethod
    def swap_by_index(map_obj: Dict[int, List[int]], index1: int, index2: int) -> List[int]:
        keys = list(map_obj.keys())
        keys[index1], keys[index2] = keys[index2], keys[index1]
        return keys

    @staticmethod
    def convert_solution(instance: Instance, current_solution: SolutionRepresentation) -> Solution:
        signed_libraries = list(current_solution.books_to_scan.keys())
        unsigned_libraries = list(current_solution.get_unsigned_libraries(instance))
        scanned_books_per_library = current_solution.books_to_scan
        scanned_books = set(current_solution.get_books_to_scann())
        fitness_score = current_solution.fitness
        solution_v1 = Solution(signed_libraries, unsigned_libraries, scanned_books_per_library, scanned_books)
        solution_v1.fitness_score = fitness_score
        return solution_v1

    @staticmethod
    def convert_solution_to_v2(current_solution: Solution, instance: Instance) -> SolutionRepresentation:
        solution_v2 =  SolutionRepresentation()
        unscanned_books = OrderedDict()

        scanned_books_per_library = OrderedDict(current_solution.scanned_books_per_library)

        for lib in instance.libraries:
            if lib.id in scanned_books_per_library:
                unscanned_books[lib.id] = set(lib.books) - set(scanned_books_per_library[lib.id])
            else:
                unscanned_books[lib.id] = set(lib.books)

        solution_v2.books_to_scan = scanned_books_per_library
        solution_v2.unscanned_books = unscanned_books
        solution_v2.fitness = current_solution.fitness_score
        return solution_v2

    @staticmethod
    def get_input_file_paths(filename: str) -> str:
        return os.path.join(input_dir, filename)

    @staticmethod
    def get_input_file_names() -> list[str]:
        return [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    @staticmethod
    def write_results(results:list, version:str ) -> None:
        # Convert to list of dicts
        print(results)
        results_dict_list = [
            {
                "instance_name": r.instance_name,
                "combination": r.combination,
                "fitness": r.version1_score
            }
            for r in results
        ]
        file_name = version + "_results.json";
        print(f"Writing to: {os.path.abspath(file_name)}")
        with open( file_name, "w", encoding="utf-8") as f:
            json.dump(results_dict_list, f, indent=4)