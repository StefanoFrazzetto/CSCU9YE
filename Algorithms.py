import abc
import copy
from enum import Enum

from Colour import ColoursList


class AlgorithmType(Enum):
    GREEDY_CONSTRUCTIVE = 0,
    HILL_CLIMBING = 1,
    MULTI_START_HC = 2,
    CUSTOM_ALGORITHM = 3


class Algorithm(metaclass=abc.ABCMeta):
    colours_list: ColoursList

    def __init__(self, *args):
        self.colours_list = ColoursList()

    @staticmethod
    def factory(algorithm_type: AlgorithmType, *args):
        """Define factory method for algorithms."""
        assert algorithm_type in AlgorithmType, f"Unrecognised algorithm {algorithm_type.name}"

        if algorithm_type == AlgorithmType.GREEDY_CONSTRUCTIVE:
            return GreedyConstructive(distance_method=args[0])

        if algorithm_type == AlgorithmType.HILL_CLIMBING:
            return HillClimbing(iterations=args[0])

        if algorithm_type == AlgorithmType.MULTI_START_HC:
            return MultiStartHillClimbing(iterations=args[0])

        if algorithm_type == AlgorithmType.CUSTOM_ALGORITHM:
            return CustomAlgorithm()

    def load_colours_list(self, colours_list: ColoursList):
        self.colours_list = copy.deepcopy(colours_list)

    @abc.abstractmethod
    def get_solution(self, *args) -> ColoursList:
        pass


class GreedyConstructive(Algorithm):
    class DistanceMethod(Enum):
        EUCLIDEAN = 0,
        DELTA_E = 1

    def __init__(self, distance_method: DistanceMethod = DistanceMethod.EUCLIDEAN):
        super(GreedyConstructive, self).__init__()
        self.distance_method = distance_method

    def get_solution(self):
        colours = copy.deepcopy(self.colours_list)
        solution = ColoursList()
        # Get a random colour
        current_colour = colours.pop_random()
        solution.append(current_colour)
        while len(colours) > 0:
            # Get the nearest colour to the current one
            current_colour, _ = colours.get_nearest_colour_euclidean(current_colour) \
                if self.distance_method == GreedyConstructive.DistanceMethod.EUCLIDEAN \
                else colours.get_nearest_colour_delta_e(current_colour)
            solution.append(current_colour)
            del colours[current_colour]
        return solution


class HillClimbing(Algorithm):
    def __init__(self, iterations: int = 1):
        super(HillClimbing, self).__init__()
        self.iterations = iterations

    def __invert_range(self, start, end):
        self.colours_list.colours[start:end] = self.colours_list[start:end][::-1]

    def get_solution(self) -> ColoursList:
        random_solution = self.colours_list.random_permutation(len(self.colours_list))
        while self.iterations > 0:
            random_colour1 = random_solution.get_random_element()
            random_colour2 = random_solution.get_random_element()

            # Ensure that the elements are different
            while random_colour1 == random_colour2:
                random_colour2 = random_solution.get_random_element()

            index_1 = self.colours_list.index(random_colour1)
            index_2 = self.colours_list.index(random_colour2)

            self.__invert_range(index_1, index_2)

            # One less to go...
            self.iterations -= 1
        return random_solution


class MultiStartHillClimbing(Algorithm):
    def __init__(self, iterations):
        super(MultiStartHillClimbing, self).__init__()
        self.iterations = iterations

    def get_solution(self) -> list:
        algo = Algorithm.factory(AlgorithmType.HILL_CLIMBING, 5000)
        algo.load_colours_list(self.colours_list)
        solutions = []
        while self.iterations > 0:
            solution = algo.get_solution()
            solutions.append(solution)
            self.iterations -= 1
        solutions = sorted(solutions, key=lambda sol: sol.get_total_distance())
        return solutions


class CustomAlgorithm(Algorithm):
    def __init__(self):
        super(CustomAlgorithm, self).__init__()

    def get_solution(self) -> ColoursList:
        algo2 = Algorithm.factory(AlgorithmType.GREEDY_CONSTRUCTIVE, GreedyConstructive.DistanceMethod.DELTA_E)
        algo2.load_colours_list(self.colours_list)
        return algo2.get_solution()


