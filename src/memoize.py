import random
import datetime


class Memoize():
    __instance = None

    @staticmethod
    def get_instance():
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
        # type: (list[int], (int | None)) -> list[int]
        """
        Takes a list, list[elemA], and a variable elemA, returns a copy of list with no 
        instances of elemA.
        """
        result_list = []
        for i in list:
            if i != exclude:
                result_list.append(i)
        return result_list

    def validate_input(self, game_input):
        # type: (Memoize, int) -> int | None
        """
        Validates that the input is a predefined input, otherwise it returns None.
        """
        valid_inputs = self.copy_exclude(self.__game_values, None)
        for i in valid_inputs:
            if i == game_input:
                return i
        return None

    def update_memoization(self, outcome):
        # type: (Memoize, int) -> None
        """
        Takes the new game outcome as an argument and updates the memoization based on the arguments value.
        If the input is invalid, i.e. does not exist in the predefined game inputs, the validate_input returns None 
        and the function terminates.
        """
        validated_outcome = Memoize.validate_input(self, outcome)
        if validated_outcome == None:
            return

        memoize = self.copy_exclude(self.__game_values, validated_outcome)
        self.__memoization += memoize

        if len(self.__memoization) > self.__memoization_limit:
            """
            If the memoization excedes the limit, repeatedly cut of the first element until it is within the limit.
            """
            while len(self.__memoization) > self.__memoization_limit:
                self.__memoization = self.__memoization[1:]

    def get_memoization(self):
        # type: (Memoize) -> list[int]
        return self.__memoization

    def get_memoization_limit(self):
        # type: (Memoize) -> int
        return self.__memoization_limit

    def get_game_inputs(self):
        # type: (Memoize) -> list[int]
        return self.__game_values

    def dump_memoization(self):
        # type: (Memoize) -> None
        """
        Empties the existing memoization.
        """
        self.__memoization = []

    def memoized_random(self):
        # type: (Memoize) -> int
        """
        Returns a pseudo-randomized game choice, and updates the memoized data.
        """
        selection = self.copy_exclude(self.__game_values, None)
        selection += self.copy_exclude(self.__memoization, None)
        choice = random.choice(selection)
        self.update_memoization(choice)
        return choice
