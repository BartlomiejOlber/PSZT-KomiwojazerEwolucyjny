from model.city import City
from model.cycle import Cycle
from typing import List
import random
from model.population import Population
from enum import Enum

class mutation_type(Enum):
    INSERTION = 0
    EXCHANGE = 1
    SCRUMBLE = 2


class Mutation():

    # lista cykli miast (populacja), typ mutacji, szansa mutacji
    def __init__(self, type: mutation_type, mutation_param: float):
        #self._population = population
        #self._cycle_size = population.get_cycle_size()
        self._mutation_type = type
        self._mutation_param = mutation_param

    def _swap(cities: List[City], i: int, j: int) -> List[City]:
        temp = cities[i]
        cities[i] = cities[j]
        cities[j] = temp
        return cities
    def _insertion(self,cycle: Cycle) -> Cycle:
        random_index = random.randint(0, len(cycle)-1)            #wybieramy losowo jakies miasto z listy
        random_destination = random.randint(0, len(cycle)-1)      #wybieramy losowo kolejne miasto z listy, moze byc problem bo moze to byc to samo miasto
        while random_destination == random_index:
            random_destination = random.randint(0, len(cycle)-1)
        if random_index < random_destination:                  #przesuwamy miasto pierwsze na miejsce drugiego, NIE ZAMIENIAMY ICH
            temp = cycle[random_index]
            for i in range(random_index, random_destination):
                cycle[i] = cycle[i+1]
            cycle[random_destination] = temp
        else:
            temp = cycle[random_index]
            for i in range(random_index, random_destination, -1):
                cycle[i] = cycle[i-1]
            cycle[random_destination] = temp
        return cycle
    # w cyklu zamieniamy ze soba dwa miasta i zwracamy to, co wyjdzie
    def _exchange(self, cycle: Cycle) -> Cycle:
        i =random.randint(0, len(cycle) - 1)
        j = random.randint(0, len(cycle) - 1)
        while j==i:
            j = random.randint(0, len(cycle))
        cycle = Mutation._swap(cycle, i, j)
        return Cycle(cycle)
    def _scramble(self,cycle: Cycle) -> Cycle:
        random_index_start = random.randint(0, len(cycle)-1)
        random_index_end = random.randint(0, len(cycle)-1)
        while random_index_end == random_index_start:         #upewniamy się że start != end
            random_index_end = random.randint(0, len(cycle)-1)
        i = random_index_start
        while i % len(cycle) != random_index_end:
            r = random.randint(0,abs(i % len(cycle) - random_index_end)-1)
            cycle = Mutation._swap(cycle, i % len(cycle), (i + r) % len(cycle))
            i += 1
        return Cycle(cycle)

    def mutate(self, population: Population) -> Population:
        temp_population = Population()
        for curr_cycle in population:
            if random.uniform(0, 1)>=self._mutation_param:
                if self._mutation_type == mutation_type.INSERTION:
                    curr_cycle = self._insertion(curr_cycle)
                elif self._mutation_type == mutation_type.EXCHANGE:
                    curr_cycle = self._exchange(curr_cycle)
                elif self._mutation_type == mutation_type.SCRUMBLE:
                    curr_cycle = self._scramble(curr_cycle)
                else:
                    curr_cycle = self._insertion(curr_cycle)
            temp_population.add_cycle(curr_cycle)
        return temp_population