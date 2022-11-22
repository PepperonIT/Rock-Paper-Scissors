import random
import datetime


def copy_exclude(list, exclude):
    """
    Takes a list, list[elemA], and a variable elemA, returns a copy of list with no 
    instances of elemA.
    """
    result_list = []
    for i in list:
        if i != exclude:
            result_list.append(i)
    return result_list


class Memoize(type):
    """
    Memoizing random function for RPS, returns an integer with one of three values, 0, 1, or 2.
    """
    _instance = {}
    __game_values = [0, 1, 2]
    __memoization_limit = 6
    __memoization = []

    def __call__(cls):
        if cls not in cls._instance:
            cls._instance[cls] = super(Memoize, cls).__call__()
        return cls._instance[cls]

    def memoize(self):
        random.seed(datetime.datetime.now())

    def new_memo(self, outcome):
        memoization = copy_exclude(self.__memoization, None)
        addition = copy_exclude(self.__game_values, outcome)

        if len(memoization) > self.__memoization_limit:
            while len(memoization) > self.__memoization_limit:
                self._memoization = self._memoization[1:]
