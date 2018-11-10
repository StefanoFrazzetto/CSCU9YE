import Utils
from Algorithms import Algorithm, AlgorithmType, GreedyConstructive
from Colour import ColoursList

dir_path = Utils.get_current_dir()  # Get current dir
Utils.change_dir(dir_path)  # Change the working directory so we can read the file

ncolors, colours = Utils.read_file('colours.txt')  # Total number of colours and list of colours

test_size = 100  # Size of the subset of colours for testing
test_colours = colours[0:test_size]  # list of colours for testing

colours_list = ColoursList.list_from_tuple_list(test_colours)

cl = colours_list.random_permutation(test_size)
Utils.plot_colours_improved(cl)

# GC
algorithm = Algorithm.factory(AlgorithmType.GREEDY_CONSTRUCTIVE, GreedyConstructive.DistanceMethod.EUCLIDEAN)
algorithm.load_colours_list(cl)
cl_s = algorithm.find_solution()
Utils.plot_colours_improved(cl_s)

# HC
algorithm = Algorithm.factory(AlgorithmType.HILL_CLIMBING, 50000)
algorithm.load_colours_list(cl)
cl_s = algorithm.find_solution()
Utils.plot_colours_improved(cl_s)

# MSHC
algorithm = Algorithm.factory(AlgorithmType.MULTI_START_HC, 50000)
algorithm.load_colours_list(cl)
cl_s = algorithm.find_solution()
Utils.plot_colours_improved(cl_s)

# CUSTOM
algorithm = Algorithm.factory(AlgorithmType.CUSTOM_ALGORITHM)
algorithm.load_colours_list(cl)
cl_s = algorithm.find_solution()
Utils.plot_colours_improved(cl_s)
