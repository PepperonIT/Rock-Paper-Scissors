import unittest

from src.controller import Controller


class TestController(unittest.TestCase):
    rock = 0
    paper = 1
    scissors = 2

    def test_rock(self):
        rock = Controller.get_winner(self.rock, self.rock)
        paper = Controller.get_winner(self.paper, self.rock)
        scissors = Controller.get_winner(self.scissors, self.rock)

        self.assertEqual(rock, 2)
        self.assertEqual(paper, 0)
        self.assertEqual(scissors, 1)

    def test_paper(self):
        rock = Controller.get_winner(self.rock, self.paper)
        paper = Controller.get_winner(self.paper, self.paper)
        scissors = Controller.get_winner(self.scissors, self.paper)

        self.assertEqual(rock, 1)
        self.assertEqual(paper, 2)
        self.assertEqual(scissors, 0)

    def test_scissors(self):
        rock = Controller.get_winner(self.rock, self.scissors)
        paper = Controller.get_winner(self.paper, self.scissors)
        scissors = Controller.get_winner(self.scissors, self.scissors)

        self.assertEqual(rock, 0)
        self.assertEqual(paper, 1)
        self.assertEqual(scissors, 2)

    def test_invalid_input(self):
        self.assertRaises(ValueError, Controller.get_winner, -1, self.rock)
        self.assertRaises(ValueError, Controller.get_winner, self.paper, -1)
        self.assertRaises(ValueError, Controller.get_winner, 1000, self.rock)
        self.assertRaises(ValueError, Controller.get_winner, self.paper, 1000)


if __name__ == '__main__':
    unittest.main()
