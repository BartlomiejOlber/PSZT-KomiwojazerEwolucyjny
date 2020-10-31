from model.population import Population, Cycle
from model.city import City

import random
from copy import deepcopy


class Crossover(object):

    def uniform_crossover(self, population: Population, crossover_selection_param: float, crossover_param: float):
        subpopulation = self.__make_subpopulation(population, crossover_selection_param)
        it = subpopulation.get_iterator()
        print()
        print(len(subpopulation))
        while it.has_next():
            parent_1 = it.next()
            parent_2 = it.next()
            cycle_size = len(parent_1)
            crossover_bitmap = self.__make_crossover_bitmap(cycle_size, crossover_param)
            child_1 = deepcopy(parent_1)
            child_2 = deepcopy(parent_2)
            cities_in_child_1 = set()
            cities_in_child_2 = set()
            for i in range(cycle_size):
               if crossover_bitmap[i]:
                   cities_in_child_1.add(child_1[i])
                   cities_in_child_2.add(child_2[i])
                   child_1[i] = parent_2[i]
                   child_2[i] = parent_1[i]



            print(type(parent_2))
            print(parent_2)
            print(type(parent_1))
            print(parent_1)

    @staticmethod
    def __make_crossover_bitmap(cycle_size: int, crossover_param: float):
        bitmap = []
        for i in range(cycle_size):
            if random.uniform(0., 1.) < crossover_param:
                bitmap.append(1)
            else:
                bitmap.append(0)
        return bitmap

    @staticmethod
    def __make_subpopulation(population: Population, crossover_selection_parameter: float) -> Population:
        subpopulation = Population()
        cycles_added = set()
        i = 0
        for cycle in population:
            if random.uniform(0., 1.) < crossover_selection_parameter:
                subpopulation.add_cycle(cycle)
                cycles_added.add(i)
            i += 1
        print(cycles_added)
        if len(subpopulation) % 2:
            for it in range(len(population)):
                if it not in cycles_added:
                    subpopulation.add_cycle(population[it])
                    return subpopulation
        return subpopulation
