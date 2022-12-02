import unittest
from src.game import Game


class TestGame(unittest.TestCase):
    def test_game_rounds_defaulting(self):
        default_game = Game()
        custom_game = Game(10)
        invalid_game_int_negative = Game(-1)
        invalid_game_int_zero = Game(0)
        invalid_game_string = Game("1")
        invalid_game_bool_true = Game(True)
        invalid_game_bool_false = Game(False)
        invalid_game_float_whole = Game(2.0)
        invalid_game_float = Game(2.5)
        invalid_game_float_negative = Game(-2.3)

        self.assertEqual(default_game.get_round_limit(), 3)
        self.assertEqual(custom_game.get_round_limit(), 10)
        self.assertEqual(invalid_game_int_negative.get_round_limit(), 3)
        self.assertEqual(invalid_game_int_zero.get_round_limit(), 3)
        self.assertEqual(invalid_game_string.get_round_limit(), 3)
        self.assertEqual(invalid_game_bool_true.get_round_limit(), 3)
        self.assertEqual(invalid_game_bool_false.get_round_limit(), 3)
        self.assertEqual(invalid_game_float_whole.get_round_limit(), 3)
        self.assertEqual(invalid_game_float.get_round_limit(), 3)
        self.assertEqual(invalid_game_float_negative.get_round_limit(), 3)

    def test_update_game(self):
        game = Game()

        game.update_game("Human")
        self.assertEqual(game.get_human_score(), 1)
        self.assertEqual(game.get_computer_score(), 0)
        self.assertEqual(game.get_current_round(), 1)
        self.assertFalse(game.check_winner())

        game.update_game("Computer")
        self.assertEqual(game.get_human_score(), 1)
        self.assertEqual(game.get_computer_score(), 1)
        self.assertEqual(game.get_current_round(), 2)
        self.assertFalse(game.check_winner())

        game.update_game("Human")
        self.assertEqual(game.get_human_score(), 2)
        self.assertEqual(game.get_computer_score(), 1)
        self.assertEqual(game.get_current_round(), 3)
        self.assertTrue(game.check_winner())
        self.assertEqual(game.get_winner(), "Human")


if __name__ == '__main__':
    unittest.main()
