from model.cycle import Cycle, City
from model.population import Population
import model.cycle
import pandas as pd
import random
from evolution.mutation import Mutation, MutationType


class Strategy:
    def __init__(self, generations: int, mi: int, _lambda: int):
        self._generations = generations
        self._mi = mi
        self._lambda = _lambda

    # jakos tak to powinno wygladac
    # mi+lmb
    # for i in range(generations-1):
    #     for j in range(_lambda):        # <- tutaj losujemy lambda razy cykl z obecnej populacji, populacja ma liczebnosc mi
    #         OT += populacja.losowy_cykl
    #     OT = krzyzuj(OT)                # wrzucamy do krzyżarki to co zebralismy wyzej (te lambda cykli w populacji)
    #     OT = mutuj(OT)                  # wrzucamy znowu ale do mutarki i dostajemy skrzyzowany, zmutwany populacje
    #     tmp = OT + populacja            # sumujemy to z nasza orginalna populacja, w sensie wszystkie poczatkowe cykle sprzed krzyzowania i mutacji tu beda
    #     populacja = get_mi_najlepszych(tmp)     # z tej sumy wybiearmy mi najlepszych i one beda nasza nastepna populacja bazowa

    # jakos tak to powinno wygladac
    # mi,lmb
    # for i in range(generations-1):
    #     for j in range(_lambda):        # <- tutaj losujemy lambda razy cykl z obecnej populacji, populacja ma liczebnosc mi
    #         OT += populacja.losowy_cykl
    #     OT = krzyzuj(OT)                # wrzucamy do krzyżarki to co zebralismy wyzej (te lambda cykli w populacji)
    #     OT = mutuj(OT)                  # wrzucamy znowu ale do mutarki i dostajemy skrzyzowany, zmutwany populacje
    #     tmp = OT            # wlasciwie wszystko to samo co wyzej tylko tutaj nie sumujemy z poczatkowa
    #     populacja = get_mi_najlepszych(tmp)     # z tej sumy wybiearmy mi najlepszych i one beda nasza nastepna populacja bazowa:


# def miplus(population: Population, crossover: Crossover, mutation: Mutation, generations: int, mi: int, _lambda: int):
#     curr_generation = population
#     OT = Population()
#     for i in range(generations):
#         for j in range(_lambda):
#             OT.add_cycle(curr_generation[random.randint(0,len(curr_generation))]-1)
#         #OT = crossover.uniform_crossover()
#         OT = mutation.mutate(OT)
#         curr_generation = curr_generation.get_n_best(mi)
#     return curr_generation


def miplus(population: Population, mutation: Mutation, generations: int, mi: int, _lambda: int):
    curr_generation = population

    for i in range(generations):
        OT = Population()
        for j in range(_lambda):
            OT.add_cycle(curr_generation[(random.randint(0, len(curr_generation) - 1))])
        # OT = crossover.uniform_crossover()
        OT = mutation.mutate()
        for j in curr_generation:
            OT.add_cycle(j)
        curr_generation = OT.get_n_best(mi)
    return curr_generation
