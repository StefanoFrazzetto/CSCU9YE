import random

import Utils
from Algorithms import Algorithm, AlgorithmType
from Colour import Colour, ColoursList

dir_path = Utils.get_current_dir()  # Get current dir
Utils.change_dir(dir_path)  # Change the working directory so we can read the file

ncolors, colours = Utils.read_file('colours.txt')  # Total number of colours and list of colours

test_size = 200  # Size of the subset of colours for testing
test_colours = colours[0:test_size]  # list of colours for testing

colours_list = ColoursList.list_from_tuple_list(test_colours)

# perm = random.sample(range(test_size), test_size)
# # produces random pemutation of lenght test_size, from the numbers 0 to test_size -1
# Utils.plot_colours(test_colours, perm)


cl = colours_list.random_permutation(test_size)
Utils.plot_colours_improved(cl)

algorithm = Algorithm.factory(AlgorithmType.GREEDY_CONSTRUCTIVE)
algorithm.load_colours_list(cl)
cl_s = algorithm.get_solution(200)
Utils.plot_colours_improved(cl_s)
