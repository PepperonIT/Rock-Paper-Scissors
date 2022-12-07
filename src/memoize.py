import random


class DynamicRNG():
    """
    Uses previous outcomes to adjust the chosen game gesture for rock-paper-scissors. 
    __choices is where the memoized values are stored.
    __choices_limit is the limit of how many choices should be kept in the dynamic choices list.
    __game_value is the set of valid game moves.

    Note that changing these game settings might affect the unit tests.
    """
    __instance = None

    @staticmethod
    def get_instance():
        """
        Returns a pointer to the active Memoization instance.
        If there is none, it creates it.
        """
        if DynamicRNG.__instance == None:
            DynamicRNG()
        return DynamicRNG.__instance

    def __init__(self):
        """
        Initializer for the DynamicRNG singleton.
        """
        if DynamicRNG.__instance != None:
            raise Exception("Singleton class initialized a second time.")
        else:
            DynamicRNG.__instance = self
            self.__choices = []
            self.__choices_limit = 4
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
        # type: (DynamicRNG, int) -> int | None
        """
        Validates that the input is a predefined input, otherwise it returns None.
        """
        valid_inputs = self.copy_exclude(self.__game_values, None)
        for i in valid_inputs:
            if i == game_input:
                return i
        return None

    def cut_choices(self, bias):
        if bias in self.__choices:
            self.__choices.remove(bias)
        self.__choices = self.__choices[-self.__choices_limit:]

    def update_choices(self, outcome):
        # type: (DynamicRNG, int) -> None
        """
        Takes the new game outcome as an argument and updates the choices based on the value, also removes the 
        chosen value from the choices before adding new values. If the input is invalid, i.e. does not exist 
        in the predefined game inputs, the validate_input returns None and the function terminates.
        """
        validated_outcome = DynamicRNG.validate_input(self, outcome)
        if validated_outcome == None:
            return

        if len(self.__choices) > 0:
            if outcome in self.__choices:
                self.__choices.remove(outcome)

        new_choices = self.copy_exclude(self.__game_values, validated_outcome)
        # If you want more even randomness activate the shuffle method.
        # This will cause most of the unit tests to fail, since some of them assume that
        # the choices entry method is consistent.
        # random.shuffle(new_choices)
        self.__choices += new_choices

        if len(self.__choices) > self.__choices_limit:
            self.cut_choices(outcome)

    def get_choices(self):
        # type: (DynamicRNG) -> list[int]
        """
        Simple get method for __choices.
        """
        return self.__choices

    def get_choices_limit(self):
        # type: (DynamicRNG) -> int
        """
        Simple get method for __choices_limit.
        """
        return self.__choices_limit

    def get_game_inputs(self):
        # type: (DynamicRNG) -> list[int]
        """
        Simple get method for __game_values.
        """
        return self.__game_values

    def dump_choices(self):
        # type: (DynamicRNG) -> None
        """
        Empties the existing choices.
        """
        self.__choices = []

    def dynamic_random(self):
        # type: (DynamicRNG) -> int
        """
        If there is no stored choices values simply returns a random game value then updates the
        DynamicRNG. But if something has been stored a random value from the DynamicRNG's choices is
        selected. The choices is then updated with the new outcome.
        """
        if self.__choices == []:
            selected = random.choice(self.__game_values)
            self.update_choices(selected)
            return selected
        else:
            selected = random.choice(self.__choices)
            self.update_choices(selected)
            return selected
