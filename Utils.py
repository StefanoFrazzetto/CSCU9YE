import os
import random
import time

import matplotlib.pyplot as plt
import numpy as np

from Algorithms import Algorithm
from Colour import ColoursList


def get_timestamp_millis():
    return int(round(time.time() * 1000))


def millis_to_seconds(time1, time2):
    return (time1 - time2) / 1000


def get_current_dir():
    return os.path.dirname(os.path.realpath(__file__))


def change_dir(path):
    os.chdir(path)


# Reads the file  of colours
# Returns the number of colours in the file and a list with the colours (RGB) values

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


# Display the colours in the order of the permutation in a pyplot window
# Input, list of colours, and ordering  of colours.
# They need to be of the same length

def plot_colours(colours, perm):
    assert len(colours) == len(perm)

    ratio = 10  # ratio of line height/width, e.g. colour lines will have height 10 and width 1
    img = np.zeros((ratio, len(colours), 3))
    for i in range(0, len(colours)):
        img[:, i, :] = colours[perm[i]]

    fig, axes = plt.subplots(1, figsize=(8, 4))  # figsize=(width,height) handles window dimensions
    axes.imshow(img, interpolation='nearest')
    axes.axis('off')
    plt.show()


def plot_from_algorithm(algorithm: Algorithm):
    plot_colours_improved(algorithm.get_best_solution().colours, algorithm)


def plot_colours_improved(colours: ColoursList, algorithm: Algorithm = None):
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

    if algorithm is not None:
        plt.text(0, line1_y, f"Algorithm: {algorithm.get_algorithm_name()}")
    formatted_distance = "{0:.2f}".format(colours.get_total_distance())
    plt.text(0, line2_y, f"Total distance (euclidean): {formatted_distance}")
    plt.show()


def get_permutation(size: int):
    return random.sample(range(size), size)
