from .cycle import Cycle

from typing import List
from copy import deepcopy


class Population(object):
    def __init__(self, cycles: List[Cycle] = None):
        self.__cycles = cycles if cycles else []

    def add_cycle(self, cycle: Cycle):
        self.__cycles.append(Cycle(cycle[:]))

    def remove_cycle(self, index) -> Cycle:
        return self.__cycles.pop(index)

    def rand_populate(self, seed: Cycle, size: int):
        for i in range(size):
            random_cycle = deepcopy(seed)
            random_cycle.randomize()
            self.__cycles.append(random_cycle)

    def __iter__(self):
        return PopulationIterator(self)

    def __getitem__(self, index: int):
        return self.__cycles[index]

    def get_iterator(self):
        return self.__iter__()

    def get_the_best(self) -> Cycle:
        fittest = min(self.__cycles)
        return fittest

    def get_cycles(self):
        return self.__cycles

    def get_cycle_size(self):
        return len(self.__cycles[0]) if self.__cycles else 0

    def __len__(self):
        return len(self.__cycles)

    def get_n_best(self, n: int):
        return Population(sorted(self.__cycles)[:n])


class PopulationIterator(object):
    def __init__(self, population: Population):
        self._population = population
        self._index = 0

    def next(self) -> Cycle:
        if self._index < len(self._population.get_cycles()):
            result = (self._population.get_cycles()[self._index])
            self._index += 1
            return result

        raise StopIteration

    def __next__(self):
        return self.next()

    def has_next(self) -> bool:
        return len(self._population) > self._index
