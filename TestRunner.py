import threading
from typing import Dict

import numpy as np

from Algorithms import *
from Colour import ColoursList


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
    algorithm_types: Dict[AlgorithmType, Algorithm]
    benchmarks: List[Benchmark]
    test_run_configurations: List[TestRunConfiguration]

    def __init__(self, colours: ColoursList):
        self.colours = colours
        self.test_run_configurations = []
        self.threads = []
        self.benchmarks = []

        # self.algorithm_types = [algorithm for algorithm in AlgorithmType]
        self.algorithm_types = [AlgorithmType.HILL_CLIMBING]

    def add_run_configuration(self, subset_size: int, iterations: int):
        trc = TestRunConfiguration(subset_size, iterations)
        self.test_run_configurations.append(trc)

    def configure(self):
        for test_run in self.test_run_configurations:
            for algorithm_type in self.algorithm_types:
                benchmark = Benchmark(algorithm_type, self.colours, test_run.subset_size, test_run.iterations)
                self.benchmarks.append(benchmark)

    def run(self):
        # Start all the benchmarks in parallel
        for benchmark in self.benchmarks:
            print(f"Starting benchmark for {benchmark.algorithm.get_algorithm_name()}")
            benchmark.start()
            self.threads.append(benchmark)

        # Wait for all threads to finish
        for thread in self.threads:
            thread.join()

        print("All threads finished. Plotting results...")

        for benchmark in self.benchmarks:
            Utils.plot_colours_improved(benchmark.colours)
            Utils.plot_from_algorithm(benchmark.algorithm)
