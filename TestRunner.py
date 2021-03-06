import threading
from functools import total_ordering
from typing import List

from Algorithms import Algorithm, AlgorithmType, AlgorithmSolution
from Colour import ColoursList, ColourUtils
from Utils import Assert, Time, Plot


class Benchmark(threading.Thread):
    """
    Benchmark class to test a single algorithm over a number of iterations using a subset of colours.
    """
    algorithm: Algorithm
    colours: ColoursList

    def __init__(self, algorithm_type: AlgorithmType, colours: ColoursList, subset_size: int, iterations: int):
        super().__init__()
        self.algorithm = Algorithm.factory(algorithm_type)  # the algorithm to run
        self.subset_size = subset_size
        self.colours = colours.random_permutation(subset_size)  # the colours to use to run the benchmark
        self.test_results = []  # the results for each run
        self.iterations = iterations  # number of times to run

    def get_distances(self):
        Assert.not_empty(self.test_results, "No results to generate statistics for.")
        return [result.get_distance() for result in self.test_results]

    def get_total_time(self):
        return self.algorithm.get_run_time()

    def __save_results(self):
        for solution in self.algorithm.get_solutions():
            self.test_results.append(TestResult.from_solution(solution))

    def run(self):
        self.algorithm.load_colours_list(self.colours)
        self.algorithm.run(self.iterations)
        self.__save_results()

    def plot_colours(self):
        Plot.colours(
            self.algorithm.get_best_solution().get_colours(),
            self.algorithm.get_best_solution().get_total_distance(),
            self.algorithm.get_algorithm_name(),
            self.algorithm.get_run_time()
        )

    def plot_distance_distribution(self):
        Plot.candlestick_distances(
            self.algorithm.get_algorithm_name(),
            self.get_distances(),
            self.subset_size,
            self.iterations
        )

    def plot_distance_progress(self):
        Plot.scatter_distances(
            self.algorithm.get_algorithm_name(),
            self.get_distances(),
            self.subset_size,
            self.iterations
        )


@total_ordering
class TestResult(object):
    def __init__(self):
        self.subset_size = 0
        self.total_distance = 0

    def __eq__(self, other: 'TestResult'):
        return self.subset_size == other.subset_size and \
               self.total_distance == other.total_distance

    def __lt__(self, other: 'TestResult'):
        return self.total_distance < other.total_distance

    @staticmethod
    def from_solution(solution: AlgorithmSolution):
        tr = TestResult()
        tr.subset_size = len(solution.get_colours())
        tr.total_distance = solution.get_total_distance()
        return tr

    def get_distance(self):
        return self.total_distance


class TestRunConfiguration(object):
    def __init__(self, algorithm_type: AlgorithmType, subset_size: int, iterations: int = 1):
        self.algorithm_type = algorithm_type
        self.subset_size = subset_size
        self.iterations = iterations


class TestRunner(object):
    """
    TestRunner handles the benchmarking process for the chosen algorithms.
    It creates a new Benchmark for each test to be run, and runs each one
    of them using a separate thread.
    """
    benchmarks: List[Benchmark]
    run_configurations: List[TestRunConfiguration]

    def __init__(self, colours: list):
        self.colours = ColourUtils.list_from_tuple_list(colours)
        self.run_configurations = []
        self.threads = []
        self.benchmarks = []
        self.algorithms = set()

    def add_run_configuration(self, algorithm_type: AlgorithmType, subset_size: int, iterations: int):
        """
        Add a new test run configuration.
        :param algorithm_type: the algorithm to be tested.
        :param subset_size: the size of the subset of colours to use.
        :param iterations: the number of times the algorithm has to be run.
        """
        trc = TestRunConfiguration(algorithm_type, subset_size, iterations)
        self.run_configurations.append(trc)
        self.algorithms.add(algorithm_type)

    def configure(self):
        for test_run in self.run_configurations:
            benchmark = Benchmark(test_run.algorithm_type, self.colours, test_run.subset_size, test_run.iterations)
            self.benchmarks.append(benchmark)

    def __plot_benchmarks(self):
        print("Plotting results...")

        starting_subsets = []
        for benchmark in self.benchmarks:
            if benchmark.subset_size not in starting_subsets:
                # Plot the starting colours once for each colour subset
                starting_subsets.append(len(benchmark.colours))
                Plot.colours(
                    benchmark.colours.get_all(),
                    benchmark.colours.get_total_distance()
                )

            benchmark.plot_colours()

    def plot_all(self):
        self.__plot_benchmarks()
        self.plot_distances()
    # def plot_run_times(self):
    #
    #     data = {}
    #     for benchmark in self.benchmarks:
    #         data[
    #             benchmark.subset_size, benchmark.iterations, benchmark.algorithm.get_algorithm_name()
    #         ] = benchmark.get_total_time()
    #
    #     graphics_values = []
    #     for run_configuration in self.run_configurations:
    #         algorithms = []
    #         iterations = []
    #         times = []
    #         for subset, alg_iterations, algorithm in data:
    #             if subset == run_configuration.subset_size and alg_iterations == run_configuration.iterations:
    #                 algorithms.append(algorithm)
    #                 times.append(data[subset, alg_iterations, algorithm])
    #                 iterations.append(alg_iterations)
    #         graphics_values.append((algorithms, iterations, times))
    #
    #     for algorithms, iterations, times in graphics_values:
    #         Plot.barchart(algorithms, times, iterations)

    def __start_benchmarks(self):
        # Start all the benchmarks in parallel
        for benchmark in self.benchmarks:
            print(f"Starting benchmark for {benchmark.algorithm.get_algorithm_name()}")
            benchmark.start()
            self.threads.append(benchmark)

        # Wait for all threads to finish
        for thread in self.threads:
            thread.join()

    def run(self):
        """
        Run all the benchmarks using the provided test run configurations.
        """
        Assert.not_empty(self.benchmarks, "The benchmarks list cannot be empty. Please add run configurations.")

        timestamp_start = Time.get_timestamp_millis()
        self.__start_benchmarks()
        timestamp_end = Time.get_timestamp_millis()
        running_time = Time.millis_to_seconds(timestamp_end, timestamp_start)
        print(f"All threads finished in {running_time} s")

    def get_benchmarks(self):
        return self.benchmarks

    def plot_distances(self):
        for benchmark in self.benchmarks:
            benchmark.plot_distance_distribution()
            benchmark.plot_distance_progress()
