import random
import time

from greedy_with_calculated_initial.models.Results import Results
from greedy_with_calculated_initial.solution.InitialGenerator import InitialSolutionGenerator
from greedy_with_calculated_initial.solution.InstanceProvider import InstanceProvider
from greedy_with_calculated_initial.solution.Operators import ReorderLibsTweakOperator, ShuffleLibsTweakOperator, ReplaceLibsTweakOperator
from greedy_with_calculated_initial.solution.OutputWriter import SolutionOutputWriter
from greedy_with_calculated_initial.solution.TweakOperatorParams import TweakOperatorParams
from ils.models import Parser, SolverModified
from greedy_with_calculated_initial.models.Instance import Instance
from greedy_with_calculated_initial.models.SolutionRepresentation import SolutionRepresentation
from greedy_with_calculated_initial.solution.Utils import Utils


# def main():
#     file_names = Utils.get_input_file_names()
#     # for file_name in file_names:
#     file_name = "B6k_L35_D70.in"
#     path = Utils.get_input_file_paths(file_name)
#     print(f"Calculating results for: {file_name}")
#     instance = InstanceProvider.get_instance(path)
#     solution = InitialSolutionGenerator.generate_initial_solution(instance)
#     print(f"Initial solution for instance: {file_name}, score: {solution.fitness}")
#
#     improved_solution = hill_climbing(solution.clone(), instance, 50000)
#
#     print(f"Solution for instance: {file_name}, score: {improved_solution.fitness}, from solution with representations v2")
#
#     solver = SolverModified()
#     data = Parser(path).parse()
#     solution_v1 = Utils.convert_solution(instance, improved_solution.clone())
#     fitness, sol = solver.iterated_local_search(data, solution_v1)
#     print(f"Solution for instance: {file_name}, score: {solution_v1.fitness_score}, from solution with representations v1")
#
#     print(f"Final Fitness for instance {file_name} is : {fitness}")
#     SolutionOutputWriter.write_solution_to_file(improved_solution, file_name, "v1")
def main():
        results = []
    # file_names = Utils.get_input_file_names()
    # already_executed = Utils.get_already_run_file_names()
    # for file_name in (f for f in file_names if f not in already_executed):
        file_name = "B50_L5_D4.txt"
        path = Utils.get_input_file_paths(file_name)
        print(f"Calculating results for: {file_name}")
        instance = InstanceProvider.get_instance(path)
        solution = InitialSolutionGenerator.generate_initial_solution(instance)
        initial_score = solution.fitness
        print(f"Initial solution for instance: {file_name}, score: {solution.fitness}")

        improved_solution = hill_climbing(solution.clone(), instance, 10000)
        other_representation_score = improved_solution.fitness
        print(f"Solution for instance: {file_name}, score: {improved_solution.fitness}, from solution with representations v2")
        SolutionOutputWriter.write_solution_to_file(improved_solution, "other-representation" + file_name, "test/other-representation/")

        solver = SolverModified()
        data = Parser(path).parse()
        solution_v1 = Utils.convert_solution(instance, improved_solution.clone())
        solution_v1.export("./output/test/initial/" + "initial" + file_name)

        fitness, sol = solver.variable_neighborhood_search(data, solution_v1)

        print(f"Solution for instance: {file_name}, score: {solution_v1.fitness_score}, from solution with representations v1")
        # fitness = sol.fitness_score
        results.append(Results(file_name, "variable_neighborhood_search",  initial_score, other_representation_score, fitness))
        sol.export("./output/test/final/" + "final-solution" +file_name)


        print(f"Final Fitness for instance {file_name} is : {fitness}")

        SolutionOutputWriter.write_solution_to_file(improved_solution, file_name, "test/validation")

        Utils.write_results(results, "v9")


def hill_climbing(current_solution: SolutionRepresentation, instance_value: Instance, iterations: int) -> SolutionRepresentation:
    reorder_libs = ReorderLibsTweakOperator()
    shuffle_libs = ShuffleLibsTweakOperator()
    replace_libs = ReplaceLibsTweakOperator()
    # swap_books = SwapBooksTweakOperator()

    operators = [replace_libs, shuffle_libs, reorder_libs, ]
    rand = random.Random()

    params = TweakOperatorParams.from_solution(current_solution, instance_value)
    currentTime = (time.time()) * 1000 + 150000
    iteration = 0
    while currentTime > time.time()*1000 and iteration < iterations:
        iteration += 1
    # for _ in range(iterations):
        operator = rand.choice(operators)
        # if operator is swap_books:
        #     new_solution = operator.tweak(current_solution.clone(), instance_value, params)
        # else:
        new_solution = operator.tweak(current_solution.clone(), instance_value)

        if new_solution.fitness > current_solution.fitness:
            current_solution = new_solution

    return current_solution

if __name__ == "__main__":
    main()
