import unittest

import Fumagalli_Motta_Tarantino_2020.tests.Test_Model as Test
import Fumagalli_Motta_Tarantino_2020.Types as Types

import Fumagalli_Motta_Tarantino_2020.AdditionalModels as AdditionalModels


class TestMircoFoundationModel(Test.TestOptimalMergerPolicyModel):
    def setUp(self) -> None:
        self.calculate_properties_profits_consumer_surplus()

    def setupModel(self, **kwargs) -> None:
        self.model = AdditionalModels.MicroFoundationModel(**kwargs)

    def calculate_properties_profits_consumer_surplus(self) -> None:
        # calculations made with Gamma = 0.2
        self.test_incumbent_profit_without_innovation = 0.25
        self.test_cs_without_innovation = 0.125

        self.test_incumbent_profit_with_innovation = 1 / 2.4
        self.test_cs_with_innovation = 1 / 4.8

        self.test_incumbent_profit_duopoly = 1 / (2.2**2)
        self.test_startup_profit_duopoly = self.test_incumbent_profit_duopoly
        self.test_cs_duopoly = 1.2 / (2.2**2)

    def get_welfare_value(self, market_situation: str) -> float:
        if market_situation == "duopoly":
            return (
                self.test_cs_duopoly
                + self.test_startup_profit_duopoly
                + self.test_incumbent_profit_duopoly
            )
        if market_situation == "without_innovation":
            return (
                self.test_cs_without_innovation
                + self.test_incumbent_profit_without_innovation
            )
        if market_situation == "with_innovation":
            return (
                self.test_cs_with_innovation
                + self.test_incumbent_profit_with_innovation
            )

    def test_properties_profits_consumer_surplus(self):
        self.setupModel()
        self.assertTrue(
            self.are_floats_equal(
                self.test_cs_without_innovation, self.model.cs_without_innovation
            )
        )
        self.assertTrue(
            self.are_floats_equal(
                self.test_incumbent_profit_without_innovation,
                self.model.incumbent_profit_without_innovation,
            )
        )
        self.assertTrue(
            self.are_floats_equal(
                self.test_cs_duopoly,
                self.model.cs_duopoly,
            )
        )
        self.assertTrue(
            self.are_floats_equal(
                self.test_incumbent_profit_duopoly,
                self.model.incumbent_profit_duopoly,
            )
        )
        self.assertTrue(
            self.are_floats_equal(
                self.test_startup_profit_duopoly,
                self.model.startup_profit_duopoly,
            )
        )
        self.assertTrue(
            self.are_floats_equal(
                self.test_cs_with_innovation,
                self.model.cs_with_innovation,
            )
        )
        self.assertTrue(
            self.are_floats_equal(
                self.test_incumbent_profit_with_innovation,
                self.model.incumbent_profit_with_innovation,
            )
        )

    @unittest.skip("Not yet implemented")
    def test_intermediate_optimal_merger_policy(self):
        pass

    def test_laissez_faire_optimal_merger_policy(self):
        # laissez-faire is never optimal -> dominated by strict
        self.setupModel()
        self.assertFalse(self.model.is_laissez_faire_optimal())


class TestPerfectInformationModel(Test.TestOptimalMergerPolicyModel):
    def setupModel(self, **kwargs) -> None:
        self.model = AdditionalModels.PerfectInformationModel(**kwargs)

    def test_laissez_faire_optimal_merger_policy(self):
        self.setupModel()
        self.assertFalse(self.model.is_laissez_faire_optimal())


