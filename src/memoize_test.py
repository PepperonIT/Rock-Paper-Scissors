import unittest
from memoize import Memoize


class TestMemoize(unittest.TestCase):

    def test_update_memoization_one_outcome(self):
        memo = Memoize.get_instance()
        Memoize.dump_memoization(memo)
        Memoize.update_memoization(memo, 2)
        result = Memoize.get_memoization(memo)
        self.assertEqual(result, [0, 1], "Failed")

    def test_update_memoization_limit(self):
        memo = Memoize.get_instance()
        limit = Memoize.get_memoization_limit(memo)
        for i in range(limit + 1):
            Memoize.update_memoization(memo, 0)
        result = Memoize.get_memoization(memo)
        self.assertEqual(len(result), limit)

    def test_update_memoization_invalid_input(self):
        memo = Memoize.get_instance()
        Memoize.dump_memoization(memo)
        Memoize.update_memoization(memo, -1)
        result = Memoize.get_memoization(memo)
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
