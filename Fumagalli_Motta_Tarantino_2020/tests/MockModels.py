import unittest.mock as mock

import Fumagalli_Motta_Tarantino_2020.Types as Types
import Fumagalli_Motta_Tarantino_2020.Models as Models


def mock_optimal_merger_policy(
    asset_threshold: float = 3,
    asset_threshold_late_takeover: float = 1,
    takeover: bool = False,
    shelving: bool = False,
    successful: bool = True,
    policy: Types.MergerPolicies = Types.MergerPolicies.Intermediate_late_takeover_prohibited,
) -> Models.OptimalMergerPolicy:
    def set_summary(
        credit_rationed=False,
        early_bidding_type=Types.Takeover.No,
        late_bidding_type=Types.Takeover.No,
        development_attempt=shelving,
        development_outcome=successful,
        early_takeover=False,
        late_takeover=False,
        policy=policy,
    ) -> Types.OptimalMergerPolicySummary:
        if takeover:
            early_bidding_type = Types.Takeover.Separating
            early_takeover = True

        return Types.OptimalMergerPolicySummary(
            credit_rationed=credit_rationed,
            set_policy=policy,
            early_bidding_type=early_bidding_type,
            late_bidding_type=late_bidding_type,
            development_attempt=development_attempt,
            development_outcome=development_outcome,
            early_takeover=early_takeover,
            late_takeover=late_takeover,
            optimal_policy=policy,
        )

    def summary():
        if model.startup_assets < 1:
            return set_summary(credit_rationed=True, development_outcome=False)
        if model.startup_assets < 3:
            return set_summary(development_outcome=False)
        return set_summary()

    model: Models.OptimalMergerPolicy = mock.Mock(spec=Models.OptimalMergerPolicy)
    type(model).startup_assets = 3.5
    type(model).private_benefit = 0.18
    type(model).development_costs = 0.28
    type(model).success_probability = 0.38
    type(model).tolerated_harm = 0.48
    type(model).cs_duopoly = 0.58
    type(model).incumbent_profit_duopoly = 0.68
    type(model).startup_profit_duopoly = 0.78
    type(model).cs_without_innovation = 0.88
    type(model).incumbent_profit_without_innovation = 0.98
    type(model).cs_with_innovation = 1.08
    type(model).incumbent_profit_with_innovation = 1.18
    type(model).asset_threshold = mock.PropertyMock(return_value=asset_threshold)
    type(model).asset_threshold_late_takeover = mock.PropertyMock(
        return_value=asset_threshold_late_takeover
    )
    model.summary = summary
    return model