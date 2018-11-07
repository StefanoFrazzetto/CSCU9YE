from math import sqrt


class Colour(object):
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    @staticmethod
    def __rgb_convert(value):
        return value * 255

    def distance_from(self, colour: 'Colour'):
        return sqrt(
            (self.red - colour.red)**2 +
            (self.green - colour.green)**2 +
            (self.blue - colour.green)**2
        )

    def to_rgb(self):
        """
        Convert the colour to RGB.
        :return:
        """
        return self.__rgb_convert(self.red), self.__rgb_convert(self.green), self.__rgb_convert(self.blue)
