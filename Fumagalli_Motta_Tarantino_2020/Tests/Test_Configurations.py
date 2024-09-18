import unittest
import Fumagalli_Motta_Tarantino_2020.Tests.Mock as Mock

import Fumagalli_Motta_Tarantino_2020 as FMT20


class TestLoadParameters(unittest.TestCase):
    """
    Tests the loading of preset configurations.

    See: Fumagalli_Motta_Tarantino_2020.Configurations.LoadConfig and
    Fumagalli_Motta_Tarantino_2020.Configurations.StoreConfig.
    """

    def setUpModel(self, config_id: int):
        self.config = FMT20.LoadParameters(config_id)
        self.model = FMT20.OptimalMergerPolicy(**self.config())

    def test_config_loading(self):
        self.setUpModel(2)
        self.assertFalse(self.model.is_early_takeover)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_incumbent_expected_to_shelve())

    def test_startup_assets(self):
        self.setUpModel(2)
        self.assertEqual(0.05, self.config.params.params["startup_assets"])
        self.config.set_startup_assets(0.09)
        m = FMT20.OptimalMergerPolicy(**self.config())
        self.assertEqual(0.09, m.startup_assets)

    def test_merger_policy(self):
        self.setUpModel(2)
        self.assertEqual(FMT20.MergerPolicies.Strict, self.config.params.merger_policy)
        self.config.set_merger_policy(FMT20.MergerPolicies.Laissez_faire)
        m = FMT20.OptimalMergerPolicy(**self.config())
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, m.merger_policy)

    def test_toggle_development_success(self):
        self.setUpModel(2)
        self.assertTrue(self.model.is_development_successful)
        self.config.toggle_development_success()
        m = FMT20.OptimalMergerPolicy(**self.config())
        self.assertFalse(m.is_development_successful)

    def test_adjust_parameter(self):
        self.setUpModel(2)
        self.assertEqual(0.1, self.config.params.get("development_costs"))
        self.config.adjust_parameters(development_costs=0.2)
        self.assertEqual(0.2, self.config.params.get("development_costs"))

    def test_load_unavailable_id(self):
        self.assertRaises(
            FMT20.ConfigExceptions.IDNotAvailableError, lambda: self.setUpModel(0)
        )


class TestFindParameters(unittest.TestCase):
    """
    Tests Fumagalli_Motta_Tarantino_2020.Configurations.FindConfig.
    """

    @staticmethod
    def setUpModel(config: FMT20.ParameterModel) -> FMT20.OptimalMergerPolicy:
        return FMT20.OptimalMergerPolicy(
            **config(), asset_distribution=FMT20.Distributions.UniformDistribution
        )

    @staticmethod
    def parameter_in_range(value) -> bool:
        return 0 < value < 1

    def test_parameter_generator(self):
        params: (
            FMT20.ParameterModel
        ) = FMT20.ParameterModelGenerator().get_parameter_model(
            merger_policy=FMT20.MergerPolicies.Laissez_faire,
            development_success=False,
        )
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, params.merger_policy)
        self.assertTrue(self.parameter_in_range(params.get("development_costs")))
        self.assertTrue(self.parameter_in_range(params.get("startup_assets")))
        self.assertTrue(self.parameter_in_range(params.get("success_probability")))
        self.assertTrue(self.parameter_in_range(params.get("private_benefit")))
        self.assertFalse(self.parameter_in_range(params.get("development_success")))

    def test_strict_optimal(self):
        config = FMT20.RandomConfig(
            parameter_generator=Mock.mock_parameter_model_generator(
                strict_optimal=True
            ),
            strict_optimal=True,
        ).find_config()
        model = self.setUpModel(config)
        self.assertTrue(model.is_strict_optimal())
        self.assertEqual(0.54, config.params.get("development_costs"))

    def test_intermediate_optimal(self):
        config = FMT20.RandomConfig(
            parameter_generator=Mock.mock_parameter_model_generator(
                intermediate_optimal=True
            ),
            intermediate_optimal=True,
        ).find_config()
        model = self.setUpModel(config)
        self.assertTrue(model.is_intermediate_optimal())
        self.assertEqual(0.59, config.params.get("development_costs"))

    def test_laissez_faire_optimal(self):
        config = FMT20.RandomConfig(
            parameter_generator=Mock.mock_parameter_model_generator(
                laissez_faire_optimal=True
            ),
            laissez_faire_optimal=True,
        ).find_config()
        model = self.setUpModel(config)
        self.assertTrue(model.is_laissez_faire_optimal())
        self.assertEqual(0.46, config.params.get("development_costs"))

    def test_laissez_faire_killer_acquisition(self):
        config = FMT20.RandomConfig(
            parameter_generator=Mock.mock_parameter_model_generator(
                killer_acquisition=True
            ),
            is_killer_acquisition=True,
            merger_policy=FMT20.MergerPolicies.Laissez_faire,
        ).find_config()
        model = self.setUpModel(config)
        self.assertTrue(model.is_killer_acquisition())
        self.assertEqual(0.54, config.params.get("development_costs"))

    def test_invalid_parameter_model(self):
        config = FMT20.RandomConfig(
            parameter_generator=Mock.mock_parameter_model_generator(
                invalid_parameter_model=True
            ),
        ).find_config()
        model = self.setUpModel(config)
        self.assertTrue(model.is_intermediate_optimal())

    def test_callable_condition(self):
        config = FMT20.RandomConfig(
            parameter_generator=Mock.mock_parameter_model_generator(
                callable_condition=True
            ),
            callable_condition=lambda m: m.development_costs < 0.5,
        ).find_config()
        model = self.setUpModel(config)
        self.assertTrue(model.development_costs < 0.5)

    def test_two_conditions(self):
        config = FMT20.RandomConfig(
            parameter_generator=Mock.mock_parameter_model_generator(
                two_conditions=True, killer_acquisition=True
            ),
            intermediate_optimal=True,
            is_killer_acquisition=True,
            merger_policy=FMT20.MergerPolicies.Laissez_faire,
        ).find_config()
        model = self.setUpModel(config)
        self.assertTrue(model.is_intermediate_optimal())
        self.assertTrue(model.is_killer_acquisition())

    def test_two_conditions_callable(self):
        config = FMT20.RandomConfig(
            parameter_generator=Mock.mock_parameter_model_generator(
                two_conditions=True
            ),
            laissez_faire_optimal=True,
            callable_condition=lambda m: m.development_costs > 0.4,
        ).find_config()
        model = self.setUpModel(config)
        self.assertTrue(model.development_costs > 0.4)
        self.assertTrue(model.is_laissez_faire_optimal())
