from TestRunner import TestRunner
from Utils import File

dir_path = File.get_current_dir()  # Get current dir
File.change_dir(dir_path)  # Change the working directory so we can read the file

ncolors, colours = File.read_file('colours.txt')  # Total number of colours and list of colours

# cl = colours_list.random_permutation(test_size)
# Utils.plot_colours_improved(cl)

tr = TestRunner(colours)
tr.add_run_configuration(100, 1)
# tr.add_run_configuration(500, 30)
tr.configure()
tr.run()
# tr.get_statistics()
