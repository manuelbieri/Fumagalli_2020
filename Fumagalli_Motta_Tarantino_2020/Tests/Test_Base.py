from typing import Literal

import unittest
import Fumagalli_Motta_Tarantino_2020 as FMT20


class CoreTest(unittest.TestCase):
    """
    Provides useful methods for the use in tests.
    """

    @staticmethod
    def are_floats_equal(f1: float, f2: float, tolerance: float = 10 ** (-10)) -> float:
        """
        Compares two floats for equality with respect to a tolerance.

        Parameters
        ----------
        f1: float
            First float for the comparison
        f2: float
            Second float for the comparison
        tolerance: float
            Max. difference between the floats to consider them equal

        Returns
        -------
        True
            If the floats are equal
        """
        return abs(f1 - f2) < tolerance

    @staticmethod
    def get_default_value(arg_name: str, model=FMT20.CoreModel) -> float:
        """
        Returns the default value of a parameters of specific model.

        Parameters
        ----------
        arg_name: str
            Name of the parameter
        model
            Type of the model to get the default value from

        Returns
        -------
        float
            Default value of the parameter
        """
        args_name = model.__init__.__code__.co_varnames[1:]  # "self" is not needed
        default_value = model.__init__.__defaults__
        arg_index = args_name.index(f"{arg_name}")
        return default_value[arg_index]

    def get_welfare_value(
        self,
        market_situation: Literal["duopoly", "with_innovation", "without_innovation"],
        model=FMT20.CoreModel,
    ) -> float:
        """
        Calculates the default value of welfare for a specific model and market situation.

        Market situations:
        - duopoly
        - monopoly with innovation
        - monopoly without innovation

        Parameters
        ----------
        market_situation: Literal["duopoly", "with_innovation", "without_innovation"]
            To calculate the total welfare for
        model
            Type of the model to get the default value from

        Returns
        -------
        float
            Default value of the total welfare
        """
        consumer_surplus = CoreTest.get_default_value(
            f"consumer_surplus_{market_situation}", model
        )
        incumbent_profit = CoreTest.get_default_value(
            f"incumbent_profit_{market_situation}", model
        )
        try:
            # handle case of duopoly
            startup_profit = CoreTest.get_default_value(
                f"startup_profit_{market_situation}", model
            )
        except ValueError:
            startup_profit = 0
        return consumer_surplus + incumbent_profit + startup_profit


class TestCoreModel(CoreTest):
    """
    Provides methods for model setup and tests valid setup of model.
    """

    def setupModel(self, **kwargs) -> None:
        """
        Sets up a model for a test.

        The type of the model is corresponding to the testcase.

        Parameters
        ----------
        **kwargs
            Parameter values for the model
        """
        self.model = FMT20.CoreModel(**kwargs)

    def setUpConfiguration(
        self, config_id: int, merger_policy=FMT20.MergerPolicies.Strict, **kwargs
    ) -> None:
        """
        Sets up a model from a preset configuration.

        Parameters
        ----------
        config_id: int
            ID of the preset configuration
        merger_policy: FMT20.MergerPolicies
            Merger policy to set in the model.
        **kwargs
            Parameter values for the model
        """
        config = FMT20.LoadParameters(config_id)
        config.adjust_parameters(**kwargs)
        config.params.merger_policy = merger_policy
        self.setupModel(**config())

    def test_valid_setup_default_values(self):
        self.setupModel()

    def test_uniform_distribution(self):
        self.setupModel(
            asset_distribution=FMT20.Distributions.UniformDistribution,
            standard_distribution=False,
        )
        self.assertEqual(
            1,
            self.model.asset_distribution.cumulative(
                self.model.development_costs, **self.model.asset_distribution_kwargs
            ),
        )


