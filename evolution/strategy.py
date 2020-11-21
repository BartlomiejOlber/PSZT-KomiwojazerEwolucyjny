import copy
from enum import Enum

from numpy.distutils.fcompiler import none

from evolution.crossover import Crossover
from model.population import Population
import random
from evolution.mutation import Mutation, MutationType

class Strategy_type(Enum):
    MIPLUS = 0
    MICOMMA = 1

class Strategy:
    def __init__(self, generations: int, mi: int, lmbd: int, strategy_type: Strategy_type):
        self._generations = generations
        self._mi = mi
        self._lmbd = lmbd
        self._strategy_type = strategy_type
        # te dodajemy pozniej:
        self._population = none


    def insert_population(self, population: Population):
        self._population = population

    def insert_crossover(self, crossover: Crossover):
        self._crossover = crossover

    def insert_mutation(self, mutation: Mutation):
        self._mutation = mutation

    def change_strategy(self):
        if(self._strategy_type == Strategy_type.MIPLUS):
            self._strategy_type = Strategy_type.MICOMMA
        else:
            self._strategy_type = Strategy_type.MIPLUS

    def miplus(self):
        curr_generation = copy.deepcopy(self._population)
        for i in range(self._generations):
            OT = Population()
            for j in range(self._lmbd):
                OT.add_cycle(curr_generation[(random.randint(0, len(curr_generation) - 1))])

            # self._crossover.insert_population(OT)
            # OT = self._crossover.one_point_crossover()

            self._mutation.insert_population(OT)
            OT = self._mutation.mutate()

            for j in sorted(curr_generation):
                OT.add_cycle(j)
            curr_generation = OT.get_n_best(self._mi)
        return curr_generation

    def micomma(self):
        curr_generation = copy.deepcopy(self._population)
        for i in range(self._generations):
            OT = Population()
            for j in range(self._lmbd):
                OT.add_cycle(curr_generation[(random.randint(0, len(curr_generation) - 1))])

            #self._crossover.insert_population(OT)
            #OT = self._crossover.one_point_crossover()

            self._mutation.insert_population(OT)
            OT = self._mutation.mutate()

            curr_generation = OT.get_n_best(self._mi)
        return curr_generation

    def evolve(self):
        if(self._strategy_type == Strategy_type.MIPLUS):
            return self.miplus()
        else:
            return self.micomma()



