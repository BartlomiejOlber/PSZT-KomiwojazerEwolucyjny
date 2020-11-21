from evolution.mutation import Mutation, MutationType
from evolution.strategy import Strategy, Strategy_type
import evolution.strategy as strategy
from model.cycle import Cycle, City
from model.population import Population
from evolution.crossover import Crossover
import pandas as pd
import random


def load_data() -> Cycle:
    data = pd.read_csv('data/cities.csv')
    cities = data.iloc[:10,:10]
    city_list = []
    for city_name in cities:
        city_id = 0
        adjacency_list = dict()

        for city in cities:
            adjacency_list[city] = cities[city_name][city_id]
            city_id += 1
        city_list.append(City(city_name, adjacency_list))

    cycle = Cycle(city_list)
    return cycle


def init_population():
    cycle = load_data()
    population = Population()
    population.rand_populate(cycle, 30)
    print("best: {}".format(population.get_the_best().get_length()))
    crossover = Crossover(population=population, crossover_param=0.5, crossover_selection_param=0.5)

    crossed_population = crossover.uniform_crossover()
    print(len(crossed_population))
    print("best after: {}".format(crossed_population.get_the_best().get_length()))

def testing():
    cycle = load_data()
    population = Population()
    population.rand_populate(cycle, 30)
    #Pokaz 5 najlepszych
    naj = population.get_n_best(5)
    for cycles in naj:
        print(cycles.get_length())


    strategy = Strategy(10,20,60,Strategy_type.MICOMMA)
    mutation = Mutation(population=population, mutation_type=MutationType.EXCHANGE, mutation_param=0.5)
    crossover = Crossover(population=population, crossover_param=0.5, crossover_selection_param=0.5)
    strategy.insert_crossover(crossover)
    strategy.insert_mutation(mutation)
    strategy.insert_population(population=population)
    #na razie sama mutacja jest, bez krzyzowania
    mi = strategy.evolve()
    #pokaz te po algorytmie
    print("\n\nNAJLEPSZE:")
    print(mi.get_the_best().get_length())
    mi.get_the_best().print_cycle()

    strategy.change_strategy()

    mi = strategy.evolve()
    # pokaz te po algorytmie
    print("\n\nNAJLEPSZE MIPLUS:")
    print(mi.get_the_best().get_length())
    mi.get_the_best().print_cycle()


if __name__ == '__main__':
    #init_population()
    testing()



