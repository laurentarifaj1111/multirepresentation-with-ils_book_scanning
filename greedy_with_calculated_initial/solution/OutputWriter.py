import os

from greedy_with_calculated_initial.models.SolutionRepresentation import SolutionRepresentation


class SolutionOutputWriter:
    @staticmethod
    def write_solution_to_file(solution: SolutionRepresentation, file_path: str):
        # full_path = os.path.join("output", run_version, file_path)

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, 'w') as writer:
                writer.write(f"{len(solution.books_to_scan)}\n")

                for library_id, books in solution.books_to_scan.items():
                    # First line: library_id and number of books
                    writer.write(f"{library_id} {len(books)}\n")

                    # Second line: book IDs space-separated
                    if books:
                        writer.write(" ".join(map(str, books)) + "\n")
                    else:
                        writer.write("\n")
        except IOError as e:
            print(f"Error writing solution to file: {e}")
