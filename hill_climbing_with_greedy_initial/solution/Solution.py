import random
import time
from hill_climbing_with_greedy_initial.solution.Operators import ReorderLibsTweakOperator, ShuffleLibsTweakOperator, \
    ReplaceLibsTweakOperator, SwapBooksTweakOperator
from hill_climbing_with_greedy_initial.solution.TweakOperatorParams import TweakOperatorParams
from hill_climbing_with_greedy_initial.models.Instance import Instance
from hill_climbing_with_greedy_initial.models.SolutionRepresentation import SolutionRepresentation


class HillClimbing:
    def hill_climbing(self, current_solution: SolutionRepresentation, instance_value: Instance,
                      iterations: int) -> SolutionRepresentation:
        reorder_libs = ReorderLibsTweakOperator()
        shuffle_libs = ShuffleLibsTweakOperator()
        replace_libs = ReplaceLibsTweakOperator()
        swap_books = SwapBooksTweakOperator()

        operators = [replace_libs, shuffle_libs, reorder_libs, ]
        rand = random.Random()

        params = TweakOperatorParams.from_solution(current_solution, instance_value)
        currentTime = (time.time()) * 1000 + 150000
        iteration = 0
        while currentTime > time.time() * 1000 and iteration < iterations:
            iteration += 1
            for _ in range(iterations):
                operator = rand.choice(operators)
            if operator is swap_books:
                new_solution = operator.tweak(current_solution.clone(), instance_value, params)
            else:
                new_solution = operator.tweak(current_solution.clone(), instance_value)

            if new_solution.fitness > current_solution.fitness:
                current_solution = new_solution

        return current_solution
