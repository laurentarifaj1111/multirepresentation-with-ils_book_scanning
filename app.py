import os
import time

from hill_climbing_with_greedy_initial.models import Results
from hill_climbing_with_greedy_initial.solution import Utils, InitialSolutionGenerator, SolutionOutputWriter
from hill_climbing_with_greedy_initial.solution.InstanceProvider import InstanceProvider
from hill_climbing_with_greedy_initial.solution.Solution import HillClimbing
from ils.models import Solver, Parser
from ils.models.initial_solution import InitialSolution
from ils.validator.multiple_validator import validate_all_solutions
from ils.validator.validator import validate_solution


solver = Solver()
multi_representation_solution = HillClimbing()
directory = os.listdir('./input')
results = []
results_ils = []
output_dir = 'output/output'
os.makedirs(output_dir, exist_ok=True)
version = "v1"

multi_representation_solution_path = "./output/multi_representation/final/" + version + "/"
initial_solution_ils_path = "./output/ils/initial/" + version + "/"
solutions_path = "./output/ils/" + version + "/"
results_summary_path = "./results/" + version + "/"
results_summary_path = "output/output/multi_representation/final/v1/"

output_file_paths = [
    (solutions_path, "final_solution_ils")
]

def main():
    file_names = Utils.get_input_file_names()
    for file_name in file_names:
        ten_minute_from_now = (time.time()) * 1000 + 600000
        path = Utils.get_input_file_paths(file_name)
        # Read Instance
        instance = InstanceProvider.get_instance(path)
        copy_of_ils_solution = None

        # Generate Initial Solution using guided initial solution
        solution = InitialSolutionGenerator.generate_initial_solution(instance)
        parser = Parser(f'./input/{file_name}')
        data = parser.parse()

        while ten_minute_from_now > time.time() * 1000:
            # Apply hill climbing for 100 iterations
            hill_climbing_solution = multi_representation_solution.hill_climbing(solution.clone(), instance, 100)

            # Convert to other ils representation
            ils_solution_converted = Utils.convert_solution(instance, hill_climbing_solution.clone())

            # Apply iterated local search for 100 iterations
            ils_solution = solver.iterated_local_search(data, ils_solution_converted, max_iterations=100)

            # Convert to algorithm with greedy initial soultion representation
            solution = Utils.convert_solution_to_v2(ils_solution, instance)

            solutionsValidationsForIteration(output_file_paths, file_name)

        # Create directory and export
        os.makedirs(os.path.dirname(solutions_path), exist_ok=True)
        ils_solution.export(f'{solutions_path}/{file_name}')

        results.append(Results(file_name, "ils", solution.fitness))
        results_ils.append((file_name, "ils_solution_converted", solution.fitness))

    # Validate all solutions
    all_solution_validations(output_file_paths)


def solutionsValidationsForIteration(file_paths, file_name:str):
        print("\nValidating all solutions...")
        for file_path, name in file_paths:
            input_path = "./input/" + file_name
            output_path = file_path+ file_name
            result = validate_solution(input_path, output_path, True)
            print(result)

def all_solution_validations(file_paths):
    for file_path, algorithm_name in file_paths:
        validate_all_solutions(input_dir='./input', output_dir=file_path)

        # Print summary of all instances
        print("\nSummary of all instances:")
        print("-" * 50)
        print(f"{'Instance':<20} {'Score':>15}")
        print("-" * 50)
        for file, name,  score in results_ils:
            print(f"{file:<20} {score:>15,}")
        print("-" * 50)

        # Write summary to a text file
        summary_full_path = results_summary_path + name  + "/"
        os.makedirs(os.path.dirname(summary_full_path), exist_ok=True)
        summary_file = os.path.join(summary_full_path, 'summary_results.txt')
        with open(summary_file, 'w+') as f:
            f.write("Summary of all instances:\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Instance':<20} {'Algorithm':<40} {'Score':>15}\n")
            f.write("-" * 80 + "\n")
            for file, name,  score in results_ils:
                f.write(f"{file:<20} {name:<40} {score:>15,}\n")
            f.write("-" * 80 + "\n")
        print(f"\nSummary has been written to: {summary_file}")


if __name__ == "__main__":
    main()
