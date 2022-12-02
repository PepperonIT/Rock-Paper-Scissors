import unittest

from src.connection import Connection


class TestConnection(unittest.TestCase):
    rock = 0
    paper = 1
    scissors = 2

    def test_rock(self):
        rock = Connection.get_winner(self.rock, self.rock)
        paper = Connection.get_winner(self.paper, self.rock)
        scissors = Connection.get_winner(self.scissors, self.rock)

        self.assertEqual(rock, 2)
        self.assertEqual(paper, 0)
        self.assertEqual(scissors, 1)

    def test_paper(self):
        rock = Connection.get_winner(self.rock, self.paper)
        paper = Connection.get_winner(self.paper, self.paper)
        scissors = Connection.get_winner(self.scissors, self.paper)

        self.assertEqual(rock, 1)
        self.assertEqual(paper, 2)
        self.assertEqual(scissors, 0)

    def test_scissors(self):
        rock = Connection.get_winner(self.rock, self.scissors)
        paper = Connection.get_winner(self.paper, self.scissors)
        scissors = Connection.get_winner(self.scissors, self.scissors)

        self.assertEqual(rock, 0)
        self.assertEqual(paper, 1)
        self.assertEqual(scissors, 2)

    def test_invalid_input(self):
        invalid_negative_int_human = Connection.get_winner(-1, self.rock)
        invalid_negative_int_computer = Connection.get_winner(self.paper, -1)
        invalid_int_human = Connection.get_winner(1000, self.rock)
        invalid_int_computer = Connection.get_winner(self.paper, 1000)

        self.assertEqual(invalid_negative_int_human, None)
        self.assertEqual(invalid_negative_int_computer, None)
        self.assertEqual(invalid_int_human, None)
        self.assertEqual(invalid_int_computer, None)


if __name__ == '__main__':
    unittest.main()
