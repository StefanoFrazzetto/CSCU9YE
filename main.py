import Utils
from Colour import ColourUtils
from TestRunner import TestRunner

dir_path = Utils.get_current_dir()  # Get current dir
Utils.change_dir(dir_path)  # Change the working directory so we can read the file

ncolors, colours = Utils.read_file('colours.txt')  # Total number of colours and list of colours

colours_list = ColourUtils.list_from_tuple_list(colours)

# cl = colours_list.random_permutation(test_size)
# Utils.plot_colours_improved(cl)

tr = TestRunner(colours_list)
tr.add_run_configuration(100, 30)
tr.add_run_configuration(500, 30)
tr.configure()
tr.run()
