import os
from greedy_with_calculated_initial.models import Results
from greedy_with_calculated_initial.solution import Utils, InitialSolutionGenerator, SolutionOutputWriter
from greedy_with_calculated_initial.solution.InstanceProvider import InstanceProvider
from greedy_with_calculated_initial.solution.Solution import MultiRepresentationSolution
from ils.models import Solver, Parser
from ils.validator.multiple_validator import validate_all_solutions
from ils.validator.validator import validate_solution


solver = Solver()
multi_representation_solution = MultiRepresentationSolution()
directory = os.listdir('./input')
results = []
results_ils = []
output_dir = './output'
os.makedirs(output_dir, exist_ok=True)
version = "v1"

multi_representation_solution_path = "./output/multi_representation/final/" + version + "/"
initial_solution_ils_path = "./output/ils/initial/" + version + "/"
final_solution_ils_path = "./output/ils/final/" + version + "/"
results_summary_path = "./results/" + version + "/"

output_file_paths = [
    (multi_representation_solution_path, "multirepresentation_solution"),
    (initial_solution_ils_path, "initial_solution_ils"),
    (final_solution_ils_path, "final_solution_ils")]


def main():
    file_names = Utils.get_input_file_names()
    for file_name in file_names:
        # file_name = "B50_L5_D4.txt"
        path = Utils.get_input_file_paths(file_name)
        print(f"Calculating results for: {file_name}")
        instance = InstanceProvider.get_instance(path)
        solution = InitialSolutionGenerator.generate_initial_solution(instance)
        initial_score = solution.fitness
        print(f"Initial solution for instance: {file_name}, score: {solution.fitness}")


        improved_solution = multi_representation_solution.hill_climbing(solution.clone(), instance, 10000)
        multi_representation_score = improved_solution.fitness
        print(
            f"Solution for instance: {file_name}, score: {improved_solution.fitness}, from solution with representations v2")
        SolutionOutputWriter.write_solution_to_file(improved_solution, multi_representation_solution_path + file_name)
        results_ils.append((file_name, "multirepresentation_solution",  improved_solution.fitness))

        parser = Parser(f'./input/{file_name}')
        data = parser.parse()
        ils_solution_converted = Utils.convert_solution(instance, improved_solution.clone())
        os.makedirs(os.path.dirname(initial_solution_ils_path), exist_ok=True)
        ils_solution_converted.export(f'{initial_solution_ils_path}/{file_name}')
        results_ils.append((file_name, "ils_solution_converted",  ils_solution_converted.fitness_score))

        final_ils_solution = solver.iterated_local_search(data, ils_solution_converted)
        os.makedirs(os.path.dirname(final_solution_ils_path), exist_ok=True)
        final_ils_solution.export(f'{final_solution_ils_path}/{file_name}')

        fitness = final_ils_solution.fitness_score
        results.append(Results(file_name, "ils", initial_score, multi_representation_score, fitness))
        os.path.isfile(final_solution_ils_path + file_name)
        results_ils.append((file_name, "final_ils_solution",  fitness))

        print(f"ils Fitness for instance {file_name} is : {fitness}")
        solutionsValidationsForIteration(output_file_paths, file_name)


    all_solution_validations(output_file_paths)
    Utils.write_results(results, version)

def solutionsValidationsForIteration(file_paths:[str], file_name:str):
        print("\nValidating all solutions...")
        for file_path, name in file_paths:
            input_path = "./input/" + file_name
            output_path = file_path+ file_name
            result = validate_solution(input_path, output_path, True)
            print(result)

def all_solution_validations(file_paths:[str]):
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
