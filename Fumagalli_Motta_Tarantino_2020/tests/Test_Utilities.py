import unittest

import Fumagalli_Motta_Tarantino_2020.Utilities as Utilities


class TestNormalDistributionFunction(unittest.TestCase):
    def test_cumulative_function(self):
        self.assertEqual(0.5, Utilities.NormalDistributionFunction.cumulative(0))

    def test_cumulative_function_adjusted_scale(self):
        self.assertEqual(
            0.5, Utilities.NormalDistributionFunction.cumulative(0, scale=2)
        )

    def test_inverse_cumulative_function(self):
        self.assertEqual(
            0, Utilities.NormalDistributionFunction.inverse_cumulative(0.5)
        )

    def test_inverse_cumulative_function_adjusted_loc(self):
        self.assertEqual(
            1, Utilities.NormalDistributionFunction.inverse_cumulative(0.5, loc=1)
        )
