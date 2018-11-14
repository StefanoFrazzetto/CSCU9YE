import abc
import copy
from enum import Enum
from functools import total_ordering
from typing import List

import Utils
from Utils import Assert
from Colour import ColoursList


class AlgorithmType(Enum):
    GREEDY_CONSTRUCTIVE = 0,
    HILL_CLIMBING = 1,
    MULTI_START_HC = 2,
    CUSTOM_ALGORITHM = 3


@total_ordering
class AlgorithmSolution(object):
    """
    The solution found by the algorithm.
    """
    colours: ColoursList
    total_distance: float

    def __init__(self, colours: ColoursList, total_distance: float = None):
        self.colours = colours
        self.total_distance = colours.get_total_distance() if total_distance is None else total_distance

    def __eq__(self, other: 'AlgorithmSolution'):
        return self.colours == other.colours and \
               self.total_distance == other.total_distance

    def __lt__(self, other: 'AlgorithmSolution'):
        return self.total_distance < other.total_distance


class Algorithm(metaclass=abc.ABCMeta):
    colours: ColoursList
    solutions: List[AlgorithmSolution]

    HILL_CLIMBING_ITERATIONS = 1000

    def __init__(self, *args):
        self.colours = ColoursList()
        self.solutions = []
        self.iterations = 0

        # Debug
        self.debug = False

        # Performance
        self.__start_time = 0
        self.__end_time = 0
        self.run_time = 0
        self.total_distance = 0

    @staticmethod
    def factory(algorithm_type: AlgorithmType, *args) -> 'Algorithm':
        """Define factory method for algorithms."""
        assert algorithm_type in AlgorithmType, f"Unrecognised algorithm {algorithm_type.name}"

        if algorithm_type == AlgorithmType.GREEDY_CONSTRUCTIVE:
            return GreedyConstructive(
                distance_method=args[0] if len(args) > 0 else GreedyConstructive.DistanceMethod.EUCLIDEAN)

        if algorithm_type == AlgorithmType.HILL_CLIMBING:
            return HillClimbing()

        if algorithm_type == AlgorithmType.MULTI_START_HC:
            return MultiStartHillClimbing()

        if algorithm_type == AlgorithmType.CUSTOM_ALGORITHM:
            return CustomAlgorithm()

    @abc.abstractmethod
    def find_solution(self, *args):
        pass

    def get_algorithm_name(self) -> str:
        return self.__class__.__name__

    def get_solutions(self) -> List[AlgorithmSolution]:
        Assert.not_empty(self.solutions, "No solutions have been found yet.")
        sorted(self.solutions)
        return self.solutions

    def get_best_solution(self):
        return self.get_solutions()[-1]

    def get_run_time(self):
        """
        Get the running time by subtracting end time from start time.
        :return: the algorithm running time in microseconds.
        """
        seconds = Utils.millis_to_seconds(self.__end_time, self.__start_time)
        return float("{0:.2f}".format(seconds))

    def load_colours_list(self, colours_list: ColoursList):
        self.colours = colours_list.clone()

    def run(self, iterations: int):
        self.iterations = iterations
        self.__start_time = Utils.get_timestamp_millis()
        for _ in range(self.iterations):
            self.find_solution()
        self.__end_time = Utils.get_timestamp_millis()
        self.run_time = self.get_run_time()

    def save_solution(self, solution: ColoursList or AlgorithmSolution):
        if type(solution) is ColoursList:
            self.solutions.append(AlgorithmSolution(solution))
        elif type(solution) is AlgorithmSolution:
            self.solutions.append(solution)
        else:
            assert "Trying to save wrong type of solution."


class GreedyConstructive(Algorithm):
    class DistanceMethod(Enum):
        EUCLIDEAN = 0,
        DELTA_E = 1

    def __init__(self, distance_method: DistanceMethod = DistanceMethod.EUCLIDEAN):
        super(GreedyConstructive, self).__init__()
        self.distance_method = distance_method

    def find_solution(self):
        colours = copy.deepcopy(self.colours)
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

        self.solutions.append(AlgorithmSolution(solution, solution.get_total_distance()))


class HillClimbing(Algorithm):
    temp_solution: ColoursList

    def __init__(self):
        super(HillClimbing, self).__init__()
        self.is_initialized = False
        self.best_solution = self.temp_solution = None
        self.best_solution_distance = None

    @staticmethod
    def __invert_range(colours_list: ColoursList, start, end):
        colours_list.colours[start:end] = colours_list[start:end][::-1]

    @staticmethod
    def __swap_colours(colours: ColoursList, index1, index2):
        colours[index1], colours[index2] = colours[index2], colours[index1]

    @staticmethod
    def __get_random_indexes(colours: ColoursList) -> (int, int):
        """
        Get two random indexes from self.temp_solution ensuring that index1 < index2.
        :return: int index1, int index2
        """
        colour1 = colours.get_random_element()
        colour2 = colours.get_random_element()

        # Ensure that the elements are different
        while colour1 == colour2:
            colour2 = colours.get_random_element()

        index1 = colours.get_index(colour1)
        index2 = colours.get_index(colour2)

        # Swap indexes if index1 > index2
        if index1 > index2:
            index1, index2 = index2, index1

        return index1, index2

    def __get_random_permutation(self):
        return self.colours.random_permutation(len(self.colours))

    def find_solution(self):
        # TODO Check if all clone calls are necessary.
        for _ in range(self.HILL_CLIMBING_ITERATIONS):
            if self.is_initialized is False:
                self.best_solution = self.temp_solution = self.colours.clone()
                self.best_solution_distance = self.best_solution.get_total_distance()
                self.save_solution(self.best_solution)
                self.is_initialized = True

            index1, index2 = self.__get_random_indexes(self.best_solution)
            self.__swap_colours(self.temp_solution, index1, index2)
            temp_solution_distance = self.temp_solution.get_total_distance()

            if self.temp_solution.get_total_distance() < self.best_solution_distance:
                if self.debug:
                    print(f"Previous distance: {self.best_solution_distance} - New distance: {temp_solution_distance}")
                self.best_solution = self.temp_solution.clone()
                self.save_solution(self.best_solution)
                self.best_solution_distance = temp_solution_distance
            else:
                # Not improving; go back to previous state
                self.temp_solution = self.best_solution.clone()


class MultiStartHillClimbing(Algorithm):
    def __init__(self):
        super(MultiStartHillClimbing, self).__init__()

    def find_solution(self):
        algorithm = Algorithm.factory(AlgorithmType.HILL_CLIMBING)
        algorithm.load_colours_list(self.colours)
        algorithm.find_solution()
        self.save_solution(algorithm.get_best_solution())


class CustomAlgorithm(Algorithm):
    def __init__(self):
        super(CustomAlgorithm, self).__init__()

    def find_solution(self):
        algorithm = Algorithm.factory(AlgorithmType.GREEDY_CONSTRUCTIVE, GreedyConstructive.DistanceMethod.DELTA_E)
        algorithm.load_colours_list(self.colours)
        algorithm.find_solution()
        self.save_solution(algorithm.get_best_solution())
