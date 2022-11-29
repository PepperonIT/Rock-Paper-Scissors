import random


class Memoize():
    """
    Uses memoization to adjust the chosen game gesture for rock-paper-scissors. 
    __memoization is where the memoized values are stored.
    __memoization limit is twice the limit of memoization moves, if you want to memoize 
    the last 3 moves it should be set to 6.
    __game_value is the set of valid game moves.
    """
    __instance = None

    @staticmethod
    def get_instance():
        """
        Returns a pointer to the active Memoization instance.
        If there is none, it creates it.
        """
        if Memoize.__instance == None:
            Memoize()
        return Memoize.__instance

    def __init__(self):
        """
        Initializer for the Memoization singleton.
        """
        if Memoize.__instance != None:
            raise Exception("Singleton class initialized a second time.")
        else:
            Memoize.__instance = self
            self.__memoization = []
            self.__memoization_limit = 4
            self.__game_values = [0, 1, 2]

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

    def cut_memoization(self, bias):
        if bias in self.__memoization:
            self.__memoization.remove(bias)
        self.__memoization = self.__memoization[-self.__memoization_limit:]

    def update_memoization(self, outcome):
        # type: (Memoize, int) -> None
        """
        Takes the new game outcome as an argument and updates the memoization based on the value, also removes the 
        chosen value from the memoization before adding new values. If the input is invalid, i.e. does not exist 
        in the predefined game inputs, the validate_input returns None and the function terminates.
        """
        validated_outcome = Memoize.validate_input(self, outcome)
        if validated_outcome == None:
            return

        if len(self.__memoization) > 0:
            if outcome in self.__memoization:
                self.__memoization.remove(outcome)

        memoize = self.copy_exclude(self.__game_values, validated_outcome)
        self.__memoization += memoize

        if len(self.__memoization) > self.__memoization_limit:
            self.cut_memoization(outcome)

    def get_memoization(self):
        # type: (Memoize) -> list[int]
        """
        Simple get method for __memoization.
        """
        return self.__memoization

    def get_memoization_limit(self):
        # type: (Memoize) -> int
        """
        Simple get method for __memoization_limit.
        """
        return self.__memoization_limit

    def get_game_inputs(self):
        # type: (Memoize) -> list[int]
        """
        Simple get method for __game_values.
        """
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
        If there is no memoized values simply returns a random game value then updates the
        memoization. But if something has been memoized a random value from the memoization is
        selected. The memoization is then updated with the new outcome.
        """
        if self.__memoization == []:
            selected = random.choice(self.__game_values)
            self.update_memoization(selected)
            return selected
        else:
            selected = random.choice(self.__memoization)
            self.update_memoization(selected)
            return selected
