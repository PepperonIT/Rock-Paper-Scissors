import unittest
from src.memoize import Memoize


class TestMemoize(unittest.TestCase):

    def test_copy_exclude_one_input(self):
        """
        Test that copy_exclude does infact exclude the given values.
        """
        exclude_int = Memoize.copy_exclude([0, 1, 2, 3, 4], 2)
        self.assertEqual(exclude_int, [0, 1, 3, 4])

    def test_copy_exclude_multiple_ints(self):
        """
        Test that copy_exclude excludes all instances of the given value.
        """
        exclude_multiple_ints = Memoize.copy_exclude([0, 1, 2, 0, 1, 2, 3, 0, 1, 2], 1)
        self.assertEqual(exclude_multiple_ints, [0, 2, 0, 2, 3, 0, 2])

    def test_copy_exclude_is_copy(self):
        """
        Test that copy_exclude does in fact create a copy and does not manipulate 
        the original data.
        """
        test_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        exclusion_list = Memoize.copy_exclude(test_list, 3)
        self.assertNotEqual(test_list, exclusion_list)

    def test_validate_input_valid_inputs(self):
        """
        Test that validate_input functions propperly for values in its span.
        """
        memo = Memoize.get_instance()

        valid_zero = Memoize.validate_input(memo, 0)
        valid_one = Memoize.validate_input(memo, 1)
        valid_two = Memoize.validate_input(memo, 2)

        self.assertEqual(valid_zero, 0, "Validation of '0' failed.")
        self.assertEqual(valid_one, 1, "Validation of '1' failed.")
        self.assertEqual(valid_two, 2, "Validation of '2' failed.")

    def test_validate_input_invalid_input(self):
        """
        Tests that validate_input does infact invalidate some arbitrary invalid input.
        """
        memo = Memoize.get_instance()

        invalid_positive_int = Memoize.validate_input(memo, 1000)
        invalid_negative_int = Memoize.validate_input(memo, -1)
        invalid_string = Memoize.validate_input(memo, "1")
        invalid_list = Memoize.validate_input(memo, [1])

        self.assertEqual(invalid_positive_int, None)
        self.assertEqual(invalid_negative_int, None)
        self.assertEqual(invalid_string, None)
        self.assertEqual(invalid_list, None)

    def test_update_memoization_one_outcome(self):
        """
        Test that the outcome of one game result gives the correct memoization.
        """
        memo = Memoize.get_instance()
        Memoize.dump_memoization(memo)
        Memoize.update_memoization(memo, 2)
        result = Memoize.get_memoization(memo)
        self.assertEqual(result, [0, 1], "Failed")

    def test_update_memoization_limit(self):
        """
        Test that the memoization limit is adhered to.
        """
        memo = Memoize.get_instance()
        limit = Memoize.get_memoization_limit(memo)
        for i in range(limit + 1):
            Memoize.update_memoization(memo, 0)
        result = Memoize.get_memoization(memo)
        self.assertEqual(len(result), limit)

    def test_update_memoization_limit_slicing(self):
        """
        Test that the memoization limiter functions as it should when 
        slicing off old memoized values. 
        """
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
        """
        Test that the update_memoization function uses the validate_input function
        correctly.
        """
        memo = Memoize.get_instance()
        Memoize.dump_memoization(memo)
        Memoize.update_memoization(memo, -1)
        result = Memoize.get_memoization(memo)
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
