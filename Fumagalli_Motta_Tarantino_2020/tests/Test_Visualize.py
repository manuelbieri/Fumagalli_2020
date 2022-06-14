from typing import Callable
import unittest

import Fumagalli_Motta_Tarantino_2020.tests.MockModels as MockModels
import Fumagalli_Motta_Tarantino_2020 as FMT20


class TestVisualize(unittest.TestCase):
    show_all: bool = False

    def setUp(self) -> None:
        self.show_plot = None
        self.never_show_plot = None
        self.visualizer = None

    def setUpMock(self, **kwargs) -> None:
        self.mock: FMT20.OptimalMergerPolicy = MockModels.mock_optimal_merger_policy(
            **kwargs
        )

    def setUpVisualizerCall(
        self,
        plot_type: Callable,
        show_plot: bool = False,
        never_show_plot: bool = False,
        show_plot_now: bool = False,
        **kwargs
    ) -> None:
        self.visualizer: FMT20.IVisualize = plot_type()
        self.show_plot = show_plot
        self.never_show_plot = never_show_plot
        self.kwargs = kwargs
        if show_plot_now:
            self.show_figure()

    def tearDown(self) -> None:
        if self.visualizer is not None and self.show_plot is not None:
            self.show_figure()

    def show_figure(self) -> None:
        if (self.show_plot or TestVisualize.show_all) and not self.never_show_plot:
            self.visualizer.show(**self.kwargs)
        else:
            self.visualizer.plot(**self.kwargs)

    def test_plot_interface(self):
        self.setUpMock()
        self.assertRaises(NotImplementedError, FMT20.IVisualize(self.mock).plot)

    def test_essential_asset_thresholds(self):
        self.setUpMock(asset_threshold=2, asset_threshold_late_takeover=1)
        self.visualizer: FMT20.AssetRange = FMT20.AssetRange(self.mock)
        thresholds = self.visualizer._get_essential_thresholds()
        self.assertEqual(7, len(thresholds))
        self.assertEqual("$F(0)$", thresholds[0].name)
        self.assertEqual("$F(K)$", thresholds[-1].name)

    def test_essential_asset_thresholds_negative_values(self):
        self.setUpMock()
        self.visualizer: FMT20.AssetRange = FMT20.AssetRange(self.mock)
        thresholds = self.visualizer._get_essential_thresholds()
        self.assertEqual(7, len(thresholds))
        self.assertEqual(thresholds[0].value, 0.5)
        self.assertEqual(thresholds[-1].name, "$F(K)$")

    def test_outcomes_asset_range(self):
        self.setUpMock(
            asset_threshold=1.2815515655446004,
            asset_threshold_late_takeover=0.5244005127080407,
        )
        self.visualizer: FMT20.AssetRange = FMT20.AssetRange(self.mock)
        outcomes = self.visualizer._get_outcomes_asset_range()
        self.assertEqual(6, len(outcomes))
        self.assertTrue(outcomes[0].credit_rationed)
        self.assertFalse(outcomes[0].development_outcome)
        self.assertTrue(outcomes[1].credit_rationed)
        self.assertFalse(outcomes[1].development_outcome)
        self.assertFalse(outcomes[2].credit_rationed)
        self.assertFalse(outcomes[2].development_outcome)
        self.assertFalse(outcomes[3].credit_rationed)
        self.assertFalse(outcomes[3].development_outcome)
        self.assertFalse(outcomes[4].credit_rationed)
        self.assertTrue(outcomes[4].development_outcome)

    def test_asset_range_plot_negative_threshold(self):
        self.setUpMock()
        self.setUpVisualizerCall(lambda: FMT20.AssetRange(self.mock))

    def test_asset_range_plot(self):
        self.setUpMock(asset_threshold=3, asset_threshold_late_takeover=1)
        self.setUpVisualizerCall(lambda: FMT20.AssetRange(self.mock))

    def test_asset_range_set_model(self):
        self.setUpMock()
        mock2: FMT20.OptimalMergerPolicy = MockModels.mock_optimal_merger_policy()
        mock2.development_costs = 0.3
        self.visualizer: FMT20.AssetRange = FMT20.AssetRange(self.mock)
        self.assertEqual(7, len(self.visualizer._thresholds))
        self.visualizer.set_model(mock2)
        self.assertEqual(3, len(self.visualizer._thresholds))

    def test_outcomes_merger_policies(self):
        self.setUpMock(
            asset_threshold=1.2815515655446004,
            asset_threshold_late_takeover=0.5244005127080407,
        )
        self.visualizer: FMT20.MergerPoliciesAssetRange = (
            FMT20.MergerPoliciesAssetRange(self.mock)
        )
        outcomes = self.visualizer._get_outcomes_different_merger_policies()
        self.assertEqual(4, len(outcomes))
        self.assertEqual(FMT20.MergerPolicies.Strict, outcomes[0][0].set_policy)
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
            outcomes[1][0].set_policy,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            outcomes[2][0].set_policy,
        )
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, outcomes[3][0].set_policy)

    def test_merger_policies_plot(self):
        self.setUpMock(asset_threshold=3, asset_threshold_late_takeover=1)
        self.setUpVisualizerCall(
            lambda: FMT20.MergerPoliciesAssetRange(self.mock),
            thresholds=True,
            optimal_policy=True,
            y_offset=-25,
        )

    def test_timeline_plot(self):
        self.setUpMock(policy=FMT20.MergerPolicies.Laissez_faire)
        self.setUpVisualizerCall(lambda: FMT20.Timeline(self.mock))

    def test_timeline_plot_takeover_development_not_successful(self):
        self.setUpMock(set_outcome=True, is_owner_investing=True)
        self.setUpVisualizerCall(lambda: FMT20.Timeline(self.mock))

    def test_timeline_plot_takeover_shelving_credit_constraint(self):
        self.setUpMock(set_outcome=True, is_early_takeover=False)
        self.setUpVisualizerCall(lambda: FMT20.Timeline(self.mock))

    def test_timeline_set_model(self):
        mock1: FMT20.OptimalMergerPolicy = MockModels.mock_optimal_merger_policy()
        mock2: FMT20.OptimalMergerPolicy = MockModels.mock_optimal_merger_policy(
            policy=FMT20.MergerPolicies.Laissez_faire
        )
        self.setUpVisualizerCall(lambda: FMT20.Timeline(mock1), show_plot_now=True)
        self.visualizer.set_model(mock2)

    def test_payoff_plot(self):
        self.setUpMock()
        self.setUpVisualizerCall(lambda: FMT20.Payoffs(self.mock, dark_mode=True))

    def test_overview_plot(self):
        self.setUpMock()
        self.setUpVisualizerCall(
            lambda: FMT20.Overview(self.mock, default_style=False), show_plot=True
        )

    def test_perfect_information_asset_range(self):
        model = FMT20.PerfectInformation(**FMT20.LoadParameters(config_id=50)())
        self.setUpVisualizerCall(
            lambda: FMT20.MergerPoliciesAssetRangePerfectInformation(model),
            thresholds=True,
            optimal_policy=True,
            y_offset=-40,
        )

    def test_perfect_information_overview(self):
        model = FMT20.PerfectInformation(**FMT20.LoadParameters(config_id=51)())
        self.setUpVisualizerCall(lambda: FMT20.Overview(model))
