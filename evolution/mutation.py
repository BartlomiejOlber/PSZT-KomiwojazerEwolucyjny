from model.population import Population
from model.cycle import Cycle
from model.evolution_params import EvolutionParams
from model.types import MutationType

import random


class Mutation(object):
    def __init__(self, population: Population, evolution_params: EvolutionParams):
        self._population = population
        self._cycle_size = population.get_cycle_size()
        self._mutation_type = evolution_params.mutation_type
        self._mutation_param = evolution_params.mutation_param

    def set_next_generation(self, population: Population):
        self._population = population

    def _insertion(self, cycle: Cycle) -> Cycle:
        random_index = random.randint(0, self._cycle_size - 1)
        random_destination = random.randint(0, self._cycle_size - 1)
        while random_destination == random_index:
            random_destination = random.randint(0, self._cycle_size - 1)
        if random_index < random_destination:
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
        while random_index_end == random_index_start:
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
                elif self._mutation_type == MutationType.SCRAMBLE:
                    curr_cycle = self._scramble(curr_cycle)
                else:
                    curr_cycle = self._insertion(curr_cycle)
            temp_population.add_cycle(curr_cycle)

        return temp_population
