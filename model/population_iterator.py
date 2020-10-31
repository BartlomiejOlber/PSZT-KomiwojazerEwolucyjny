from model.population import Population


class PopulationIterator(object):
    def __init__(self, population: Population):
        self._population = population
        self._index = 0

    def next(self):
        if self._index < len(self._population.get_cycles()):
            result = (self._population.get_cycles()[self._index])
            self._index += 1
            return result
        raise StopIteration

    def __next__(self):
        return self.next()

    def has_next(self) -> bool:
        return len(self._population) > self._index
