import abc
import copy
import threading
from enum import Enum
from functools import total_ordering
from typing import List

import Utils
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
    run_time: float
    total_distance: float

    def __init__(self, colours: ColoursList, run_time: float, total_distance: float = None):
        self.colours = colours
        self.run_time = run_time
        self.total_distance = colours.get_total_distance() if total_distance is None else total_distance

    def __eq__(self, other: 'AlgorithmSolution'):
        return self.colours == other.colours and \
               self.total_distance == other.total_distance and \
               self.run_time == other.run_time

    def __lt__(self, other: 'AlgorithmSolution'):
        return self.total_distance < other.total_distance


class Algorithm(threading.Thread, metaclass=abc.ABCMeta):
    colours: ColoursList
    solutions: List[AlgorithmSolution]

    def __init__(self, *args):
        threading.Thread.__init__(self)
        self.colours = ColoursList()
        self.solutions = []

        # Debug
        self.debug = True

        # Performance
        self.start_time = Utils.get_timestamp_millis()
        self.end_time = 0
        self.run_time = 0
        self.total_distance = 0
        self.results = []

    @staticmethod
    def factory(algorithm_type: AlgorithmType, *args) -> 'Algorithm':
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

    @abc.abstractmethod
    def find_solution(self, *args):
        pass

    def get_algorithm_name(self) -> str:
        return self.__class__.__name__

    def get_solutions(self) -> List[AlgorithmSolution]:
        assert self.solutions is not None, "No solutions have been found yet."
        return self.solutions

    def get_best_solution(self):
        sorted(self.solutions)
        return self.solutions[-1]

    def __calculate_run_time(self):
        """
        Get the running time by subtracting end time from start time.
        :return: the algorithm running time in microseconds.
        """
        seconds = Utils.millis_to_seconds(self.end_time, self.start_time)
        return float("{0:.2f}".format(seconds))

    def load_colours_list(self, colours_list: ColoursList):
        self.colours = colours_list.clone()

    def run(self, *args):
        self.find_solution(*args)
        self.end_time = self.end_time = Utils.get_timestamp_millis()
        self.run_time = self.__calculate_run_time()
        self.__save_solution()

    def __save_solution(self):
        solution = AlgorithmSolution(self.colours, self.run_time, self.total_distance)
        self.solutions.append(solution)


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

        self.solutions.append(solution)


class HillClimbing(Algorithm):
    temp_solution: ColoursList

    def __init__(self, iterations: int = 1):
        super(HillClimbing, self).__init__()
        self.iterations = iterations
        self.best_solution = None
        self.temp_solution = None

    def load_colours_list(self, colours_list: ColoursList):
        super(HillClimbing, self).load_colours_list(colours_list)

        # Get a random permutation as best first solution
        self.best_solution = self.__get_random_permutation()

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
        return self.colours.random_permutation(len(self.colours))

    def find_solution(self):
        # TODO: Working, but replaced with else
        # # Go back to original state
        # self.temp_solution = self.best_solution.clone()

        self.temp_solution = self.best_solution.clone()
        best_solution_distance = self.temp_solution.get_total_distance()

        for i in range(self.iterations):
            index1, index2 = self.__get_random_indexes()
            self.__swap_colours(index1, index2)

            current_solution_distance = self.temp_solution.get_total_distance()
            if current_solution_distance < best_solution_distance:
                if self.debug:
                    print("Better solution found!")
                    print(f"Previous distance: {best_solution_distance} - New distance: {current_solution_distance}")
                self.solutions.append(self.temp_solution.clone())
                best_solution_distance = current_solution_distance
            else:
                # Not improving; go back to previous state
                self.temp_solution = self.best_solution.clone()


class MultiStartHillClimbing(Algorithm):
    def __init__(self, starts, hill_climbing_iterations):
        super(MultiStartHillClimbing, self).__init__()
        self.starts = starts
        self.hill_climbing_iterations = hill_climbing_iterations

    def find_solution(self):
        algorithm = Algorithm.factory(AlgorithmType.HILL_CLIMBING, self.hill_climbing_iterations)
        algorithm.load_colours_list(self.colours)
        for i in range(self.starts):
            algorithm.find_solution()
            self.solutions.append(algorithm.get_best_solution())


class CustomAlgorithm(Algorithm):
    def __init__(self):
        super(CustomAlgorithm, self).__init__()

    def find_solution(self):
        algo2 = Algorithm.factory(AlgorithmType.GREEDY_CONSTRUCTIVE, GreedyConstructive.DistanceMethod.DELTA_E)
        algo2.load_colours_list(self.colours)
        algo2.find_solution()
        self.solutions.append(algo2.get_best_solution())
