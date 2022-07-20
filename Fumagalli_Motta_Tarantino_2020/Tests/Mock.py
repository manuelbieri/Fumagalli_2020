import unittest.mock as mock
from mockito import when

import Fumagalli_Motta_Tarantino_2020 as FMT20


def mock_optimal_merger_policy(
    asset_threshold: float = 0.5,
    asset_threshold_late_takeover: float = -1,
    credit_constrained: bool = False,
    policy: FMT20.MergerPolicies = FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
    **kwargs
) -> FMT20.OptimalMergerPolicy:
    """
    Creates a mock model of Fumagalli_Motta_Tarantino_2020.Models.OptimalMergerPolicy.
    """

    def set_outcome(model_outcome, **kwargs_outcome):
        """
        Sets properties concerning the outcome in the model.

        Notes
        -----
        This function overrides all the logic in the model, with the given values.
        """
        if kwargs_outcome.get("set_outcome", False):
            type(model_outcome).is_owner_investing = kwargs_outcome.get(
                "is_owner_investing", False
            )
            type(model_outcome).is_early_takeover = kwargs_outcome.get(
                "is_early_takeover", True
            )
            type(model_outcome).is_late_takeover = kwargs_outcome.get(
                "is_late_takeover", False
            )
            type(model_outcome).is_development_successful = kwargs_outcome.get(
                "is_development_successful", False
            )

    def set_summary(
        credit_rationed=False,
        early_bidding_type=FMT20.Takeover.No,
        late_bidding_type=FMT20.Takeover.No,
        development_attempt=True,
        development_outcome=True,
        early_takeover=False,
        late_takeover=False,
        set_policy=policy,
    ) -> FMT20.OptimalMergerPolicySummary:
        """
        Sets the returned summary for the model.
        """
        return FMT20.OptimalMergerPolicySummary(
            credit_rationed=credit_rationed,
            set_policy=set_policy,
            early_bidding_type=early_bidding_type,
            late_bidding_type=late_bidding_type,
            development_attempt=development_attempt,
            development_outcome=development_outcome,
            early_takeover=early_takeover,
            late_takeover=late_takeover,
            optimal_policy=set_policy,
        )

    def summary(
        merger_policy: FMT20.MergerPolicies = FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
    ):
        """
        Regulates the returned summaries given the asset thresholds.
        """
        if model.startup_assets < asset_threshold_late_takeover:
            return set_summary(
                credit_rationed=True,
                development_attempt=False,
                development_outcome=False,
                early_bidding_type=FMT20.Takeover.Separating,
                early_takeover=True,
                set_policy=merger_policy,
            )
        if model.startup_assets < asset_threshold:
            return set_summary(
                credit_rationed=False,
                development_outcome=False,
                early_bidding_type=FMT20.Takeover.Pooling,
                early_takeover=False,
                set_policy=merger_policy,
            )
        return set_summary(set_policy=merger_policy, credit_rationed=credit_constrained)

    model: FMT20.OptimalMergerPolicy = mock.Mock(spec=FMT20.OptimalMergerPolicy)
    type(model).merger_policy = policy
    type(model).startup_assets = 3.5
    type(model).private_benefit = 0.18
    type(model).development_costs = 1.5
    type(model).success_probability = 0.38
    type(model).tolerated_harm = 0.48
    type(model).cs_duopoly = 0.58
    type(model).incumbent_profit_duopoly = 0.68
    type(model).startup_profit_duopoly = 0.78
    type(model).w_duopoly = (
        model.incumbent_profit_duopoly + model.startup_profit_duopoly + model.cs_duopoly
    )
    type(model).cs_without_innovation = 0.88
    type(model).incumbent_profit_without_innovation = 0.98
    type(model).w_without_innovation = (
        model.incumbent_profit_without_innovation + model.cs_without_innovation
    )
    type(model).cs_with_innovation = 1.08
    type(model).incumbent_profit_with_innovation = 1.18
    type(model).w_with_innovation = (
        model.incumbent_profit_with_innovation + model.cs_with_innovation
    )

    type(model).asset_threshold = mock.PropertyMock(return_value=asset_threshold)
    type(model).asset_threshold_late_takeover = mock.PropertyMock(
        return_value=asset_threshold_late_takeover
    )
    type(model).asset_distribution_threshold_profitable_without_late_takeover = 0.4
    type(model).asset_distribution_threshold_welfare = 0.6
    type(model).asset_threshold_late_takeover_cdf = 0.7
    type(model).asset_distribution_threshold_with_late_takeover = 0.8
    type(model).asset_threshold_cdf = 0.9
    type(model).asset_distribution_threshold_unprofitable_without_late_takeover = 1
    type(model).asset_distribution_threshold_shelving_approved = 0.91
    type(model).early_bidding_type = FMT20.Takeover.Separating
    type(model).late_bidding_type = FMT20.Takeover.Pooling
    model.asset_distribution = FMT20.Distributions.NormalDistribution
    model.asset_distribution_kwargs = {}

    set_outcome(model, **kwargs)

    model.get_optimal_merger_policy = (
        lambda: FMT20.MergerPolicies.Intermediate_late_takeover_prohibited
    )
    model.summary = lambda: summary(merger_policy=model.merger_policy)
    return model


def mock_parameter_model_generator(
    strict_optimal=False,
    intermediate_optimal=False,
    laissez_faire_optimal=False,
    killer_acquisition=False,
    invalid_parameter_model=False,
    callable_condition=False,
    two_conditions=False,
) -> FMT20.ParameterModelGenerator:
    """
    Creates a mock model of Fumagalli_Motta_Tarantino_2020.Configurations.FindConfig.ParameterModelGenerator.
    """
    generator: FMT20.ParameterModelGenerator = mock.Mock(
        spec=FMT20.ParameterModelGenerator
    )
    config10 = FMT20.LoadParameters(10)
    config11 = FMT20.LoadParameters(11)
    config15 = FMT20.LoadParameters(15)
    config16 = FMT20.LoadParameters(16)
    if strict_optimal:
        when(generator).get_parameter_model().thenReturn(config15).thenReturn(config10)
    elif intermediate_optimal:
        when(generator).get_parameter_model().thenReturn(config10).thenReturn(config15)
    elif laissez_faire_optimal or callable_condition:
        when(generator).get_parameter_model().thenReturn(config10).thenReturn(config16)
    elif two_conditions and killer_acquisition:
        config10.set_merger_policy(FMT20.MergerPolicies.Laissez_faire)
        config11.set_merger_policy(FMT20.MergerPolicies.Laissez_faire)
        config15.set_merger_policy(FMT20.MergerPolicies.Laissez_faire)
        when(generator).get_parameter_model(
            merger_policy=FMT20.MergerPolicies.Laissez_faire
        ).thenReturn(config11).thenReturn(config10).thenReturn(config15)
    elif two_conditions:
        when(generator).get_parameter_model().thenReturn(config10).thenReturn(config16)
    elif killer_acquisition:
        config10.set_merger_policy(FMT20.MergerPolicies.Laissez_faire)
        when(generator).get_parameter_model(
            merger_policy=FMT20.MergerPolicies.Laissez_faire
        ).thenReturn(config11).thenReturn(config10)
    elif invalid_parameter_model:
        config16.adjust_parameters(development_costs=10)
        when(generator).get_parameter_model().thenReturn(config16).thenReturn(config15)
    return generator
