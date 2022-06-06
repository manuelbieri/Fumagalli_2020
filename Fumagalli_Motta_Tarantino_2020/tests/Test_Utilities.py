import unittest
import Fumagalli_Motta_Tarantino_2020 as FMT20


class TestNormalDistributionFunction(unittest.TestCase):
    def test_cumulative_function(self):
        self.assertEqual(0.5, FMT20.Utilities.NormalDistributionFunction.cumulative(0))

    def test_cumulative_function_adjusted_scale(self):
        self.assertEqual(
            0.5, FMT20.Utilities.NormalDistributionFunction.cumulative(0, scale=2)
        )

    def test_inverse_cumulative_function(self):
        self.assertEqual(
            0, FMT20.Utilities.NormalDistributionFunction.inverse_cumulative(0.5)
        )

    def test_inverse_cumulative_function_adjusted_loc(self):
        self.assertEqual(
            1, FMT20.Utilities.NormalDistributionFunction.inverse_cumulative(0.5, loc=1)
        )


class TestUniformDistributionFunction(TestNormalDistributionFunction):
    def test_cumulative_function(self):
        self.assertEqual(0, FMT20.Utilities.UniformDistributionFunction.cumulative(0))

    def test_cumulative_function_adjusted_scale(self):
        self.assertEqual(
            0.5, FMT20.Utilities.UniformDistributionFunction.cumulative(1, scale=2)
        )

    def test_inverse_cumulative_function(self):
        self.assertEqual(
            0.5, FMT20.Utilities.UniformDistributionFunction.inverse_cumulative(0.5)
        )

    def test_inverse_cumulative_function_adjusted_loc(self):
        self.assertEqual(
            2.5,
            FMT20.Utilities.UniformDistributionFunction.inverse_cumulative(0.5, loc=2),
        )
