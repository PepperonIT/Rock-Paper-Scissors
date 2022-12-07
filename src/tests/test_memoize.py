import unittest
from src.memoize import DynamicRNG


class TestMemoize(unittest.TestCase):

    def test_copy_exclude_one_input(self):
        """
        Test that copy_exclude does infact exclude the given values.
        """
        exclude_int = DynamicRNG.copy_exclude([0, 1, 2, 3, 4], 2)
        self.assertEqual(exclude_int, [0, 1, 3, 4])

    def test_copy_exclude_multiple_ints(self):
        """
        Test that copy_exclude excludes all instances of the given value.
        """
        exclude_multiple_ints = DynamicRNG.copy_exclude([0, 1, 2, 0, 1, 2, 3, 0, 1, 2], 1)
        self.assertEqual(exclude_multiple_ints, [0, 2, 0, 2, 3, 0, 2])

    def test_copy_exclude_is_copy(self):
        """
        Test that copy_exclude does in fact create a copy and does not manipulate
        the original data.
        """
        test_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        exclusion_list = DynamicRNG.copy_exclude(test_list, 3)
        self.assertNotEqual(test_list, exclusion_list)

    def test_validate_input_valid_inputs(self):
        """
        Test that validate_input functions propperly for values in its span.
        """
        memo = DynamicRNG.get_instance()

        valid_zero = DynamicRNG.validate_input(memo, 0)
        valid_one = DynamicRNG.validate_input(memo, 1)
        valid_two = DynamicRNG.validate_input(memo, 2)

        self.assertEqual(valid_zero, 0, "Validation of '0' failed.")
        self.assertEqual(valid_one, 1, "Validation of '1' failed.")
        self.assertEqual(valid_two, 2, "Validation of '2' failed.")

    def test_validate_input_invalid_input(self):
        """
        Tests that validate_input does infact invalidate some arbitrary invalid input.
        """
        memo = DynamicRNG.get_instance()

        invalid_positive_int = DynamicRNG.validate_input(memo, 1000)
        invalid_negative_int = DynamicRNG.validate_input(memo, -1)
        invalid_string = DynamicRNG.validate_input(memo, "1")
        invalid_list = DynamicRNG.validate_input(memo, [1])

        self.assertEqual(invalid_positive_int, None)
        self.assertEqual(invalid_negative_int, None)
        self.assertEqual(invalid_string, None)
        self.assertEqual(invalid_list, None)

    def test_cut_memoization(self):
        memo = DynamicRNG.get_instance()
        DynamicRNG.dump_choices(memo)
        moves = DynamicRNG.get_game_inputs(memo)

        for i in range(DynamicRNG.get_choices_limit(memo)):
            DynamicRNG.update_choices(memo, moves[0])

        DynamicRNG.update_choices(memo, moves[1])
        expected_memoization = [moves[2], moves[2], moves[0], moves[2]]

        self.assertEqual(DynamicRNG.get_choices(memo), expected_memoization)

    def test_update_memoization_one_outcome(self):
        """
        Test that the outcome of one game result gives the correct memoization.
        """
        memo = DynamicRNG.get_instance()
        DynamicRNG.dump_choices(memo)
        moves = DynamicRNG.get_game_inputs(memo)

        DynamicRNG.update_choices(memo, moves[2])

        result = DynamicRNG.get_choices(memo)
        self.assertEqual(result, [moves[0], moves[1]])

    def test_update_memoization_limit(self):
        """
        Test that the memoization limit is adhered to.
        """
        memo = DynamicRNG.get_instance()
        DynamicRNG.dump_choices(memo)
        moves = DynamicRNG.get_game_inputs(memo)

        limit = DynamicRNG.get_choices_limit(memo)
        for i in range(limit + 1):
            DynamicRNG.update_choices(memo, moves[0])
        result = DynamicRNG.get_choices(memo)
        self.assertEqual(len(result), limit)

    def test_update_memoization_limit_slicing(self):
        """
        Test that the memoization limiter functions as it should when
        slicing off old memoized values.
        """
        memo = DynamicRNG.get_instance()
        memo_limit = DynamicRNG.get_choices_limit(memo)
        DynamicRNG.dump_choices(memo)
        moves = DynamicRNG.get_game_inputs(memo)

        for i in range(memo_limit // 2):
            DynamicRNG.update_choices(memo, moves[0])
        for i in range(memo_limit // 2):
            DynamicRNG.update_choices(memo, moves[1])

        memoized = DynamicRNG.get_choices(memo)
        game_inputs = DynamicRNG.get_game_inputs(memo)
        repeated_memo = DynamicRNG.copy_exclude(game_inputs, moves[1])

        expected_memo = []
        for i in range(memo_limit // 2):
            expected_memo += repeated_memo

        self.assertEqual(memoized, expected_memo)

    def test_update_memoization_invalid_input(self):
        """
        Test that the update_memoization function uses the validate_input function
        correctly.
        """
        memo = DynamicRNG.get_instance()
        DynamicRNG.dump_choices(memo)

        DynamicRNG.update_choices(memo, -1)
        result = DynamicRNG.get_choices(memo)
        self.assertEqual(len(result), 0)

    def test_proportions(self):
        """
        Run the game for 1 000 turns, fail if one outcome occurs 40% of the time or more.
        """
        memo = DynamicRNG.get_instance()
        moves = DynamicRNG.get_game_inputs(memo)

        runs = 1000
        cumulative = {}
        for game_move in moves:
            cumulative[game_move] = 0

        for i in range(runs):
            cumulative[DynamicRNG.dynamic_random(memo)] += 1

        for i in cumulative:
            res = float(cumulative[i]) / float(runs)
            self.assertLess(res, 0.4)
            print(i, " was selected: %10.4f" % (res), " of the time")


if __name__ == '__main__':
    unittest.main()
