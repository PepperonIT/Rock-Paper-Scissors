import unittest
from memoize import Memoize


class TestMemoize(unittest.TestCase):

    def test_validate_input_valid_inputs(self):
        memo = Memoize.get_instance()

        valid_zero = Memoize.validate_input(memo, 0)
        valid_one = Memoize.validate_input(memo, 1)
        valid_two = Memoize.validate_input(memo, 2)

        self.assertEqual(valid_zero, 0, "Validation of '0' failed.")
        self.assertEqual(valid_one, 1, "Validation of '1' failed.")
        self.assertEqual(valid_two, 2, "Validation of '2' failed.")

    def test_validate_input_invalid_input(self):
        memo = Memoize.get_instance()

        invalid_positive_int = Memoize.validate_input(memo, 1000)
        invalid_negative_int = Memoize.validate_input(memo, -1)
        invalid_string = Memoize.validate_input(memo, "1")
        invalid_list = Memoize.validate_input(memo, [1])
        invalid_bool = Memoize.validate_input(memo, True)

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

    def test_update_memoization_limit_slicing(self):
        memo = Memoize.get_instance()
        memo_limit = Memoize.get_memoization_limit(memo)

        for i in range(memo_limit // 2):
            Memoize.update_memoization(memo, 0)
        for i in range(memo_limit // 2):
            Memoize.update_memoization(memo, 1)

        memoized = Memoize.get_memoization(memo)
        game_inputs = Memoize.get_game_inputs(memo)
        repeated_memo = Memoize.copy_exclude(game_inputs, 1)

        expected_memo = []
        for i in range(memo_limit // 2):
            expected_memo += repeated_memo

        self.assertEqual(memoized, expected_memo)

    def test_update_memoization_invalid_input(self):
        memo = Memoize.get_instance()
        Memoize.dump_memoization(memo)
        Memoize.update_memoization(memo, -1)
        result = Memoize.get_memoization(memo)
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
