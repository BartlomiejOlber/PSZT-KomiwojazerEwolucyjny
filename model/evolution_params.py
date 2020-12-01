from model.types import MutationType, StrategyType, CrossoverType


class EvolutionParams(object):
    def __init__(self, params_dict: dict):
        self.cities = params_dict['cities']
        self.mu = params_dict['mu']
        self.lmbd = params_dict['lambda']
        self.generations = params_dict['generations']
        self.mutation_param = params_dict['mutation_param']
        self.crossover_param = params_dict['crossover_param']
        self.uniform_crossover_param = params_dict['uniform_crossover_param']
        self.mutation_type = MutationType.make(params_dict['mutation_type'])
        self.crossover_type = CrossoverType.make(params_dict['crossover_type'])
        self.strategy_type = StrategyType.MU_PLUS if params_dict['plus'] else StrategyType.MU_COMMA
