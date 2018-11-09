import abc
from enum import Enum

from Colour import ColoursList


class AlgorithmType(Enum):
    GREEDY_CONSTRUCTIVE = 0,
    HILL_CLIMBING = 1,
    MULTI_START_HC = 2,
    CUSTOM_ALGORITHM = 3


class Algorithm(metaclass=abc.ABCMeta):
    colours_list: ColoursList

    def __init__(self):
        self.colours_list = ColoursList()

    @staticmethod
    def factory(algorithm_type: AlgorithmType):
        """Define factory method for algorithms."""
        assert algorithm_type in AlgorithmType, f"Unrecognised algorithm {algorithm_type.name}"

        if algorithm_type == AlgorithmType.GREEDY_CONSTRUCTIVE:
            return GreedyConstructive()

        if algorithm_type == AlgorithmType.HILL_CLIMBING:
            return HillClimbing()

        if algorithm_type == AlgorithmType.MULTI_START_HC:
            return MultiStartHillClimbing()

        if algorithm_type == AlgorithmType.CUSTOM_ALGORITHM:
            return CustomAlgorithm()

    def load_colours_list(self, colours_list: ColoursList):
        self.colours_list = colours_list

    @abc.abstractmethod
    def get_solution(self, *args) -> ColoursList:
        pass


class GreedyConstructive(Algorithm):
    def get_solution(self, iterations: int):
        colours = self.colours_list
        solution = ColoursList()
        # Get a random colour
        current_colour = colours.pop_random()
        solution.append(current_colour)
        while len(colours) > 0:
            # Get the nearest colour to the current one
            current_colour, _ = colours.get_nearest_colour(current_colour)
            solution.append(current_colour)
            del colours[current_colour]
        return solution

    def __init__(self):
        super(GreedyConstructive, self).__init__()


class HillClimbing(Algorithm):
    def __init__(self):
        super(HillClimbing, self).__init__()

    def get_solution(self, *args) -> ColoursList:
        pass


class MultiStartHillClimbing(Algorithm):
    def __init__(self):
        super(MultiStartHillClimbing, self).__init__()

    def get_solution(self, *args) -> ColoursList:
        pass


class CustomAlgorithm(Algorithm):
    def __init__(self):
        super(CustomAlgorithm, self).__init__()

    def get_solution(self, *args) -> ColoursList:
        pass
