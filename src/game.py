class Game:

    def __init__(self, rounds=None):
        # type: (int) -> None
        """
        Initiates the game, it is a best of 'x' rounds. Allows for different number of 
        rounds, but by default plays 3 rounds.
        """
        if type(rounds) != int or rounds < 1:
            self.__round_limit = 3
        else:
            self.__round_limit = rounds

        self.__current_round = 0
        self.__computer_score = 0
        self.__human_score = 0

    def get_round_limit(self):
        # type: () -> int
        """
        Returns the round limit for the game.
        """
        return self.__round_limit

    def get_computer_score(self):
        # type: () -> int
        """
        Returns the computers score.
        """
        return self.__computer_score

    def get_human_score(self):
        # type: () -> int
        """
        Returns the human players score.
        """
        return self.__human_score

    def get_current_round(self):
        # type: () -> int
        """
        Return the current round of the best of 'x' game.
        """
        return self.__current_round

    def check_winner(self):
        # type: () -> bool
        """
        Returns True if there is a winner, otherwise returns False.
        """
        if max(self.__computer_score, self.__human_score) > (self.__round_limit / 2):
            return True
        return False

    def get_winner(self):
        # () -> str | None
        """
        Returns the winner, if there is any, or 'Draw' if it is a draw. 
        Also checks that there is in fact a winner.
        """
        if not self.check_winner():
            return None
        if self.__computer_score > self.__human_score:
            return "Computer"
        elif self.__human_score > self.__computer_score:
            return "Human"
        else:
            return "Draw"

    def update_game(self, winner=str):
        # type: (str) -> None
        """
        Updates the game state based on the stated winner and increments the current round.
        This can be extended to account for several winners if there are more than two players.
        """
        winners = winner.split()
        for i in winners:
            if i == "Human":
                self.__human_score += 1
            elif i == "Computer":
                self.__computer_score += 1

        self.__current_round += 1
