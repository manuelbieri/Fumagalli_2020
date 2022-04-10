import unittest
from typing import Dict

import Fumagalli_Motta_Tarantino_2020.Model as Model


class TestBaseModel(unittest.TestCase):
    def test_valid_setup_default_values(self):
        Model.BaseModel()

    @staticmethod
    def get_default_value(arg_name: str) -> float:
        args_name = Model.BaseModel.__init__.__code__.co_varnames[
            1:
        ]  # "self" is not needed
        default_value = Model.BaseModel.__init__.__defaults__
        arg_index = args_name.index(f"{arg_name}")
        return default_value[arg_index]

    def get_welfare_value(self, market_situation: str) -> float:
        consumer_surplus = self.get_default_value(
            f"consumer_surplus_{market_situation}"
        )
        incumbent_profit = self.get_default_value(
            f"incumbent_profit_{market_situation}"
        )
        try:
            # handle case of duopoly
            startup_profit = self.get_default_value(
                f"startup_profit_{market_situation}"
            )
        except ValueError:
            startup_profit = 0
        return consumer_surplus + incumbent_profit + startup_profit

    def test_invalid_tolerated_harm(self):
        self.assertRaises(
            AssertionError, lambda: Model.BaseModel(tolerated_level_of_harm=-0.1)
        )

    def test_invalid_private_benefit(self):
        self.assertRaises(AssertionError, lambda: Model.BaseModel(private_benefit=-0.1))

    def test_invalid_profit(self):
        self.assertRaises(
            AssertionError,
            lambda: Model.BaseModel(
                incumbent_profit_without_innovation=0.2, incumbent_profit_duopoly=0.3
            ),
        )
        self.assertRaises(
            AssertionError,
            lambda: Model.BaseModel(
                incumbent_profit_with_innovation=0.2,
                incumbent_profit_without_innovation=0.3,
            ),
        )
        self.assertRaises(
            AssertionError,
            lambda: Model.BaseModel(
                incumbent_profit_with_innovation=0.2,
                incumbent_profit_duopoly=0.3,
                startup_profit_duopoly=0.2,
            ),
        )
        self.assertRaises(
            AssertionError,
            lambda: Model.BaseModel(
                startup_profit_duopoly=0.2,
                incumbent_profit_with_innovation=0.5,
                incumbent_profit_duopoly=0.3,
            ),
        )

    def test_invalid_consumer_surplus(self):
        self.assertRaises(
            AssertionError,
            lambda: Model.BaseModel(
                consumer_surplus_with_innovation=0.2,
                consumer_surplus_without_innovation=0.3,
            ),
        )

    def test_invalid_success_probability(self):
        self.assertRaises(
            AssertionError, lambda: Model.BaseModel(success_probability=0)
        )
        self.assertRaises(
            AssertionError, lambda: Model.BaseModel(success_probability=1.1)
        )

    def test_properties(self):
        self.model = Model.BaseModel()
        self.assertEqual(
            self.get_default_value("tolerated_level_of_harm"), self.model.tolerated_harm
        )
        self.assertEqual(
            self.get_default_value("development_costs"), self.model.development_costs
        )
        self.assertEqual(
            self.get_default_value("startup_assets"), self.model.startup_assets
        )
        self.assertEqual(
            self.get_default_value("success_probability"),
            self.model.success_probability,
        )
        self.assertTrue(self.model.development_success)
        self.assertEqual(
            self.get_default_value("private_benefit"), self.model.private_benefit
        )
        self.assertEqual(
            self.get_default_value("consumer_surplus_without_innovation"),
            self.model.cs_without_innovation,
        )
        self.assertEqual(
            self.get_default_value("incumbent_profit_without_innovation"),
            self.model.incumbent_profit_without_innovation,
        )
        self.assertEqual(
            self.get_default_value("consumer_surplus_duopoly"), self.model.cs_duopoly
        )
        self.assertEqual(
            self.get_default_value("incumbent_profit_duopoly"),
            self.model.incumbent_profit_duopoly,
        )
        self.assertEqual(
            self.get_default_value("startup_profit_duopoly"),
            self.model.startup_profit_duopoly,
        )
        self.assertEqual(
            self.get_default_value("consumer_surplus_with_innovation"),
            self.model.cs_with_innovation,
        )
        self.assertEqual(
            self.get_default_value("incumbent_profit_with_innovation"),
            self.model.incumbent_profit_with_innovation,
        )

    def test_welfare_properties(self):
        self.model = Model.BaseModel()
        self.assertEqual(self.get_welfare_value("duopoly"), self.model.w_duopoly)
        self.assertEqual(
            self.get_welfare_value("without_innovation"),
            self.model.w_without_innovation,
        )
        self.assertEqual(
            self.get_welfare_value("with_innovation"), self.model.w_with_innovation
        )