class TestProperties(TestCoreModel):
    """
    Tests properties for Fumagalli_Motta_Tarantino_2020.Models.Base.MergerPolicy.
    """

    def setUp(self) -> None:
        self.model_type = self.get_model_type()
        self.model = self.model_type()

    @staticmethod
    def get_model_type():
        return FMT20.MergerPolicy

    def abstract_property_test(
        self, property_, property_name: str, invalid_value=120
    ) -> None:
        """
        Skeleton for all tests of model properties.

        Example
        --------
        ```
        model = FMT20.OptimalMergerPolicy()
        self.abstract_property_test(model_type.startup_assets, "startup_assets")
        ```

        Parameters
        ----------
        property_
            Property of the model
        property_name: str
            Name of the property as a string
        invalid_value: int
            Invalid value for the property
        """
        value = self.get_default_value(property_name)
        self._test_get(property_, value)
        self._test_valid_set(property_, value)
        self._test_invalid_set(property_, invalid_value)

    def _test_get(self, property_, value):
        self.assertTrue(self.are_floats_equal(value, property_.fget(self.model)))

    def _test_invalid_set(self, property_, invalid_value):
        self.assertRaises(
            AssertionError, lambda: property_.fset(self.model, invalid_value)
        )

    def _test_valid_set(self, property_, value):
        value += 0.01
        property_.fset(self.model, value)
        self.assertTrue(self.are_floats_equal(value, value, property_.fget(self.model)))

    def test_development_costs(self):
        self.abstract_property_test(
            self.model_type.development_costs, "development_costs"
        )

    def test_startup_assets(self):
        self.abstract_property_test(self.model_type.startup_assets, "startup_assets")

    def test_success_probability(self):
        self.abstract_property_test(
            self.model_type.success_probability, "success_probability"
        )

    def test_private_benefit(self):
        self.abstract_property_test(self.model_type.private_benefit, "private_benefit")

    def test_incumbent_profit_without_innovation(self):
        self.abstract_property_test(
            self.model_type.incumbent_profit_without_innovation,
            "incumbent_profit_without_innovation",
        )

    def test_incumbent_profit_duopoly(self):
        self.abstract_property_test(
            self.model_type.incumbent_profit_duopoly, "incumbent_profit_duopoly"
        )

    def test_incumbent_profit_with_innovation(self):
        self.abstract_property_test(
            self.model_type.incumbent_profit_with_innovation,
            "incumbent_profit_with_innovation",
        )

    def test_startup_profit_duopoly(self):
        self.abstract_property_test(
            self.model_type.startup_profit_duopoly, "startup_profit_duopoly"
        )

    def test_consumer_surplus_with_innovation(self):
        self.abstract_property_test(
            self.model_type.cs_with_innovation, "consumer_surplus_with_innovation"
        )

    def test_consumer_surplus_without_innovation(self):
        self.abstract_property_test(
            self.model_type.cs_without_innovation, "consumer_surplus_without_innovation"
        )

    def test_consumer_surplus_duopoly(self):
        self.abstract_property_test(
            self.model_type.cs_duopoly, "consumer_surplus_duopoly", invalid_value=0
        )

    def test_welfare_without_innovation(self):
        self.assertEqual(
            self.get_welfare_value("without_innovation"),
            self.model.w_without_innovation,
        )

    def test_welfare_with_innovation(self):
        self.assertEqual(
            self.get_welfare_value("with_innovation"), self.model.w_with_innovation
        )

    def test_welfare_duopoly(self):
        self.assertEqual(self.get_welfare_value("duopoly"), self.model.w_duopoly)

    def test_development_success(self):
        self.assertTrue(self.model.development_success)
        self.model.development_success = False
        self.assertFalse(self.model.development_success)
        self.assertRaises(
            AssertionError,
            lambda: self.model_type.development_success.fset(self.model, None),
        )

    def test_invalid_merger_policy(self):
        self.assertRaises(AssertionError, lambda: self.setupModel(merger_policy=None))


class TestMergerPolicy(TestCoreModel):
    """
    Tests Fumagalli_Motta_Tarantino_2020.Models.Base.MergerPolicy.
    """

    def setupModel(self, **kwargs) -> None:
        self.model = FMT20.MergerPolicy(**kwargs)

    def test_tolerated_harm_strict(self):
        self.setupModel()
        self.assertTrue(
            self.are_floats_equal(
                0.014561171, self.model.tolerated_harm, tolerance=10**-8
            )
        )

    def test_tolerated_harm_intermediate_late_takeover_allowed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_prohibited
        )
        self.assertTrue(
            self.are_floats_equal(
                0.054561171, self.model.tolerated_harm, tolerance=10**-8
            )
        )

    def test_tolerated_harm_intermediate_late_takeover_prohibited(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed
        )
        self.assertTrue(
            self.are_floats_equal(0.1, self.model.tolerated_harm, tolerance=10**-8)
        )

    def test_tolerated_harm_laissez_faire(self):
        self.setupModel(merger_policy=FMT20.MergerPolicies.Laissez_faire)
        self.assertEqual(float("inf"), self.model.tolerated_harm)


