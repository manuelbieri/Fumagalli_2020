import unittest

import Fumagalli_Motta_Tarantino_2020.Model as Model


class TestBaseModel(unittest.TestCase):
    def test_valid_setup_default_values(self):
        Model.BaseModel()

    def test_invalid_tolerated_harm(self):
        self.assertRaises(AssertionError, lambda: Model.BaseModel(tolerated_level_of_harm=-0.1))

    def test_invalid_private_benefit(self):
        self.assertRaises(AssertionError, lambda: Model.BaseModel(private_benefit=-0.1))

    def test_invalid_profit(self):
        self.assertRaises(
            AssertionError,
            lambda: Model.BaseModel(incumbent_profit_without_innovation=0.2, incumbent_profit_duopoly=0.3),
        )
        self.assertRaises(
            AssertionError,
            lambda: Model.BaseModel(incumbent_profit_with_innovation=0.2, incumbent_profit_without_innovation=0.3),
        )
        self.assertRaises(
            AssertionError,
            lambda: Model.BaseModel(
                incumbent_profit_with_innovation=0.2, incumbent_profit_duopoly=0.3, startup_profit_duopoly=0.2
            ),
        )
        self.assertRaises(
            AssertionError,
            lambda: Model.BaseModel(
                startup_profit_duopoly=0.2, incumbent_profit_with_innovation=0.5, incumbent_profit_duopoly=0.3
            ),
        )

    def test_invalid_consumer_surplus(self):
        self.assertRaises(
            AssertionError,
            lambda: Model.BaseModel(
                consumer_surplus_monopoly_with_innovation=0.2, consumer_surplus_monopoly_without_innovation=0.3
            ),
        )

    def test_invalid_success_probability(self):
        self.assertRaises(AssertionError, lambda: Model.BaseModel(success_probability=0))
        self.assertRaises(AssertionError, lambda: Model.BaseModel(success_probability=1.1))
