from Algorithms import AlgorithmType
from Colour import ColoursList
from TestRunner import TestRunner, Benchmark
from Utils import File

dir_path = File.get_current_dir()  # Get current dir
File.change_dir(dir_path)  # Change the working directory so we can read the file

ncolors, colours = File.read_file('colours.txt')  # Total number of colours and list of colours

# colours_100 = ColoursList.random_permutation(colours, 100)
# colours_500 = ColoursList.random_permutation(colours, 500)
#
# bench1 = Benchmark(AlgorithmType.GREEDY_CONSTRUCTIVE, colours_100)

tr = TestRunner(colours)

tr.add_run_configuration(AlgorithmType.GREEDY_CONSTRUCTIVE, 100, 10)
tr.add_run_configuration(AlgorithmType.HILL_CLIMBING, 100, 10)
tr.add_run_configuration(AlgorithmType.MULTI_START_HC, 100, 10)
tr.add_run_configuration(AlgorithmType.CUSTOM_ALGORITHM, 100, 10)

# tr.add_run_configuration(AlgorithmType.GREEDY_CONSTRUCTIVE, 500, 10)
# tr.add_run_configuration(AlgorithmType.HILL_CLIMBING, 500, 10)
# tr.add_run_configuration(AlgorithmType.MULTI_START_HC, 500, 10)
# tr.add_run_configuration(AlgorithmType.GREEDY_COCUSTOM_ALGORITHMNSTRUCTIVE, 500, 10)

tr.configure()
tr.run()
