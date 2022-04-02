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


class TestLaissezFaireMergerPolicyModel(TestMergerPolicyModel):
    def test_laissez_faire_default_outcome(self):
        self.model = Model.MergerPolicyModel(tolerated_level_of_harm=1)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("Pooling", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_laissez_faire_no_early_takeover_credit_rationed(self):
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

    def test_laissez_faire_no_early_takeover_not_credit_rationed(self):
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

    def test_laissez_faire_no_early_takeover_not_credit_rationed_unsuccessful(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=1, private_benefit=0.075,
            development_success=False
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("No", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_laissez_faire_early_takeover_credit_rationed(self):
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

    def test_laissez_faire_early_takeover_not_credit_rationed(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=1,
            private_benefit=0.075,
            development_costs=0.076,
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

    def test_laissez_faire_early_takeover_not_credit_rationed_unsuccessful(self):
        self.model = Model.MergerPolicyModel(
            tolerated_level_of_harm=1,
            private_benefit=0.075,
            development_costs=0.076,
            success_probability=0.76,
            incumbent_profit_with_innovation=0.51,
            development_success=False
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("Separating", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)


@unittest.skip("Not implemented")
class TestIntermediateLateTakeoverAllowedMergerPolicyModel(TestMergerPolicyModel):
    pass


@unittest.skip("Not implemented")
class TestIntermediateLateTakeoverProhibitedMergerPolicyModel(TestMergerPolicyModel):
    pass


class TestStrictMergerPolicyModel(TestMergerPolicyModel):
    def test_strict_merger_policy_default_outcome_summary(self):
        self.model = Model.MergerPolicyModel()
        summary: Dict[str, any] = self.model.summary()
        self.assertFalse(summary['credit_rationed'])
        self.assertEqual("No", summary['early_bidding_type'])
        self.assertEqual("No", summary['late_bidding_type'])
        self.assertTrue(summary['development_attempt'])
        self.assertTrue(summary['development_outcome'])
        self.assertFalse(summary['early_takeover'])
        self.assertFalse(summary['late_takeover'])

    def test_strict_merger_policy_default_outcome(self):
        self.model = Model.MergerPolicyModel()
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual("No", self.model.get_early_bidding_type)
        self.assertEqual("No", self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_strict_merger_policy_credit_rationed(self):
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

    def test_strict_merger_policy_pooling_bid(self):
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

    def test_strict_merger_policy_separating_bid(self):
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
