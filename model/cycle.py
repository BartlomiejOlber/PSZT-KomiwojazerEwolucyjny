from .city import City
from typing import List
import random


class Cycle(object):

    def __init__(self, cities: List[City] = None):
        self.__length = 0.0
        self.__cities = cities

    def __lt__(self, other):
        return self.get_length() < other.get_length()

    def __gt__(self, other):
        return self.get_length() > other.get_length()

    def __len__(self):
        return len(self.__cities)

    def __getitem__(self, index: int):
        return self.__cities[index]

    def __setitem__(self, index: int, value):
        self.__cities[index] = value

    def get_length(self) -> float:
        self.__length = 0.0
        prev_city = self.__cities[0]
        for city in self.__cities[1:]:
            self.__length += city.get_distance_from(prev_city.get_name())
            prev_city = city
        self.__length += self.__cities[0].get_distance_from(prev_city.get_name())
        return self.__length

    def randomize(self):
        return random.shuffle(self.__cities)

    def print_cycle(self):
        i = 1
        for city in self.__cities:
            print(" {}.{}".format(i, city.get_name()) if city else " ", end=" ")
            i += 1