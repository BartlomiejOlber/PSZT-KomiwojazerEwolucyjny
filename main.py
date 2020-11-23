from evolution.mutation import Mutation
from evolution.strategy import Strategy
from evolution.crossover import Crossover
from model.cycle import Cycle, City
from model.population import Population
from model.evolution_params import EvolutionParams

import pandas as pd
import argparse


def load_data(cities_number: int) -> Cycle:
    data = pd.read_csv('data/cities.csv')
    cities = data.iloc[:cities_number, :cities_number]
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


def init_population(cities_number: int, population_size: int) -> Population:
    cycle = load_data(cities_number)
    population = Population()
    population.rand_populate(cycle, population_size)
    return population


def testing():
    evolution_params = parse_args()
    population = init_population(evolution_params.cities, evolution_params.mi)
    mutation = Mutation(population=population, evolution_params=evolution_params)
    crossover = Crossover(population=population, evolution_params=evolution_params)
    strategy = Strategy(evolution_params=evolution_params, mutation=mutation, crossover=crossover,
                        population=population)

    naj = population.get_n_best(5)
    for cycles in naj:
        print(cycles.get_length())

    mi = strategy.evolve()
    print("\n\nNAJLEPSZE:")
    print(mi.get_the_best().get_length())
    mi.get_the_best().print_cycle()

    strategy.change_strategy()
    strategy.set_population(population)
    mi = strategy.evolve()
    print("\n\nNAJLEPSZE MIPLUS:")
    print(mi.get_the_best().get_length())
    mi.get_the_best().print_cycle()
    print()


def parse_args() -> EvolutionParams:
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cities", type=int, required=True, help="cycle size")
    ap.add_argument("-m", "--mi", type=int, required=True, help="base population size")
    ap.add_argument("-l", "--lambda", type=int, required=True, help="number of cycles taking part in reproduction")
    ap.add_argument("-g", "--generations", type=int, required=True, help="number of algorithm iterations")
    ap.add_argument("-mp", "--mutation_param", type=float, required=True, help="probability of mutation")
    ap.add_argument("-cp", "--crossover_param", type=float, required=True, help="probability of crossover")
    ap.add_argument("-u", "--uniform_crossover_param", type=float, required=False, help="probability of genome cross")
    ap.add_argument("-mt", "--mutation_type", type=str, required=False, help="\"exchange\", \"insertion\" or "
                                                                             "\"scramble\"")
    ap.add_argument("-ct", "--crossover_type", type=str, required=False, help="\"uniform\" or \"one_point\"")
    ap.add_argument('-p', "--plus", action='store_true', help="mi plus lambda strategy if flag is set")
    args = vars(ap.parse_args())
    print("{}".format(args["crossover_type"]))
    if args["crossover_type"] == "uniform" and not args["uniform_crossover_param"]:
        print("you need to provide -u param")
        exit(-1)
    return EvolutionParams(args)


if __name__ == '__main__':
    testing()
