import os
import time

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


class Assert:
    @staticmethod
    def not_empty(obj: list, message: str = None):
        assert len(obj) > 0, "The list is empty." if message is None else message

    @staticmethod
    def not_none(obj, message: str = None):
        assert obj is not None, "The object value is None." if message is None else message

    @staticmethod
    def same_length(obj1, obj2, message: str = None):
        assert len(obj1) == len(obj2), "The objects have different lengths" if message is None else message


class Time:
    @staticmethod
    def get_timestamp_millis():
        return int(round(time.time() * 1000))

    @staticmethod
    def millis_to_seconds(time1, time2):
        if time1 < time2:
            time1, time2 = time2, time1
        return (time1 - time2) / 1000


class File:
    @staticmethod
    def get_current_dir():
        return os.path.dirname(os.path.realpath(__file__))

    # Reads the file  of colours
    # Returns the number of colours in the file and a list with the colours (RGB) values

    @staticmethod
    def change_dir(path):
        os.chdir(path)

    @staticmethod
    def read_file(fname):
        with open(fname, 'r') as afile:
            lines = afile.readlines()
        n = int(lines[3])  # number of colours  in the file
        colours = []
        lines = lines[4:]  # colors as rgb values
        for l in lines:
            rgb = l.split()
            colours.append(rgb)
        return n, colours


class Plot:
    @staticmethod
    def __save_plot(figure: Figure, filename: str, subset_size: int):
        figure.savefig(f"./results/{filename}_{subset_size}", bbox_inches='tight')

    @staticmethod
    def colours(colours: list, total_distance: float = None, algorithm_name: str = None, run_time: float = None):
        ratio = 10  # ratio of line height/width, e.g. colour lines will have height 10 and width 1
        img = np.zeros((ratio, len(colours), 3))
        for i in range(len(colours)):
            img[:, i, :] = colours[i].to_tuple()

        fig, axes = plt.subplots(1, figsize=(8, 4))  # figsize=(width,height) handles window dimensions
        axes.imshow(img, interpolation='nearest')
        axes.axis('off')

        line_y_coefficient = (len(colours) / 100)
        line1_y = 18 * line_y_coefficient
        line2_y = 20 * line_y_coefficient
        line3_y = 22 * line_y_coefficient
        line4_y = 24 * line_y_coefficient

        plt.text(0, line1_y, f"Colours subset size: {len(colours)}")

        if algorithm_name is not None:
            plt.text(0, line2_y, f"Algorithm: {algorithm_name}")

        formatted_distance = "{0:.2f}".format(total_distance)
        plt.text(0, line3_y, f"Total distance (euclidean): {formatted_distance}")

        if run_time is not None:
            plt.text(0, line4_y, f"Algorithm running time: {run_time} s")

        Plot.__save_plot(fig, algorithm_name if algorithm_name is not None else "Subset", len(colours))
