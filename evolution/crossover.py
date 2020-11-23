from model.population import Population, Cycle
from model.evolution_params import EvolutionParams
from model.types import CrossoverType

import random
from copy import deepcopy


class Crossover(object):

    def __init__(self, population: Population, evolution_params: EvolutionParams):
        self._cycle_size = population.get_cycle_size()
        self._population = population
        self._population_size = len(self._population)
        self._uniform_crossover_param = evolution_params.uniform_crossover_param
        self._crossover_param = evolution_params.crossover_param
        self._crossover_type = evolution_params.crossover_type

    def insert_next_generation(self, population: Population):
        self._population = population
        self._population_size = len(self._population)

    def do_crossover(self) -> Population:
        if self._crossover_type == CrossoverType.UNIFORM:
            return self._uniform_crossover()
        elif self._crossover_type == CrossoverType.ONE_POINT:
            return self._one_point_crossover()

    def _uniform_crossover(self):
        subpopulation = self._make_subpopulation()
        it = subpopulation.get_iterator()
        while it.has_next():
            parent_1 = it.next()
            parent_2 = it.next()
            self._make_crossover_bitmap()
            cities_to_reorder_1, cities_to_reorder_2, cities_to_swap = self._get_cities_to_cross(parent_1, parent_2)
            child_1, child_2 = self._make_children(parent_1, parent_2)

            for i in range(self._cycle_size):
                if self.__crossover_bitmap[i] and parent_1[i] in cities_to_swap:
                    child_2[i] = parent_1[i]
                if self.__crossover_bitmap[i] and parent_2[i] in cities_to_swap:
                    child_1[i] = parent_2[i]

            for i in range(self._cycle_size):
                if not child_1[i]:
                    child_1[i] = cities_to_reorder_1.pop()
                if not child_2[i]:
                    child_2[i] = cities_to_reorder_2.pop()
            self._population.add_cycle(child_1)
            self._population.add_cycle(child_2)
        return self._population

    def _one_point_crossover(self):
        subpopulation = self._make_subpopulation()
        it = subpopulation.get_iterator()
        while it.has_next():
            parent_1 = it.next()
            parent_2 = it.next()
            division_id = self._get_division_index()
            cities_to_reorder_1, cities_to_reorder_2, cities_to_swap = self._get_cities_to_cross(parent_1, parent_2,
                                                                                                 True, division_id)
            child_1, child_2 = self._make_children(parent_1, parent_2, True, division_id)
            for i in range(division_id, self._cycle_size):
                if parent_1[i] in cities_to_swap:
                    child_2[i] = parent_1[i]
                if parent_2[i] in cities_to_swap:
                    child_1[i] = parent_2[i]

            for i in range(division_id, self._cycle_size):
                if not child_1[i]:
                    child_1[i] = cities_to_reorder_1.pop()
                if not child_2[i]:
                    child_2[i] = cities_to_reorder_2.pop()
            self._population.add_cycle(child_1)
            self._population.add_cycle(child_2)
        return self._population

    def _get_division_index(self):
        return random.randint(1, self._cycle_size - 1)

    def _get_cities_to_cross(self, parent_1: Cycle, parent_2: Cycle, one_point: bool = False, division_id=0):
        cities_to_cross_1 = set()
        cities_to_cross_2 = set()
        for i in range(division_id, self._cycle_size):
            if one_point or self.__crossover_bitmap[i]:
                cities_to_cross_1.add(parent_1[i])
                cities_to_cross_2.add(parent_2[i])
        return cities_to_cross_1.difference(cities_to_cross_2), cities_to_cross_2.difference(cities_to_cross_1), \
               cities_to_cross_1.intersection(cities_to_cross_2)

    def _make_crossover_bitmap(self):
        self.__crossover_bitmap = []
        for i in range(self._cycle_size):
            if random.uniform(0., 1.) < self._crossover_param:
                self.__crossover_bitmap.append(1)
            else:
                self.__crossover_bitmap.append(0)

    def _make_children(self, parent_1: Cycle, parent_2: Cycle, one_point: bool = False, division_id=0):
        child_1 = Cycle(parent_1[:])
        child_2 = Cycle(parent_2[:])
        for i in range(division_id, self._cycle_size):
            if one_point or self.__crossover_bitmap[i]:
                child_1[i] = None
                child_2[i] = None
        return child_1, child_2

    def _make_subpopulation(self):
        subpopulation = Population()
        cycles_added = set()
        for i in reversed(range(self._population_size)):
            if random.uniform(0., 1.) < self._crossover_param and\
                    len(subpopulation) < self._population_size - 1:
                subpopulation.add_cycle(self._population.remove_cycle(i))
                cycles_added.add(i)
        if len(subpopulation) % 2:
            subpopulation.add_cycle(self._population.remove_cycle(0))
        return subpopulation

