import random
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

    def __to_lbc(self):
        return convert_color(sRGBColor(self.red, self.green, self.blue), LabColor)

    @staticmethod
    def get_white():
        return Colour(1, 1, 1)

    @staticmethod
    def __rgb_convert(value):
        return value * 255

    def distance_from(self, colour: 'Colour'):
        s = (self.red - colour.red) ** 2 + (self.green - colour.green) ** 2 + (self.blue - colour.blue) ** 2
        return s ** (1 / 3) if s > 0 else 0

    def to_rgb(self):
        """
        Convert the colour to RGB.
        :return:
        """
        return self.__rgb_convert(self.red), self.__rgb_convert(self.green), self.__rgb_convert(self.blue)

    def to_tuple(self):
        return self.red, self.green, self.blue

    def delta_e(self, other: 'Colour'):
        return delta_e_cie2000(self.__to_lbc(), other.__to_lbc())


class ColoursList(object):
    colours: List[Colour]

    def __init__(self):
        self.colours = []

    def __getitem__(self, index):
        return self.colours[index]

    def __delitem__(self, key):
        index = self.colours.index(key)
        del self.colours[index]

    def __contains__(self, item):
        for element in self.colours:
            if element == item:
                return True
        return False

    def __len__(self):
        return len(self.colours)

    def __str__(self):
        for colour in self.get_all():
            print(colour)

    def index(self, element):
        return self.colours.index(element)

    def append(self, colour: Colour):
        """Append a colour to the list"""
        self.colours.append(colour)

    def slice(self, start_index: int = 0, end_index: int = None):
        """Return a slice of the list"""
        return self.colours[start_index:end_index]

    def get(self, index: int):
        assert index is not None
        return self.colours[index]

    def get_all(self) -> list:
        return self.colours

    def sort(self):
        return np.sort(self.colours)

    def get_nearest_colour(self, colour: Colour) -> (Colour, float):
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

    def get_total_distance(self):
        total = 0
        for i in range(len(self) - 1):
            total = self.get(i).distance_from(self.get(i + 1))
        return total

    def random_sample(self, elements) -> List[Colour]:
        return random.sample(self.colours, elements)

    def random_permutation(self, size) -> 'ColoursList':
        new_list = ColoursList()
        permutation = Utils.get_permutation(size)
        for i in range(len(self)):
            new_list.append(self.get(permutation[i]))
        return new_list

    def pop_random(self):
        colour = random.choice(self.colours)
        del self[colour]
        return colour

    def get_random_element(self):
        return random.choice(self.colours)

    @staticmethod
    def list_from_tuple_list(colours_list: list) -> 'ColoursList':
        colours = ColoursList()
        for element in colours_list:
            colour = Colour(element[0], element[1], element[2])
            colours.append(colour)
        return colours
