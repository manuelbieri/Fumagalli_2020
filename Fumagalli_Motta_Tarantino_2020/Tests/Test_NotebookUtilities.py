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
        m = get_model_by_id(51, prefered_type=FMT20.PerfectInformation)
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
        fig = configure_two_axes(m1=FMT20.ProCompetitive(), m2=FMT20.ResourceWaste())
        self.assertEqual(2, len(fig.axes))

    def test_configure_default(self):
        fig = configure_two_axes()
        self.assertEqual(2, len(fig.axes))
