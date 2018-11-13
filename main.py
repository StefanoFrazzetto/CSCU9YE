import Utils
from Algorithms import Algorithm, AlgorithmType, GreedyConstructive
from Colour import ColourUtils

dir_path = Utils.get_current_dir()  # Get current dir
Utils.change_dir(dir_path)  # Change the working directory so we can read the file

ncolors, colours = Utils.read_file('colours.txt')  # Total number of colours and list of colours

test_size = 500  # Size of the subset of colours for testing
test_colours = colours[0:test_size]  # list of colours for testing
hill_climbing_iterations = 50000
multi_start_hc_iterations = 25000
multi_start_hc_runs = 10
colours_list = ColourUtils.list_from_tuple_list(test_colours)

cl = colours_list.random_permutation(test_size)
Utils.plot_colours_improved(cl)

# tr = TestRunner(cl)
# tr.add_test_run_configuration(100, 5)
# tr.add_test_run_configuration(500, 5)
# tr.run()

# GC
algorithm = Algorithm.factory(AlgorithmType.GREEDY_CONSTRUCTIVE, GreedyConstructive.DistanceMethod.EUCLIDEAN)
algorithm.load_colours_list(cl)
algorithm.run()

# HC
algorithm = Algorithm.factory(AlgorithmType.HILL_CLIMBING, hill_climbing_iterations)
algorithm.load_colours_list(cl)
algorithm.run()

# MSHC
# 1. 10 - 25000
# 2. 20 - 125000
# 3. 5 - 50000

algorithm = Algorithm.factory(AlgorithmType.MULTI_START_HC, multi_start_hc_runs, hill_climbing_iterations)
algorithm.load_colours_list(cl)
algorithm.run()

# CUSTOM
algorithm = Algorithm.factory(AlgorithmType.CUSTOM_ALGORITHM)
algorithm.load_colours_list(cl)
algorithm.run()
