from .cycle import Cycle
from copy import deepcopy


class Population(object):

    def __init__(self, cycle: Cycle, size: int):
        self.__cycles = []
        for i in range(size):
            random_cycle = deepcopy(cycle)
            random_cycle.randomize()
            self.__cycles.append(random_cycle)

        for cycle in self.__cycles:
            print(cycle.get_length())

    def get_the_best(self) -> Cycle:
        fittest = min(self.__cycles)
        print(fittest.get_length())
        return fittest
