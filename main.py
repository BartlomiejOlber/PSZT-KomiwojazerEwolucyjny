from model.cycle import Cycle, City
from model.population import Population
from evolution.crossover import Crossover
from evolution.mutation import Mutation
from evolution.mutation import mutation_type
import pandas as pd
import itertools
import random

# ładujemy dane z pliku csv
# dla każde
def load_data() -> Cycle:
    data = pd.read_csv('data/cities.csv')
    cities = data.iloc[:10,:10]                             #pobieramy jedynie pierwszych 10 miast
    city_list = []
    for city_name in cities:                #dla każdego z miast tworzymy liste odległości do innych miast
        city_id = 0
        adjacency_list = dict()

        for city in cities:
            adjacency_list[city] = cities[city_name][city_id]
            city_id += 1
        city_list.append(City(city_name, adjacency_list))

    cycle = Cycle(city_list)
    print(cycle.get_length())
    return cycle


def init_population():
    cycle = load_data()         #tworzony pierwszy cykl, ma wszystkie miasta po kolei w sobie jak na razie
    population = Population()
    population.rand_populate(cycle, 10) #
    curr_best = population.get_the_best()   #funkcja zwraca najlepszego z cykli w obecnej populacji, musimy gdzies przypisac
    crossover = Crossover()
    crossover.uniform_crossover(population, 0.3)


#
# {Problem komiwojazera, Algorytm Ewolucyjny.
# Opis: nalezy wybrac N miast polskich i znalezc najkrotszy cykl laczacy je wszystkie.
# Algorytm: ewolucyjny (μ+λ) i (μ,λ). Nalezy zaprojektowac operatory krzyzowania i mutacji.
#     Należy eksperymentalnie ustalić w przybliżeniu najlepsze parametry działania obu algorytmów.
# Interfejs: pokazuje postep procesu optymalizacji, podaje ostateczną kolejność miast.
#     Należy sprawdzić program dla N=10,20,30.}
if __name__ == '__main__':
    #init_population()
    cycle = load_data()
    # for cities in cycle:
    #     print(cities.get_name())
    populacja = Population()
    populacja.rand_populate(cycle,10)
    stare_dlogosci = []
    i = 0
    print("POCZATEK:")
    for cycles in populacja:
        print('\n' + str(i) + ' cykl' + '\t-\t' + str(cycles.get_length()) )
        stare_dlogosci.append(cycles.get_length())
        for cities in cycles:
            print(cities.get_name())
        i+=1
    mutacja = Mutation(mutation_type.SCRUMBLE,0.1)
    nowa = mutacja.mutate(populacja)
    i = 0
    nowe_dlugosci = []
    print("\nKONIEC:")
    for cycles in nowa:
        print('\n' + str(i) + ' cykl' + '\t-\t' + str(cycles.get_length()))
        nowe_dlugosci.append(cycles.get_length())
        for cities in cycles:
            print(cities.get_name())
        i += 1

    for i in range(10):
        print(str(abs(nowe_dlugosci[i]-stare_dlogosci[i])))

