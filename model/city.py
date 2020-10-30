from typing import List


class City(object):

    def __init__(self, name: str, adjacency_list: dict):
        self.__name = name
        self.__adjacency_list = adjacency_list

    def get_name(self):
        return self.__name

    def get_distance_from(self, another_city: str):
        return self.__adjacency_list[another_city]