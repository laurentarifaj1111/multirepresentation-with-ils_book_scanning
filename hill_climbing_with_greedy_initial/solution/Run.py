import random
import time

from hill_climbing_with_greedy_initial.models.Results import Results
from hill_climbing_with_greedy_initial.solution.InitialGenerator import InitialSolutionGenerator
from hill_climbing_with_greedy_initial.solution.InstanceProvider import InstanceProvider
from hill_climbing_with_greedy_initial.solution.Operators import ReorderLibsTweakOperator, ShuffleLibsTweakOperator, \
    ReplaceLibsTweakOperator, SwapBooksTweakOperator
from hill_climbing_with_greedy_initial.solution.OutputWriter import SolutionOutputWriter
from hill_climbing_with_greedy_initial.solution.Solution import HillClimbing
from hill_climbing_with_greedy_initial.solution.TweakOperatorParams import TweakOperatorParams
from hill_climbing_with_greedy_initial.models.Instance import Instance
from hill_climbing_with_greedy_initial.models.SolutionRepresentation import SolutionRepresentation
from hill_climbing_with_greedy_initial.solution.Utils import Utils

solver = HillClimbing()


def main():
    results = []
    file_names = Utils.get_input_file_names()
    for file_name in file_names:
        path = Utils.get_input_file_paths(file_name)

        # Generate initial
        print(f"Calculating results for: {file_name}")
        instance = InstanceProvider.get_instance(path)
        solution = InitialSolutionGenerator.generate_initial_solution(instance)

        # Run with hill climbing for 1000 iterations
        improved_solution = solver.hill_climbing(solution.clone(), instance, 1000)

        # Write solution
        SolutionOutputWriter.write_solution_to_file(improved_solution, "hill_climbing" + file_name, "/hill_climbing/")

        Utils.write_results(results, "v1")


if __name__ == "__main__":
    main()
