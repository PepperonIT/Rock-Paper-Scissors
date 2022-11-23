import random
import datetime


@staticmethod
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

    def update_memoization(self, outcome):
        """
        Takes the new game outcome as an argument and updates the memoization based on the arguments value.
        """
        memoize = copy_exclude(self.__game_values, outcome)
        self.__memoization += memoize

        if len(self.__memoization) > self.__memoization_limit:
            """
            If the memoization excedes the limit, repeatedly cut of the first element until it is within the limit.
            """
            while len(self.__memoization) > self.__memoization_limit:
                self.__memoization = self.__memoization[1:]
        return True
