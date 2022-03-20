import unittest

import Fumagalli_Motta_Tarantino_2020.Model as Model


class TestBaseModel(unittest.TestCase):
    def setUp(self) -> None:
        self.model = Model.BaseModel()

    def test_valid_setup_default_values(self):
        Model.BaseModel()

    @staticmethod
    def get_default_value(arg_name: str) -> float:
        args_name = Model.BaseModel.__init__.__code__.co_varnames[1:]  # "self" is not needed
        default_value = Model.BaseModel.__init__.__defaults__
        arg_index = args_name.index(f"{arg_name}")
        return default_value[arg_index]

    def get_welfare_value(self, market_situation: str) -> float:
        consumer_surplus = self.get_default_value(f"consumer_surplus_{market_situation}")
        incumbent_profit = self.get_default_value(f"incumbent_profit_{market_situation}")
        try:
            # handle case of duopoly
            startup_profit = self.get_default_value(f"startup_profit_{market_situation}")
        except ValueError:
            startup_profit = 0
        return consumer_surplus + incumbent_profit + startup_profit

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
            lambda: Model.BaseModel(consumer_surplus_with_innovation=0.2, consumer_surplus_without_innovation=0.3),
        )

    def test_invalid_success_probability(self):
        self.assertRaises(AssertionError, lambda: Model.BaseModel(success_probability=0))
        self.assertRaises(AssertionError, lambda: Model.BaseModel(success_probability=1.1))

    def test_properties(self):
        self.assertEqual(self.get_default_value("tolerated_level_of_harm"), self.model.tolerated_harm)
        self.assertEqual(self.get_default_value("development_costs"), self.model.development_costs)
        self.assertEqual(self.get_default_value("startup_assets"), self.model.startup_assets)
        self.assertEqual(self.get_default_value("success_probability"), self.model.success_probability)
        self.assertEqual(self.get_default_value("private_benefit"), self.model.private_benefit)
        self.assertEqual(
            self.get_default_value("consumer_surplus_without_innovation"), self.model.cs_without_innovation
        )
        self.assertEqual(
            self.get_default_value("incumbent_profit_without_innovation"),
            self.model.incumbent_profit_without_innovation,
        )
        self.assertEqual(self.get_default_value("consumer_surplus_duopoly"), self.model.cs_duopoly)
        self.assertEqual(self.get_default_value("incumbent_profit_duopoly"), self.model.incumbent_profit_duopoly)
        self.assertEqual(self.get_default_value("startup_profit_duopoly"), self.model.startup_profit_duopoly)
        self.assertEqual(self.get_default_value("consumer_surplus_with_innovation"), self.model.cs_with_innovation)
        self.assertEqual(
            self.get_default_value("incumbent_profit_with_innovation"), self.model.incumbent_profit_with_innovation
        )

    def test_welfare_properties(self):
        self.assertEqual(self.get_welfare_value("duopoly"), self.model.w_duopoly)
        self.assertEqual(self.get_welfare_value("without_innovation"), self.model.w_without_innovation)
        self.assertEqual(self.get_welfare_value("with_innovation"), self.model.w_with_innovation)


class TestMergerPolicyModel(TestBaseModel):
    def test_valid_setup_default_values(self):
        Model.MergerPolicyModel()
