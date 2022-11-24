import unittest
from memoize import Memoize


class TestMemoize(unittest.TestCase):

    def test_update_memoization_one_outcome(self):
        memo = Memoize.getInstance()
        result = Memoize.update_memoization(memo, 2)
        self.assertEqual(result, True, "Failed")


if __name__ == '__main__':
    unittest.main()
