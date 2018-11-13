from typing import List, Dict

from Algorithms import *
from Colour import ColoursList


class TestRunConfiguration(object):
    def __init__(self, subset_size: int, run_count: int = 1):
        self.subset_size = subset_size
        self.run_count = run_count


class TestRunner(object):
    algorithms: Dict[AlgorithmType, Algorithm]
    test_run_configurations: List[TestRunConfiguration]

    HILL_CLIMBING_ITERATIONS = 50000
    MULTI_START_ITERATIONS = 25000
    MULTI_START_STARTS = 30

    def __init__(self, colours: ColoursList):
        self.colours = colours
        self.test_run_configurations = []

        self.threads = []

        self.algorithms = {
            AlgorithmType.GREEDY_CONSTRUCTIVE: Algorithm.factory(
                AlgorithmType.GREEDY_CONSTRUCTIVE,
                GreedyConstructive.DistanceMethod.EUCLIDEAN
            ),

            AlgorithmType.HILL_CLIMBING: Algorithm.factory(
                AlgorithmType.HILL_CLIMBING,
                self.HILL_CLIMBING_ITERATIONS
            ),

            AlgorithmType.MULTI_START_HC: Algorithm.factory(
                AlgorithmType.MULTI_START_HC,
                self.MULTI_START_STARTS,
                self.MULTI_START_ITERATIONS
            ),

            AlgorithmType.CUSTOM_ALGORITHM: Algorithm.factory(
                AlgorithmType.CUSTOM_ALGORITHM
            )
        }

    def add_run_configuration(self, subset_size: int):
        trc = TestRunConfiguration(subset_size)
        self.test_run_configurations.append(trc)

    def run(self):
        for test_run in self.test_run_configurations:
            test_run.subset_size

        # Start threads and append them to list
        for _, algorithm in self.algorithms:
            algorithm.start()
            self.threads.append(algorithm)

        # Wait for all the threads to finish
        for thread in self.threads:
            thread.join()

        print("All threads finished. Plotting results...")