class TestMergerPolicyModel(TestBaseModel):
    def test_valid_setup_default_values(self):
        Model.MergerPolicyModel()


class TestLaissezFaireMergerPolicyModel(unittest.TestCase):
    def test_not_profitable_below_assets_threshold_not_credit_rationed(self):
        self.model = Model.MergerPolicyModel(tolerated_level_of_harm=1)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("Pooling", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_above_assets_threshold_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=1,
            startup_assets=0.01,
            private_benefit=0.099,
            success_probability=0.51,
            development_costs=0.1,
            startup_profit_duopoly=0.339,
            incumbent_profit_duopoly=0.01,
            incumbent_profit_with_innovation=0.35,
            consumer_surplus_with_innovation=0.4,
            incumbent_profit_without_innovation=0.3,
        )
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual("No", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_above_assets_threshold_not_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=1, private_benefit=0.075
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("No", self.model.get_early_bidding_type)
        self.assertEqual("Pooling", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertTrue(self.model.is_late_takeover)

    def test_not_profitable_below_assets_threshold_not_credit_rationed_unsuccessful(
        self,
    ):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=1, private_benefit=0.075, development_success=False
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("No", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=1,
            private_benefit=0.075,
            startup_assets=0.005,
            development_costs=0.076,
            success_probability=0.79,
            incumbent_profit_with_innovation=0.179,
            incumbent_profit_without_innovation=0.08,
            incumbent_profit_duopoly=0.05,
            startup_profit_duopoly=0.1,
        )
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual("Separating", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_not_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=1,
            private_benefit=0.075,
            development_costs=0.078,
            success_probability=0.76,
            incumbent_profit_with_innovation=0.51,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("Separating", self.model.get_early_bidding_type)
        self.assertEqual("Pooling", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertTrue(self.model.is_late_takeover)

    def test_profitable_not_credit_rationed_unsuccessful(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=1,
            private_benefit=0.075,
            development_costs=0.078,
            success_probability=0.76,
            incumbent_profit_with_innovation=0.51,
            development_success=False,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("Separating", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)


class TestIntermediateLateTakeoverAllowedMergerPolicyModel(unittest.TestCase):
    def test_not_profitable_not_credit_rationed(self):
        self.model = Model.MergerPolicyModel(tolerated_level_of_harm=0.06)
        self.assertEqual(
            "Intermediate (late takeover allowed)", self.model.merger_policy
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("No", self.model.get_early_bidding_type)
        self.assertEqual("Pooling", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertTrue(self.model.is_late_takeover)

    def test_not_profitable_not_credit_rationed_unsuccessful(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=0.06, development_success=False
        )
        self.assertEqual(
            "Intermediate (late takeover allowed)", self.model.merger_policy
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("No", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=0.06,
            startup_assets=0.01,
            private_benefit=0.099,
            success_probability=0.51,
            development_costs=0.1,
            startup_profit_duopoly=0.339,
            incumbent_profit_duopoly=0.01,
            incumbent_profit_with_innovation=0.35,
            consumer_surplus_with_innovation=0.4,
            incumbent_profit_without_innovation=0.3,
        )
        self.assertEqual(
            "Intermediate (late takeover allowed)", self.model.merger_policy
        )
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual("No", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_not_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=0.06, incumbent_profit_with_innovation=0.59
        )
        self.assertEqual(
            "Intermediate (late takeover allowed)", self.model.merger_policy
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("Separating", self.model.get_early_bidding_type)
        self.assertEqual("Pooling", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertTrue(self.model.is_late_takeover)

    def test_profitable_not_credit_rationed_unsuccessful(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=0.06,
            incumbent_profit_with_innovation=0.59,
            development_success=False,
        )
        self.assertEqual(
            "Intermediate (late takeover allowed)", self.model.merger_policy
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("Separating", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=0.12,
            private_benefit=0.075,
            startup_assets=0.005,
            development_costs=0.076,
            success_probability=0.79,
            incumbent_profit_with_innovation=0.179,
            incumbent_profit_without_innovation=0.08,
            incumbent_profit_duopoly=0.05,
            startup_profit_duopoly=0.1,
        )
        self.assertEqual(
            "Intermediate (late takeover allowed)", self.model.merger_policy
        )
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual("Separating", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)


class TestIntermediateLateTakeoverProhibitedMergerPolicyModel(unittest.TestCase):
    def test_not_profitable_below_assets_threshold_not_credit_rationed(self):
        self.model = Model.MergerPolicyModel(tolerated_level_of_harm=0.025)
        self.assertEqual(
            "Intermediate (late takeover prohibited)", self.model.merger_policy
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("Pooling", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_above_assets_threshold_not_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=0.025,
            success_probability=0.74,
            private_benefit=0.08,
            development_costs=0.09,
            incumbent_profit_without_innovation=0.38,
            startup_profit_duopoly=0.22,
        )
        self.assertEqual(
            "Intermediate (late takeover prohibited)", self.model.merger_policy
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("No", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_below_assets_threshold_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=0.025,
            development_costs=0.075,
            success_probability=0.79,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            startup_profit_duopoly=0.11,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertEqual(
            "Intermediate (late takeover prohibited)", self.model.merger_policy
        )
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual("Pooling", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_below_assets_threshold_not_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=0.025,
            startup_assets=0.06,
            development_costs=0.075,
            success_probability=0.79,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            startup_profit_duopoly=0.11,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertEqual(
            "Intermediate (late takeover prohibited)", self.model.merger_policy
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("Pooling", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_above_assets_threshold_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=0.17,
            startup_assets=0.055,
            development_costs=0.071,
            success_probability=0.75,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            consumer_surplus_duopoly=0.7,
            incumbent_profit_duopoly=0.29,
            startup_profit_duopoly=0.11,
            consumer_surplus_with_innovation=0.21,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertEqual(
            "Intermediate (late takeover prohibited)", self.model.merger_policy
        )
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual("Separating", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_above_assets_threshold_not_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=0.17,
            startup_assets=0.062,
            development_costs=0.071,
            success_probability=0.75,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            consumer_surplus_duopoly=0.7,
            incumbent_profit_duopoly=0.29,
            startup_profit_duopoly=0.11,
            consumer_surplus_with_innovation=0.21,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertEqual(
            "Intermediate (late takeover prohibited)", self.model.merger_policy
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("Separating", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)


class TestStrictMergerPolicyModel(unittest.TestCase):
    def test_not_profitable_not_credit_rationed_summary(self):
        self.model = Model.MergerPolicyModel()
        summary: Dict[str, any] = self.model.summary()
        self.assertFalse(summary["credit_rationed"])
        self.assertEqual("No", summary["early_bidding_type"])
        self.assertEqual("No", summary["late_bidding_type"])
        self.assertTrue(summary["development_attempt"])
        self.assertTrue(summary["development_outcome"])
        self.assertFalse(summary["early_takeover"])
        self.assertFalse(summary["late_takeover"])

    def test_not_profitable_not_credit_rationed(self):
        self.model = Model.MergerPolicyModel()
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("No", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            private_benefit=0.09, development_costs=0.11
        )
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual("No", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_below_assets_threshold_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            development_costs=0.075,
            success_probability=0.79,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            startup_profit_duopoly=0.11,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual("Pooling", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_below_assets_threshold_not_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            startup_assets=0.06,
            development_costs=0.075,
            success_probability=0.79,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            startup_profit_duopoly=0.11,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("Pooling", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_above_assets_threshold_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            development_costs=0.075,
            success_probability=0.75,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            consumer_surplus_duopoly=0.7,
            incumbent_profit_duopoly=0.25,
            startup_profit_duopoly=0.11,
            consumer_surplus_with_innovation=0.21,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual("Separating", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_above_assets_threshold_not_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            development_costs=0.075,
            startup_assets=0.065,
            success_probability=0.75,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            consumer_surplus_duopoly=0.7,
            incumbent_profit_duopoly=0.25,
            startup_profit_duopoly=0.11,
            consumer_surplus_with_innovation=0.21,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("Separating", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)


class TestOptimalMergerPolicyModel(TestMergerPolicyModel):
    def test_strict_optimal_merger_policy(self):
        self.model = Model.OptimalMergerPolicy()
        self.assertEqual("Strict", self.model.get_optimal_merger_policy())
        self.assertTrue(self.model.is_strict_optimal())

    def test_intermediate_optimal_merger_policy(self):
        self.model = Model.OptimalMergerPolicy(
            private_benefit=0.09,
            startup_profit_duopoly=0.15,
            incumbent_profit_duopoly=0.16,
            incumbent_profit_without_innovation=0.36,
        )
        self.assertEqual(
            "Intermediate (late takeover allowed)",
            self.model.get_optimal_merger_policy(),
        )
        self.assertTrue(self.model.is_intermediate_optimal())

    def test_laissez_faire_optimal_merger_policy(self):
        self.model = Model.OptimalMergerPolicy(
            development_costs=3,
            private_benefit=2,
            consumer_surplus_with_innovation=4,
            consumer_surplus_duopoly=6,
            consumer_surplus_without_innovation=2,
            incumbent_profit_duopoly=1,
            incumbent_profit_without_innovation=3,
            incumbent_profit_with_innovation=7,
            startup_profit_duopoly=5,
        )
        self.assertEqual("Laissez-faire", self.model.get_optimal_merger_policy())
        self.assertTrue(self.model.is_laissez_faire_optimal())
