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
        self.solution = None
        self.debug = True

    @staticmethod
    def factory(algorithm_type: AlgorithmType, *args):
        """Define factory method for algorithms."""
        assert algorithm_type in AlgorithmType, f"Unrecognised algorithm {algorithm_type.name}"

        if algorithm_type == AlgorithmType.GREEDY_CONSTRUCTIVE:
            return GreedyConstructive(distance_method=args[0])

        if algorithm_type == AlgorithmType.HILL_CLIMBING:
            return HillClimbing(iterations=args[0])

        if algorithm_type == AlgorithmType.MULTI_START_HC:
            return MultiStartHillClimbing(starts=args[0], hill_climbing_iterations=args[1])

        if algorithm_type == AlgorithmType.CUSTOM_ALGORITHM:
            return CustomAlgorithm()

    def load_colours_list(self, colours_list: ColoursList):
        self.colours_list = colours_list.clone()

    def get_solution(self):
        assert self.solution is not None, "The solution has not been found yet."
        return self.solution

    def get_algorithm_name(self) -> str:
        return self.__class__.__name__

    @abc.abstractmethod
    def find_solution(self, *args):
        pass


class GreedyConstructive(Algorithm):
    class DistanceMethod(Enum):
        EUCLIDEAN = 0,
        DELTA_E = 1

    def __init__(self, distance_method: DistanceMethod = DistanceMethod.EUCLIDEAN):
        super(GreedyConstructive, self).__init__()
        self.distance_method = distance_method

    def find_solution(self):
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

        self.solution = solution


class HillClimbing(Algorithm):
    solution: ColoursList
    temp_solution: ColoursList

    def __init__(self, iterations: int = 1):
        super(HillClimbing, self).__init__()
        self.iterations = iterations
        self.temp_solution = None

    def load_colours_list(self, colours_list: ColoursList):
        super(HillClimbing, self).load_colours_list(colours_list)
        self.solution = self.__get_random_permutation()
        self.temp_solution = self.solution.clone()

    @staticmethod
    def __invert_range(colours_list: ColoursList, start, end):
        colours_list.colours[start:end] = colours_list[start:end][::-1]

    def __swap_colours(self, index1, index2):
        self.temp_solution[index1], self.temp_solution[index2] = self.temp_solution[index2], self.temp_solution[index1]

    def __get_random_indexes(self) -> (int, int):
        """
        Get two random indexes from self.temp_solution ensuring that index1 < index2.
        :return: int index1, int index2
        """
        colour1 = self.temp_solution.get_random_element()
        colour2 = self.temp_solution.get_random_element()

        # Ensure that the elements are different
        while colour1 == colour2:
            colour2 = self.temp_solution.get_random_element()

        index1 = self.temp_solution.get_index(colour1)
        index2 = self.temp_solution.get_index(colour2)

        # Swap indexes if index1 > index2
        if index1 > index2:
            index1, index2 = index2, index1

        return index1, index2

    def __get_random_permutation(self):
        return self.colours_list.random_permutation(len(self.colours_list))

    def find_solution(self):
        best_solution_distance = self.temp_solution.get_total_distance()

        for i in range(self.iterations):
            # Go back to original state
            self.temp_solution = self.solution.clone()

            index1, index2 = self.__get_random_indexes()
            self.__swap_colours(index1, index2)

            current_solution_distance = self.temp_solution.get_total_distance()
            if current_solution_distance < best_solution_distance:
                if self.debug:
                    print("Better solution found!")
                    print(f"Previous distance: {best_solution_distance} - New distance: {current_solution_distance}")
                self.solution = self.temp_solution.clone()
                best_solution_distance = current_solution_distance


class MultiStartHillClimbing(Algorithm):
    def __init__(self, starts, hill_climbing_iterations):
        super(MultiStartHillClimbing, self).__init__()
        self.starts = starts
        self.hill_climbing_iterations = hill_climbing_iterations

    def find_solution(self):
        algorithm = Algorithm.factory(AlgorithmType.HILL_CLIMBING, self.hill_climbing_iterations)
        algorithm.load_colours_list(self.colours_list)
        solutions = []
        for i in range(self.starts):
            algorithm.find_solution()
            solutions.append(algorithm.get_solution())

        solutions = sorted(solutions, key=lambda sol: sol.get_total_distance())
        self.solution = solutions[0]


class CustomAlgorithm(Algorithm):
    def __init__(self):
        super(CustomAlgorithm, self).__init__()

    def find_solution(self):
        algo2 = Algorithm.factory(AlgorithmType.GREEDY_CONSTRUCTIVE, GreedyConstructive.DistanceMethod.DELTA_E)
        algo2.load_colours_list(self.colours_list)
        algo2.find_solution()
        self.solution = algo2.get_solution()
