from model.city import City
from model.cycle import Cycle
from typing import List
import random
from model.population import Population
from enum import Enum


class MutationType(Enum):
    INSERTION = 0
    EXCHANGE = 1
    SCRUMBLE = 2


class Mutation():

    # lista cykli miast (populacja), typ mutacji, szansa mutacji
    def __init__(self, population: Population, mutation_type: MutationType, mutation_param: float):
        self._population = population
        self._cycle_size = population.get_cycle_size()
        self._mutation_type = mutation_type
        self._mutation_param = mutation_param

    # def _swap(self, cities: List[City], i: int, j: int) -> List[City]:
    #     cities[j], cities[i] = cities[i], cities[j]
    #     return cities

    def _insertion(self, cycle: Cycle) -> Cycle:
        random_index = random.randint(0, self._cycle_size - 1)  # wybieramy losowo jakies miasto z listy
        random_destination = random.randint(0, self._cycle_size - 1)  # wybieramy losowo kolejne miasto z listy, moze byc problem bo moze to byc to samo miasto
        while random_destination == random_index:
            random_destination = random.randint(0, self._cycle_size - 1)
        if random_index < random_destination:  # przesuwamy miasto pierwsze na miejsce drugiego, NIE ZAMIENIAMY ICH
            temp = cycle[random_index]
            for i in range(random_index, random_destination):
                cycle[i] = cycle[i + 1]
            cycle[random_destination] = temp
        else:
            temp = cycle[random_index]
            for i in range(random_index, random_destination, -1):
                cycle[i] = cycle[i - 1]
            cycle[random_destination] = temp
        return cycle

    # w cyklu zamieniamy ze soba dwa miasta i zwracamy to, co wyjdzie
    def _exchange(self, cycle: Cycle) -> Cycle:
        i = random.randint(0, self._cycle_size - 1)
        j = random.randint(0, self._cycle_size - 1)
        while j is i:
            j = random.randint(0, self._cycle_size - 1)
        cycle.swap(i, j)
        return cycle

    def _scramble(self, cycle: Cycle) -> Cycle:
        random_index_start = random.randint(0, self._cycle_size - 1)
        random_index_end = random.randint(0, self._cycle_size - 1)
        while random_index_end == random_index_start:  # upewniamy się że start != end
            random_index_end = random.randint(0, self._cycle_size - 1)
        i = random_index_start
        while i % self._cycle_size != random_index_end:
            r = random.randint(0, abs(i % self._cycle_size - random_index_end) - 1)
            cycle.swap(i % self._cycle_size, (i + r) % self._cycle_size)
            i += 1
        return cycle

    def mutate(self) -> Population:
        temp_population = Population()
        for curr_cycle in self._population:
            if random.uniform(0, 1) < self._mutation_param:
                if self._mutation_type == MutationType.INSERTION:
                    curr_cycle = self._insertion(curr_cycle)
                elif self._mutation_type == MutationType.EXCHANGE:
                    curr_cycle = self._exchange(curr_cycle)
                elif self._mutation_type == MutationType.SCRUMBLE:
                    curr_cycle = self._scramble(curr_cycle)
                else:
                    curr_cycle = self._insertion(curr_cycle)
            temp_population.add_cycle(curr_cycle)
        return temp_population