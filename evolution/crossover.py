from model.population import Population, Cycle
from model.city import City

import random
import numpy as np
from copy import deepcopy


class Crossover(object):

    def __init__(self, population: Population, crossover_selection_param: float, crossover_param: float):
        self.__cycle_size = population.get_cycle_size()
        self.__population = population
        self.__population_size = len(self.__population)
        self.__crossover_selection_param = crossover_selection_param
        self.__crossover_param = crossover_param

    def uniform_crossover(self):
        subpopulation = self.__make_subpopulation()
        it = subpopulation.get_iterator()
        while it.has_next():
            parent_1 = it.next()
            parent_2 = it.next()
            self.__make_crossover_bitmap()
            cities_to_reorder_1, cities_to_reorder_2, cities_for_straight_swap = self.__get_cities_to_cross(parent_1,
                                                                                                            parent_2)

            child_1, child_2 = self.__make_masked_children(parent_1, parent_2)

            for i in range(self.__cycle_size):
                if self.__crossover_bitmap[i] and parent_1[i] in cities_for_straight_swap:
                    child_2[i] = parent_1[i]
                if self.__crossover_bitmap[i] and parent_2[i] in cities_for_straight_swap:
                    child_1[i] = parent_2[i]

            for i in range(self.__cycle_size):
                if not child_1[i]:
                    child_1[i] = cities_to_reorder_1.pop()
                if not child_2[i]:
                    child_2[i] = cities_to_reorder_2.pop()
            self.__population.add_cycle(child_1)
            self.__population.add_cycle(child_2)
        return self.__population

    def __get_cities_to_cross(self, parent_1: Cycle, parent_2: Cycle):
        cities_to_cross_1 = set()
        cities_to_cross_2 = set()
        for i in range(self.__cycle_size):
            if self.__crossover_bitmap[i]:
                cities_to_cross_1.add(parent_1[i])
                cities_to_cross_2.add(parent_2[i])
        return cities_to_cross_1.difference(cities_to_cross_2), cities_to_cross_2.difference(cities_to_cross_1), \
               cities_to_cross_1.intersection(cities_to_cross_2)

    def __make_crossover_bitmap(self):
        self.__crossover_bitmap = []
        for i in range(self.__cycle_size):
            if random.uniform(0., 1.) < self.__crossover_param:
                self.__crossover_bitmap.append(1)
            else:
                self.__crossover_bitmap.append(0)

    def __make_masked_children(self, parent_1: Cycle, parent_2: Cycle):
        child_1 = deepcopy(parent_1)
        child_2 = deepcopy(parent_2)
        for i in range(self.__cycle_size):
            if self.__crossover_bitmap[i]:
                child_1[i] = None
                child_2[i] = None
        return child_1, child_2

    def __make_subpopulation(self):
        subpopulation = Population()
        cycles_added = set()
        for i in reversed(range(self.__population_size)):
            if random.uniform(0., 1.) < self.__crossover_selection_param and len(
                    subpopulation) < self.__population_size - 1:
                subpopulation.add_cycle(self.__population.remove_cycle(i))
                cycles_added.add(i)
        if len(subpopulation) % 2:
            subpopulation.add_cycle(self.__population.remove_cycle(0))
        return subpopulation