class TestLaissezFaireMergerPolicy(TestMergerPolicy):
    def test_not_profitable_below_assets_threshold_not_credit_rationed(self):
        self.setupModel(merger_policy=FMT20.MergerPolicies.Laissez_faire)
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Pooling, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)
        self.assertTrue(self.model.is_killer_acquisition())

    def test_not_profitable_above_assets_threshold_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Laissez_faire,
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
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)
        self.assertFalse(self.model.is_killer_acquisition())

    def test_not_profitable_above_assets_threshold_not_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Laissez_faire, private_benefit=0.075
        )
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.Pooling, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertTrue(self.model.is_late_takeover)
        self.assertFalse(self.model.is_killer_acquisition())

    def test_not_profitable_below_assets_threshold_not_credit_rationed_unsuccessful(
        self,
    ):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Laissez_faire,
            private_benefit=0.075,
            development_success=False,
        )
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)
        self.assertFalse(self.model.is_killer_acquisition())

    def test_profitable_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Laissez_faire,
            private_benefit=0.075,
            startup_assets=0.005,
            development_costs=0.076,
            success_probability=0.79,
            incumbent_profit_with_innovation=0.179,
            incumbent_profit_without_innovation=0.08,
            incumbent_profit_duopoly=0.05,
            startup_profit_duopoly=0.1,
        )
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Separating, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)
        self.assertFalse(self.model.is_killer_acquisition())

    def test_profitable_not_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Laissez_faire,
            private_benefit=0.075,
            development_costs=0.078,
            success_probability=0.76,
            incumbent_profit_with_innovation=0.51,
        )
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Separating, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.Pooling, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertTrue(self.model.is_late_takeover)
        self.assertFalse(self.model.is_killer_acquisition())

    def test_profitable_not_credit_rationed_unsuccessful(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Laissez_faire,
            private_benefit=0.075,
            development_costs=0.078,
            success_probability=0.76,
            incumbent_profit_with_innovation=0.51,
            development_success=False,
        )
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Separating, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)
        self.assertFalse(self.model.is_killer_acquisition())


class TestIntermediateLateTakeoverAllowedMergerPolicy(TestMergerPolicy):
    def test_not_profitable_not_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.Pooling, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertTrue(self.model.is_late_takeover)

    def test_not_profitable_not_credit_rationed_unsuccessful(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            development_success=False,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
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
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_not_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            incumbent_profit_with_innovation=0.59,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Separating, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.Pooling, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertTrue(self.model.is_late_takeover)

    def test_profitable_not_credit_rationed_unsuccessful(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            incumbent_profit_with_innovation=0.59,
            development_success=False,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Separating, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
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
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Separating, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)


class TestIntermediateLateTakeoverProhibitedMergerPolicy(TestMergerPolicy):
    def test_not_profitable_below_assets_threshold_not_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_prohibited
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
            self.model.merger_policy,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Pooling, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_above_assets_threshold_not_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
            success_probability=0.74,
            private_benefit=0.08,
            development_costs=0.09,
            incumbent_profit_without_innovation=0.38,
            startup_profit_duopoly=0.22,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
            self.model.merger_policy,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_below_assets_threshold_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
            development_costs=0.075,
            success_probability=0.79,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            startup_profit_duopoly=0.11,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
            self.model.merger_policy,
        )
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Pooling, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_below_assets_threshold_not_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
            startup_assets=0.06,
            development_costs=0.075,
            success_probability=0.79,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            startup_profit_duopoly=0.11,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
            self.model.merger_policy,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Pooling, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_above_assets_threshold_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
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
            FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
            self.model.merger_policy,
        )
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Separating, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_above_assets_threshold_not_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
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
            FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
            self.model.merger_policy,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Separating, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)