class TestStrictPerfectInformationModel(TestPerfectInformationModel):
    def test_not_profitable_not_credit_rationed(self):
        self.setupModel()
        self.assertEqual(Types.MergerPolicies.Strict, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(Types.Takeover.No, self.model.get_early_bidding_type)
        self.assertEqual(Types.Takeover.No, self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_credit_rationed(self):
        self.setupModel(startup_assets=0.01)
        self.assertEqual(Types.MergerPolicies.Strict, self.model.merger_policy)
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(Types.Takeover.No, self.model.get_early_bidding_type)
        self.assertEqual(Types.Takeover.No, self.model.get_late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_not_credit_rationed(self):
        self.setupModel(
            startup_assets=0.06,
            development_costs=0.075,
            success_probability=0.79,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            startup_profit_duopoly=0.11,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertEqual(Types.MergerPolicies.Strict, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(Types.Takeover.No, self.model.get_early_bidding_type)
        self.assertEqual(Types.Takeover.No, self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_credit_rationed(self):
        self.setupModel(
            development_costs=0.075,
            success_probability=0.79,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            startup_profit_duopoly=0.11,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertEqual(Types.MergerPolicies.Strict, self.model.merger_policy)
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(Types.Takeover.Separating, self.model.get_early_bidding_type)
        self.assertEqual(Types.Takeover.No, self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)


class TestIntermediatePerfectInformationModel(TestPerfectInformationModel):
    def test_not_profitable_not_credit_rationed(self):
        self.setupModel(
            tolerated_level_of_harm=0.06,
            consumer_surplus_duopoly=0.46,
            consumer_surplus_without_innovation=0.2,
            consumer_surplus_with_innovation=0.35,
        )
        self.assertEqual(
            Types.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(Types.Takeover.No, self.model.get_early_bidding_type)
        self.assertEqual(Types.Takeover.Pooling, self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertTrue(self.model.is_late_takeover)

    def test_not_profitable_not_credit_rationed_unsuccessful(self):
        self.setupModel(
            tolerated_level_of_harm=0.06,
            consumer_surplus_duopoly=0.46,
            consumer_surplus_without_innovation=0.2,
            consumer_surplus_with_innovation=0.35,
            development_success=False,
        )
        self.assertEqual(
            Types.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(Types.Takeover.No, self.model.get_early_bidding_type)
        self.assertEqual(Types.Takeover.No, self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_not_credit_rationed(self):
        self.setupModel(
            tolerated_level_of_harm=0.06,
            development_costs=0.09,
            incumbent_profit_without_innovation=0.35,
            consumer_surplus_duopoly=0.46,
            consumer_surplus_without_innovation=0.2,
            consumer_surplus_with_innovation=0.35,
        )
        self.assertEqual(
            Types.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(Types.Takeover.Pooling, self.model.get_early_bidding_type)
        self.assertEqual(Types.Takeover.No, self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_credit_rationed(self):
        self.setupModel(
            tolerated_level_of_harm=0.1,
            private_benefit=0.075,
            startup_assets=0.005,
            development_costs=0.076,
            success_probability=0.79,
            incumbent_profit_with_innovation=0.179,
            incumbent_profit_without_innovation=0.08,
            incumbent_profit_duopoly=0.05,
            startup_profit_duopoly=0.1,
            consumer_surplus_duopoly=0.46,
            consumer_surplus_without_innovation=0.2,
            consumer_surplus_with_innovation=0.35,
        )
        self.assertEqual(
            Types.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(Types.Takeover.Separating, self.model.get_early_bidding_type)
        self.assertEqual(Types.Takeover.No, self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)


class TestLaissezFairePerfectInformationModel(TestPerfectInformationModel):
    def test_not_profitable_not_credit_rationed(self):
        self.setupModel(tolerated_level_of_harm=1)
        self.assertEqual(Types.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(Types.Takeover.Pooling, self.model.get_early_bidding_type)
        self.assertEqual(Types.Takeover.No, self.model.get_late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_credit_rationed(self):
        self.setupModel(
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
        self.assertEqual(Types.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(Types.Takeover.No, self.model.get_early_bidding_type)
        self.assertEqual(Types.Takeover.No, self.model.get_late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_not_credit_rationed(self):
        self.setupModel(
            tolerated_level_of_harm=1,
            private_benefit=0.075,
            development_costs=0.078,
            success_probability=0.76,
            incumbent_profit_with_innovation=0.51,
        )
        self.assertEqual(Types.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(Types.Takeover.Pooling, self.model.get_early_bidding_type)
        self.assertEqual(Types.Takeover.No, self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_credit_rationed(self):
        self.setupModel(
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
        self.assertEqual(Types.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(Types.Takeover.Separating, self.model.get_early_bidding_type)
        self.assertEqual(Types.Takeover.No, self.model.get_late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)
