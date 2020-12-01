import copy
import random
from tqdm import tqdm

from model.population import Population
from model.evolution_params import EvolutionParams
from evolution.crossover import Crossover
from evolution.mutation import Mutation
from model.types import StrategyType


class Strategy(object):
    def __init__(self, evolution_params: EvolutionParams, mutation: Mutation, crossover: Crossover,
                 population: Population = None):
        self._generations = evolution_params.generations
        self._mi = evolution_params.mu
        self._lambda = evolution_params.lmbd
        self._strategy_type = evolution_params.strategy_type
        self._crossover = crossover
        self._mutation = mutation
        self._population = population
        self._evolution_log = []

    def get_log(self):
        return self._evolution_log

    def change_strategy(self):
        if self._strategy_type == StrategyType.MU_PLUS:
            self._strategy_type = StrategyType.MU_COMMA
        else:
            self._strategy_type = StrategyType.MU_PLUS

    def set_population(self, population: Population):
        self._population = copy.deepcopy(population)

    def get_type(self):
        return self._strategy_type

    def _mu_plus(self) -> Population:
        self._evolution_log.clear()
        for i in tqdm(range(self._generations)):
            self._evolution_log.append(self._population.get_the_best().get_length())
            next_generation = Population()
            for j in range(self._lambda):
                next_generation.add_cycle(self._population[(random.randint(0, len(self._population) - 1))])

            self._crossover.insert_next_generation(next_generation)
            next_generation = self._crossover.do_crossover()

            self._mutation.set_next_generation(next_generation)
            next_generation = self._mutation.mutate()

            for j in sorted(self._population):
                next_generation.add_cycle(j)

            self._population = next_generation.get_n_best(self._mi)
        return self._population

    def _mu_comma(self) -> Population:
        self._evolution_log.clear()
        for i in tqdm(range(self._generations)):
            self._evolution_log.append(self._population.get_the_best().get_length())
            next_generation = Population()
            for j in range(self._lambda):
                next_generation.add_cycle(self._population[(random.randint(0, len(self._population) - 1))])

            self._crossover.insert_next_generation(next_generation)
            next_generation = self._crossover.do_crossover()

            self._mutation.set_next_generation(next_generation)
            next_generation = self._mutation.mutate()

            self._population = next_generation.get_n_best(self._mi)
        return self._population

    def evolve(self):
        if self._strategy_type == StrategyType.MU_PLUS:
            return self._mu_plus()
        else:
            return self._mu_comma()
