from math import sqrt


class Colour(object):
    def __init__(self, red: float, green: float, blue: float):
        self.red = float(red)
        self.green = float(green)
        self.blue = float(blue)

    @staticmethod
    def __rgb_convert(value):
        return value * 255

    def distance_from(self, colour: 'Colour'):
        return sqrt(
            (self.red - colour.red)**2 +
            (self.green - colour.green)**2 +
            (self.blue - colour.green)**2
        )

    @staticmethod
    def list_from_tuple_list(colours_list) -> list:
        colours = []
        for element in colours_list:
            colour = Colour(element[0], element[1], element[2])
            colours.append(colour)
        return colours

    def to_rgb(self):
        """
        Convert the colour to RGB.
        :return:
        """
        return self.__rgb_convert(self.red), self.__rgb_convert(self.green), self.__rgb_convert(self.blue)
