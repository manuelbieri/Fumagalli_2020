import unittest

import Fumagalli_Motta_Tarantino_2020.Model as Model


class TestBaseModel(unittest.TestCase):
    def test_valid_setup_default_values(self):
        Model.BaseModel()

    def test_invalid_success_probability(self):
        self.assertRaises(AssertionError, lambda: Model.BaseModel(success_probability=0))
        self.assertRaises(AssertionError, lambda: Model.BaseModel(success_probability=1.1))

    def test_invalid_tolerated_harm(self):
        self.assertRaises(AssertionError, lambda: Model.BaseModel(tolerated_level_of_harm=-0.1))
