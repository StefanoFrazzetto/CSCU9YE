import copy
import random
from _ctypes import Union
from functools import total_ordering
from math import inf
from typing import List

import numpy as np
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import sRGBColor, LabColor

import Utils


@total_ordering
class Colour(object):
    # BUILT-IN METHODS
    def __init__(self, red: float, green: float, blue: float):
        self.red = float(red)
        self.green = float(green)
        self.blue = float(blue)

    def __eq__(self, other: 'Colour'):
        return self.distance_from(other) == 0

    def __lt__(self, other: 'Colour'):
        return self.distance_from(self.get_white()) < other.distance_from(self.get_white())

    def __str__(self):
        return str(self.to_tuple())

    # PRIVATE METHODS
    def __to_lbc(self):
        return convert_color(sRGBColor(self.red, self.green, self.blue), LabColor)

    # STATIC METHODS
    @staticmethod
    def calculate_distance(colour1: 'Colour', colour2: 'Colour') -> float:
        s = (colour1.red - colour2.red) ** 2 + (colour1.green - colour2.green) ** 2 + (colour1.blue - colour2.blue) ** 2
        return s ** (1 / 2) if s > 0 else 0

    @staticmethod
    def get_white():
        return Colour(1, 1, 1)

    @staticmethod
    def __rgb_convert(value):
        return value * 255

    # PUBLIC METHODS

    def clone(self):
        return Colour(self.red, self.green, self.blue)

    def distance_from(self, colour: 'Colour'):
        return self.calculate_distance(self, colour)

    def to_delta_e(self, other: 'Colour'):
        return delta_e_cie2000(self.__to_lbc(), other.__to_lbc())

    def to_rgb(self):
        """
        Convert the colour to RGB.
        :return:
        """
        return self.__rgb_convert(self.red), self.__rgb_convert(self.green), self.__rgb_convert(self.blue)

    def to_tuple(self):
        return self.red, self.green, self.blue


class ColoursList(object):
    colours: List[Colour]

    # BUILT-IN METHODS
    def __init__(self):
        self.colours = []
        self.total_distance = None

    def __contains__(self, item):
        for element in self.colours:
            if element == item:
                return True
        return False

    def __delitem__(self, key):
        index = self.colours.index(key)
        del self.colours[index]

    def __eq__(self, other):
        for i in range(len(self)):
            if self.get(i) != other.get(i):
                return False
        return True

    def __getitem__(self, index):
        return self.colours[index]

    def __len__(self):
        return len(self.colours)

    def __setitem__(self, key, value):
        self.colours[key] = value

    def __str__(self):
        for colour in self.get_all():
            return colour

    # PRIVATE METHODS

    # PUBLIC METHODS

    def append(self, colour: Colour):
        """Append a colour to the list"""
        self.colours.append(colour)

    def clone(self):
        colours = ColoursList()
        for colour in self:
            colours.append(colour.clone())
        return colours

    def get(self, index: int):
        assert index is not None
        return self.colours[index]

    def get_all(self) -> list:
        return self.colours

    def get_index(self, colour: Colour):
        return self.colours.index(colour)

    def get_random_element(self):
        return random.choice(self.colours)

    def get_nearest_colour_delta_e(self, colour: Colour) -> (Colour, float):
        total_distance = 0
        min_distance = inf
        nearest_colour = Colour(50, 50, 50)
        for current_colour in self.colours:
            current_distance = current_colour.to_delta_e(colour)
            if current_distance < min_distance:
                nearest_colour = current_colour
                min_distance = current_distance
                total_distance += min_distance
        return nearest_colour, total_distance

    def get_nearest_colour_euclidean(self, colour: Colour) -> (Colour, float):
        total_distance = 0
        min_distance = inf
        nearest_colour = Colour(50, 50, 50)
        for current_colour in self.colours:
            current_distance = current_colour.distance_from(colour)
            if current_distance < min_distance:
                nearest_colour = current_colour
                min_distance = current_distance
                total_distance += min_distance
        return nearest_colour, total_distance

    def get_total_distance(self) -> float:
        if self.total_distance is not None:
            return self.total_distance

        self.total_distance = 0
        for i in range(len(self) - 1):
            self.total_distance += self.get(i).distance_from(self.get(i + 1))
        return self.total_distance

    def index(self, element):
        return self.colours.index(element)

    def pop_random(self):
        colour = random.choice(self.colours)
        del self[colour]
        return colour

    def random_permutation(self, size) -> 'ColoursList':
        new_list = ColoursList()
        permutation = Utils.get_permutation(size)
        for i in range(size):
            permutation_element = permutation[i]
            colour = self.get(permutation_element)
            new_list.append(colour)
        return new_list

    def slice(self, start_index: int = 0, end_index: int = None):
        """Return a slice of the list"""
        return self.colours[start_index:end_index]

    def sort(self):
        return np.sort(self.colours)


class ColourUtils:

    @staticmethod
    def get_list_copy(colours_list: list):
        return copy.deepcopy(colours_list)

    @staticmethod
    def get_random_index(colours_list: list):
        colour = random.choice(colours_list)
        return colours_list.index(colour)

    @staticmethod
    def list_from_tuple_list(colours_list: list) -> ColoursList:
        colours = ColoursList()
        for element in colours_list:
            colour = Colour(element[0], element[1], element[2])
            colours.append(colour)
        return colours

    @staticmethod
    def get_total_distance(colours_list: list):
        total = 0
        for i in range(len(colours_list) - 1):
            total += Colour.calculate_distance(colours_list[i], colours_list[i + 1])
        return total
