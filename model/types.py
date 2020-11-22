from enum import Enum


class StrategyType(Enum):
    MIPLUS = 0
    MICOMMA = 1
    DEFAULT = MIPLUS

    @staticmethod
    def make(type_name: str = None) -> 'StrategyType':
        if type_name:
            if type_name.upper() == StrategyType.MIPLUS.name:
                return StrategyType.MIPLUS
            elif type_name.upper() == StrategyType.MICOMMA.name:
                return StrategyType.MICOMMA
        return StrategyType.DEFAULT


class CrossoverType(Enum):
    ONE_POINT = 1
    UNIFORM = 2
    DEFAULT = UNIFORM

    @staticmethod
    def make(type_name: str = None) -> 'CrossoverType':
        if type_name:
            if type_name.upper() == CrossoverType.ONE_POINT.name:
                return CrossoverType.ONE_POINT
            elif type_name.upper() == CrossoverType.UNIFORM.name:
                return CrossoverType.UNIFORM
        return CrossoverType.DEFAULT


class MutationType(Enum):
    INSERTION = 0
    EXCHANGE = 1
    SCRAMBLE = 2
    DEFAULT = INSERTION

    @staticmethod
    def make(type_name: str = None) -> 'MutationType':
        if type_name:
            if type_name.upper() == MutationType.INSERTION.name:
                return MutationType.INSERTION
            elif type_name.upper() == MutationType.EXCHANGE.name:
                return MutationType.EXCHANGE
            elif type_name.upper() == MutationType.SCRAMBLE.name:
                return MutationType.SCRAMBLE
        return MutationType.DEFAULT
