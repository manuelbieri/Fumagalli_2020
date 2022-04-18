import unittest

import Fumagalli_Motta_Tarantino_2020.tests.Test_Model as Test
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