class TestStrictMergerPolicy(TestMergerPolicy):
    def test_not_profitable_not_credit_rationed_summary(self):
        self.setupModel()
        summary: FMT20.Summary = self.model.summary()
        self.assertEqual(FMT20.MergerPolicies.Strict, self.model.merger_policy)
        self.assertFalse(summary.credit_rationed)
        self.assertEqual(FMT20.Takeover.No, summary.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, summary.late_bidding_type)
        self.assertTrue(summary.development_attempt)
        self.assertTrue(summary.development_outcome)
        self.assertFalse(summary.early_takeover)
        self.assertFalse(summary.late_takeover)

    def test_not_profitable_not_credit_rationed(self):
        self.setupModel()
        self.assertEqual(FMT20.MergerPolicies.Strict, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_credit_rationed(self):
        self.setupModel(private_benefit=0.09, development_costs=0.11)
        self.assertEqual(FMT20.MergerPolicies.Strict, self.model.merger_policy)
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_set_startup_assets_recalculation(self):
        self.setupModel(
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
        self.assertTrue(self.model.is_early_takeover)
        self.model.startup_assets = 0.065
        self.assertFalse(self.model.is_early_takeover)

    def test_set_tolerated_harm_recalculation(self):
        self.setupModel()
        self.assertEqual(FMT20.MergerPolicies.Strict, self.model.merger_policy)
        self.model.merger_policy = FMT20.MergerPolicies.Laissez_faire
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, self.model.merger_policy)

    def test_set_merger_policy(self):
        self.setupModel()
        self.assertEqual(FMT20.MergerPolicies.Strict, self.model.merger_policy)
        self.model.merger_policy = (
            FMT20.MergerPolicies.Intermediate_late_takeover_prohibited
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
            self.model.merger_policy,
        )
        self.model.merger_policy = (
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.model.merger_policy = FMT20.MergerPolicies.Laissez_faire
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.model.merger_policy = FMT20.MergerPolicies.Strict
        self.assertEqual(FMT20.MergerPolicies.Strict, self.model.merger_policy)

    def test_profitable_below_assets_threshold_credit_rationed(self):
        self.setupModel(
            development_costs=0.075,
            success_probability=0.79,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            startup_profit_duopoly=0.11,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertEqual(FMT20.MergerPolicies.Strict, self.model.merger_policy)
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Pooling, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_below_assets_threshold_not_credit_rationed(self):
        self.setupModel(
            startup_assets=0.06,
            development_costs=0.075,
            success_probability=0.79,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            startup_profit_duopoly=0.11,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertEqual(FMT20.MergerPolicies.Strict, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Pooling, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_above_assets_threshold_credit_rationed(self):
        self.setupModel(
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
        self.assertEqual(FMT20.MergerPolicies.Strict, self.model.merger_policy)
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Separating, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_above_assets_threshold_not_credit_rationed(self):
        self.setupModel(
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
        self.assertEqual(FMT20.MergerPolicies.Strict, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Separating, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)


class TestOptimalMergerPolicy(TestMergerPolicy):
    """
    Tests Fumagalli_Motta_Tarantino_2020.Models.Base.OptimalMergerPolicy.
    """

    def setupModel(self, **kwargs) -> None:
        self.model = FMT20.OptimalMergerPolicy(**kwargs)

    def test_strict_optimal_merger_policy_summary(self):
        self.setupModel()
        summary: FMT20.OptimalMergerPolicySummary = self.model.summary()
        self.assertEqual(FMT20.MergerPolicies.Strict, summary.optimal_policy)

    def test_strict_optimal_merger_policy(self):
        self.setupModel()
        self.assertEqual(
            FMT20.MergerPolicies.Strict, self.model.get_optimal_merger_policy()
        )
        self.assertTrue(self.model.is_strict_optimal())

    def test_intermediate_optimal_merger_policy(self):
        self.setupModel(
            private_benefit=0.09,
            startup_profit_duopoly=0.15,
            incumbent_profit_duopoly=0.16,
            incumbent_profit_without_innovation=0.36,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.get_optimal_merger_policy(),
        )
        self.assertTrue(self.model.is_intermediate_optimal())

    def test_laissez_faire_optimal_merger_policy(self):
        self.setupModel(
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
        self.assertEqual(
            FMT20.MergerPolicies.Laissez_faire, self.model.get_optimal_merger_policy()
        )
        self.assertTrue(self.model.is_laissez_faire_optimal())

    def test_string_representation(self):
        self.setupModel()
        self.assertEqual(
            "Merger Policy: Strict\n"
            "Is start-up credit rationed?: False\n"
            "Type of early takeover attempt: No bid\n"
            "Is the early takeover approved?: False\n"
            "Does the owner attempt the development?: True\n"
            "Is the development successful?: True\n"
            "Type of late takeover attempt: No bid\n"
            "Is the late takeover approved?: False\n"
            "Optimal merger policy: Strict",
            str(self.model),
        )
