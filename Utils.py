import os

import matplotlib.pyplot as plt
import numpy as np


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
