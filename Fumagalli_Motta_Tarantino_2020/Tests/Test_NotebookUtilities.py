import unittest
from Fumagalli_Motta_Tarantino_2020.Notebooks.NotebookUtilities import *


class TestNotebookUtilities(unittest.TestCase):
    """
    Tests Fumagalli_Motta_Tarantino_2020.Notebooks.NotebookUtilities.
    """

    def test_get_model_by_id_optimal_merger_policy(self):
        m = get_model_by_id(3)
        self.assertEqual(FMT20.OptimalMergerPolicy, type(m))

    def test_get_model_by_id_pro_competitive(self):
        m = get_model_by_id(31)
        self.assertEqual(FMT20.ProCompetitive, type(m))

    def test_get_model_by_id_resource_waste(self):
        m = get_model_by_id(41)
        self.assertEqual(FMT20.ResourceWaste, type(m))

    def test_get_model_by_id_custom_type(self):
        m = get_model_by_id(51, preferred_type=FMT20.PerfectInformation)
        self.assertEqual(FMT20.PerfectInformation, type(m))

    def test_configure_axes_first_model_invalid(self):
        self.assertRaises(
            NotImplementedError,
            lambda: configure_two_axes(m1=FMT20.OptimalMergerPolicy()),
        )

    def test_configure_axes_second_model_invalid(self):
        self.assertRaises(
            NotImplementedError,
            lambda: configure_two_axes(m2=FMT20.OptimalMergerPolicy()),
        )

    def test_configure_valid_models(self):
        fig, _ = configure_two_axes(m1=FMT20.ProCompetitive(), m2=FMT20.ResourceWaste())
        self.assertEqual(2, len(fig.axes))

    def test_configure_default(self):
        fig, _ = configure_two_axes()
        self.assertEqual(2, len(fig.axes))

    def test_distribution_labels(self):
        self.assertEqual(
            "Normal Distribution",
            get_distribution_labels(
                FMT20.Distributions.NormalDistribution, long_label=True
            ),
        )
        self.assertEqual(
            "Uniform",
            get_distribution_labels(FMT20.Distributions.UniformDistribution),
        )

    def test_available_configurations(self):
        configs = get_configurations()
        self.assertIsNotNone(configs)
        self.assertIs(type(configs[0]), type(str()))
