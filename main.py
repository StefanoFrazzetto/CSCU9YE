from Algorithms import AlgorithmType
from TestRunner import TestRunner
from Utils import File

dir_path = File.get_current_dir()  # Get current dir
File.change_dir(dir_path)  # Change the working directory so we can read the file

ncolors, colours = File.read_file('colours.txt')  # Total number of colours and list of colours

tr = TestRunner(colours)

# Requirement 1
tr.add_run_configuration(AlgorithmType.GREEDY_CONSTRUCTIVE, 100, 30)
tr.add_run_configuration(AlgorithmType.GREEDY_CONSTRUCTIVE, 500, 30)

# Requirement 2
tr.add_run_configuration(AlgorithmType.HILL_CLIMBING, 100, 30)
tr.add_run_configuration(AlgorithmType.HILL_CLIMBING, 500, 30)

# Requirement 3
# #   - 30 starts
# #   - Compute mean, median, STD
tr.add_run_configuration(AlgorithmType.MULTI_START_HC, 100, 30)
tr.add_run_configuration(AlgorithmType.MULTI_START_HC, 500, 30)
#
# # Requirement 4
# #   - 30 starts
# #   - Compute mean, median, STD
# IMPORTANT: Time required for DELTA SORT: ~16 minutes. #
tr.add_run_configuration(AlgorithmType.DELTA_SORT, 100, 30)
tr.add_run_configuration(AlgorithmType.DELTA_SORT, 500, 30)

tr.configure()
tr.run()
tr.plot_all()
