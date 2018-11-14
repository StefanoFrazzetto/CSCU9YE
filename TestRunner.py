import threading
from functools import total_ordering
from typing import Dict, List

import numpy as np

from Algorithms import Algorithm, AlgorithmType
from Colour import ColoursList, ColourUtils
from Utils import Assert, Time, Plot


class Benchmark(threading.Thread):
    """
    Benchmark class to test a single algorithm over a number of iterations using a subset of colours.
    """
    algorithm: Algorithm
    colours: ColoursList

    def __init__(self, algorithm_type: AlgorithmType, colours: ColoursList, subset_size: int, iterations: int):
        threading.Thread.__init__(self)
        self.algorithm = Algorithm.factory(algorithm_type)  # the algorithm to run
        self.colours = colours.random_permutation(subset_size)  # the colours to use to run the benchmark
        self.test_results = []  # the results for each run
        self.iterations = iterations  # number of times to run

    def run(self):
        self.algorithm.load_colours_list(self.colours)
        self.algorithm.run(self.iterations)
        self.test_results.append(TestResult.from_algorithm(self.algorithm))

    def get_statistics(self):
        Assert.not_empty(self.test_results, "No results to generate statistics for.")
        distances = [result.best_distance for result in self.test_results]
        return np.mean(distances), np.mean(distances), np.std(distances)


@total_ordering
class TestResult(object):
    def __init__(self):
        self.subset_size = 0
        self.total_run_time = 0
        self.best_distance = 0

    def __eq__(self, other: 'TestResult'):
        return self.subset_size == other.subset_size and \
               self.total_run_time == other.total_run_time and \
               self.best_distance == other.best_distance

    def __lt__(self, other: 'TestResult'):
        return self.best_distance < other.best_distance

    @staticmethod
    def from_algorithm(algorithm: Algorithm):
        tr = TestResult()
        tr.total_run_time = algorithm.get_run_time()
        tr.best_distance = algorithm.get_best_solution().total_distance


class TestRunConfiguration(object):
    def __init__(self, subset_size: int, iterations: int = 1):
        self.subset_size = subset_size
        self.iterations = iterations


class TestRunner(object):
    """
    TestRunner handles the benchmarking process for the chosen algorithms.
    It creates a new Benchmark for each test to be run, and runs each one
    of them using a separate thread.
    """
    algorithm_types: Dict[AlgorithmType, Algorithm]
    benchmarks: List[Benchmark]
    run_configurations: List[TestRunConfiguration]

    def __init__(self, colours: list):
        self.colours = ColourUtils.list_from_tuple_list(colours)
        self.run_configurations = []
        self.threads = []
        self.benchmarks = []

        self.algorithm_types = [algorithm for algorithm in AlgorithmType]
        # self.algorithm_types = [AlgorithmType.HILL_CLIMBING]

    def add_run_configuration(self, subset_size: int, iterations: int):
        """
        Add a new test run configuration.
        :param subset_size: the size of the subset of colours to use.
        :param iterations: the number of times the algorithm has to be run.
        """
        trc = TestRunConfiguration(subset_size, iterations)
        self.run_configurations.append(trc)

    def configure(self):
        for test_run in self.run_configurations:
            for algorithm_type in self.algorithm_types:
                benchmark = Benchmark(algorithm_type, self.colours, test_run.subset_size, test_run.iterations)
                self.benchmarks.append(benchmark)

    # def __generate_results(self):
    #     Salve results to test_results

    def __plot_benchmarks(self):
        print("Plotting results...")

        starting_subsets = []
        for benchmark in self.benchmarks:
            if len(benchmark.colours) not in starting_subsets:
                # Plot the starting colours once for each colour subset
                starting_subsets.append(len(benchmark.colours))
                Plot.colours(
                    benchmark.colours.get_all(),
                    benchmark.colours.get_total_distance()
                )

            Plot.colours(
                benchmark.algorithm.get_best_solution().get_colours(),
                benchmark.algorithm.get_best_solution().get_total_distance(),
                benchmark.algorithm.get_algorithm_name(),
                benchmark.algorithm.get_run_time()
            )

    def run(self):
        """
        Run all the benchmarks using the provided test run configurations.
        """
        Assert.not_empty(self.benchmarks, "The benchmarks list cannot be empty. Please add run configurations.")

        timestamp_start = Time.get_timestamp_millis()

        # Start all the benchmarks in parallel
        for benchmark in self.benchmarks:
            print(f"Starting benchmark for {benchmark.algorithm.get_algorithm_name()}")
            benchmark.start()
            self.threads.append(benchmark)

        # Wait for all threads to finish
        for thread in self.threads:
            thread.join()

        timestamp_end = Time.get_timestamp_millis()
        running_time = Time.millis_to_seconds(timestamp_end, timestamp_start)
        print(f"All threads finished in {running_time} s")

        self.__plot_benchmarks()

    def get_statistics(self):
        for benchmark in self.benchmarks:
            benchmark.get_statistics()