import os
import time

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
output_dir = 'backup/output'
os.makedirs(output_dir, exist_ok=True)
version = "v8"

multi_representation_solution_path = "./output/multi_representation/final/" + version + "/"
initial_solution_ils_path = "./output/ils/initial/" + version + "/"
final_solution_ils_path = "./output/ils/final/" + version + "/"
results_summary_path = "./results/" + version + "/"
# results_summary_path = "./backup/output/multi_representation/final/v1/"

output_file_paths = [
    # (multi_representation_solution_path, "multirepresentation_solution"),
    # (initial_solution_ils_path, "initial_solution_ils"),
    (final_solution_ils_path, "final_solution_ils")]


# def main():
#     # optimum_solutions = [
#     #     "B2.5k_L3_D90 (Appalachian Regional Project).txt",
#     #     "B18k_L4_D365 (Oxford Bodleian Archives).txt",
#     #     "B3k_L1_D1.4k (Vatican Secret Archives Project).txt",
#     #     "B50_L5_D4.txt",
#     #     "B70_L8_D7.txt",
#     #     "B80_L7_D9.txt",
#     #     "B90_L6_D11.txt",
#     #     "B95_L5_D12.txt",
#     #     "B96_L6_D14.txt",
#     #     "B98_L4_D15.txt",
#     #     "B99_L7_D16.txt",
#     #     "B100_L9_D18.txt",
#     #     "B150_L8_D10.txt",
#     #     "B300_L11_D20.txt",
#     #     "B500_L14_D18.txt",
#     #     "B750_L20_D14.txt",
#     #     "B1k_L18_D17.txt",
#     #     "B1.5k_L20_D40.txt",
#     #     "B4k_L30_D60.txt",
#     #     "B6k_L35_D70.txt",
#     #     "B9k_L40_D80.txt"
#     # ]
#     # file_names = Utils.get_input_file_names()
#     # for file_name in (f for f in file_names if f not in optimum_solutions):
#         file_name = "B1.5k_L20_D40.txt"
#         path = Utils.get_input_file_paths(file_name)
#         print(f"Calculating results for: {file_name}")
#         instance = InstanceProvider.get_instance(path)
#         solution = InitialSolutionGenerator.generate_initial_solution(instance)
#         initial_score = solution.fitness
#         print(f"Initial solution for instance: {file_name}, score: {solution.fitness}")
#
#
#         improved_solution = multi_representation_solution.hill_climbing(solution.clone(), instance, 10000)
#         multi_representation_score = improved_solution.fitness
#         print(
#             f"Solution for instance: {file_name}, score: {improved_solution.fitness}, from solution with representations v2")
#         SolutionOutputWriter.write_solution_to_file(improved_solution, multi_representation_solution_path + file_name)
#         results_ils.append((file_name, "multirepresentation_solution",  improved_solution.fitness))
#
#         parser = Parser(f'./input/{file_name}')
#         data = parser.parse()
#         ils_solution_converted = Utils.convert_solution(instance, improved_solution.clone())
#         os.makedirs(os.path.dirname(initial_solution_ils_path), exist_ok=True)
#         # ils_solution_converted.export(f'{initial_solution_ils_path}/{file_name}')
#         results_ils.append((file_name, "ils_solution_converted",  ils_solution_converted.fitness_score))
#
#
#         final_ils_solution = solver.iterated_local_search(data, ils_solution_converted, max_iterations=100)
#         os.makedirs(os.path.dirname(final_solution_ils_path), exist_ok=True)
#         final_ils_solution.export(f'{final_solution_ils_path}/{file_name}')
#         print("convertin to multi rep solution")
#         sol2 = Utils.convert_solution_to_v2(final_ils_solution, instance)
#         print("final score:", sol2.fitness)
#         new_solution = multi_representation_solution.hill_climbing(sol2, instance, 100)
#         ils_v2 = Utils.convert_solution(instance, new_solution.clone())
#         ils_v2.export(f'{final_solution_ils_path}/{file_name}')
#
#
#         fitness = final_ils_solution.fitness_score
#         results.append(Results(file_name, "ils", initial_score, multi_representation_score, fitness))
#         os.path.isfile(final_solution_ils_path + file_name)
#         results_ils.append((file_name, "final_ils_solution",  fitness))
#
#         print(f"ils Fitness for instance {file_name} is : {fitness}")
#         solutionsValidationsForIteration(output_file_paths, file_name)
#
#
#     # all_solution_validations(output_file_paths)
#     # Utils.write_results(results, version)


def main():
    optimum_solutions = [
        "B2.5k_L3_D90 (Appalachian Regional Project).txt",
        "B18k_L4_D365 (Oxford Bodleian Archives).txt",
        "B3k_L1_D1.4k (Vatican Secret Archives Project).txt",
        "B50_L5_D4.txt",
        "B70_L8_D7.txt",
        "B80_L7_D9.txt",
        "B90_L6_D11.txt",
        "B95_L5_D12.txt",
        "B96_L6_D14.txt",
        "B98_L4_D15.txt",
        "B99_L7_D16.txt",
        "B100_L9_D18.txt",
        "B150_L8_D10.txt",
        "B300_L11_D20.txt",
        "B500_L14_D18.txt",
        "B750_L20_D14.txt",
        "B1k_L18_D17.txt",
        "B1.5k_L20_D40.txt",
        "B4k_L30_D60.txt",
        "B6k_L35_D70.txt",
        "B9k_L40_D80.txt"
    ]
    file_names = Utils.get_input_file_names()
    for file_name in (f for f in file_names if f not in optimum_solutions):
        current_time = (time.time()) * 1000 + 600000
        # file_name = "B1k_L18_D17.txt"
        path = Utils.get_input_file_paths(file_name)
        instance = InstanceProvider.get_instance(path)
        solution = InitialSolutionGenerator.generate_initial_solution(instance)
        print(f"Initial solution for instance: {file_name}, score: {solution.fitness}")
        parser = Parser(f'./input/{file_name}')
        data = parser.parse()

        while current_time > time.time() * 1000:
            try:
                print(f"Calculating with other representation: {file_name}")
                improved_solution = multi_representation_solution.hill_climbing(solution.clone(), instance, 100)
                print(f"Solution for instance: {file_name}, score: {improved_solution.fitness}, from solution with representations v2")

                ils_solution_converted = Utils.convert_solution(instance, improved_solution.clone())
                final_ils_solution = solver.iterated_local_search(data, ils_solution_converted, max_iterations=100)
                print("ils score:", final_ils_solution.fitness_score)
                os.makedirs(os.path.dirname(final_solution_ils_path), exist_ok=True)
                final_ils_solution.export(f'{final_solution_ils_path}/{file_name}')

                print("converting to other rep solution")
                solution = Utils.convert_solution_to_v2(final_ils_solution, instance)

                solutionsValidationsForIteration(output_file_paths, file_name)
            except Exception as e:
                print(e)
                break

        results.append(Results(file_name, "ils",   solution.fitness))
        results_ils.append((file_name, "ils_solution_converted",  solution.fitness))


    all_solution_validations(output_file_paths)
    Utils.write_results(results, version)


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
    # all_solution_validations(output_file_paths)
    main()
