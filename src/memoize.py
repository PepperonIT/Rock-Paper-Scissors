import random
import datetime


class Memoize():

    """
    Memoizing random function for RPS, returns an integer with one of three values, 0, 1, or 2.
    """

    __instance = None

    @staticmethod
    def getInstance():
        if Memoize.__instance == None:
            Memoize()
        return Memoize.__instance

    def __init__(self):
        if Memoize.__instance != None:
            raise Exception("Singleton class initialized a second time.")
        else:
            Memoize.__instance = self
            self.__game_values = [0, 1, 2]
            self.__memoization_limit = 6
            self.__memoization = []

    @staticmethod
    def copy_exclude(list, exclude):
        # type: (list[int], int) -> list[int]
        """
        Takes a list, list[elemA], and a variable elemA, returns a copy of list with no 
        instances of elemA.
        """
        result_list = []
        for i in list:
            if i != exclude:
                result_list.append(i)
        return result_list

    def memoize(self):
        random.seed(datetime.datetime.now())

    def update_memoization(self, outcome):
        # type: (int) -> bool
        """
        Takes the new game outcome as an argument and updates the memoization based on the arguments value.
        """
        memoize = self.copy_exclude(self.__game_values, outcome)
        self.__memoization += memoize

        if len(self.__memoization) > self.__memoization_limit:
            """
            If the memoization excedes the limit, repeatedly cut of the first element until it is within the limit.
            """
            while len(self.__memoization) > self.__memoization_limit:
                self.__memoization = self.__memoization[1:]
        return True
