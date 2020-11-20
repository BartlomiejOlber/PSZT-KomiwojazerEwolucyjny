from evolution.mutation import Mutation, mutation_type
from evolution.strategy import miplus
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
    # print(cycle.get_length())
    return cycle


def init_population():
    cycle = load_data()
    population = Population()
    population.rand_populate(cycle, 50)
    print("best: {}".format(population.get_the_best().get_length()))
    crossover = Crossover(population=population, crossover_param=0.5, crossover_selection_param=0.5)
    crossed_population = crossover.uniform_crossover()
    print(len(crossed_population))
    print("best after: {}".format(crossed_population.get_the_best().get_length()))

def testing(): #UWAGA: NIE DZIALA, czasami wychodzi poza index, dla wiekszych wartosci mi, lambda i generacji czesciej
    cycle = load_data()
    population = Population()
    population.rand_populate(cycle, 10)

    #Pokaz 5 najlepszych
    naj = population.get_n_best(5)
    for cycles in naj:
        print(cycles.get_length())
    #na razie sama mutacja jest, bez krzyzowania
    mutant = Mutation(mutation_type.EXCHANGE, 0.9)
    #dowal algorytmem na tej populacji, 3 generacje, mi = 5, lambda = 10
    mi = miplus(population, mutant, 3, 5, 10)
    #pokaz te po algorytmie
    print("\n\nNAJLEPSZE:")
    for cycles in mi:
        print(cycles.get_length())

if __name__ == '__main__':
    #init_population()
    testing()

