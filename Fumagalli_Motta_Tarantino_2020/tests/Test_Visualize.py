from typing import Literal
import unittest

import Fumagalli_Motta_Tarantino_2020.tests.MockModels as MockModels
import Fumagalli_Motta_Tarantino_2020 as FMT20


class TestVisualize(unittest.TestCase):
    show_plots: bool = False
    show_always: bool = True

    def setUpMock(self, **kwargs) -> None:
        self.mock: FMT20.OptimalMergerPolicy = MockModels.mock_optimal_merger_policy(
            **kwargs
        )

    def setUpVisualizer(
        self,
        model: FMT20.OptimalMergerPolicy,
        plot_type: Literal[
            "Outcome", "Timeline", "MergerPolicies", "Payoff", "Overview"
        ] = "Outcome",
        **kwargs
    ) -> None:
        if plot_type == "Timeline":
            self.visualizer: FMT20.IVisualize = FMT20.Timeline(model, **kwargs)
        elif plot_type == "MergerPolicies":
            self.visualizer: FMT20.IVisualize = FMT20.MergerPoliciesAssetRange(
                model, **kwargs
            )
        elif plot_type == "Payoff":
            self.visualizer: FMT20.IVisualize = FMT20.Payoffs(model, **kwargs)
        elif plot_type == "Overview":
            self.visualizer: FMT20.IVisualize = FMT20.Overview(model, **kwargs)
        else:
            self.visualizer: FMT20.IVisualize = FMT20.AssetRange(model, **kwargs)

    def view_plot(self, show: bool = False) -> None:
        if show:
            self.visualizer.show()
        else:
            self.visualizer.plot()

    def test_plot_interface(self):
        self.setUpMock()
        self.assertRaises(NotImplementedError, FMT20.IVisualize(self.mock).plot)

    def test_essential_asset_thresholds(self):
        self.setUpMock(asset_threshold=2, asset_threshold_late_takeover=1)
        self.visualizer: FMT20.AssetRange = FMT20.AssetRange(self.mock)
        thresholds = self.visualizer._get_asset_thresholds()
        self.assertEqual(6, len(thresholds))
        self.assertEqual("0.5", thresholds[0].name)
        self.assertEqual("$F(K)$", thresholds[-1].name)

    def test_essential_asset_thresholds_negative_values(self):
        self.setUpMock()
        self.visualizer: FMT20.AssetRange = FMT20.AssetRange(self.mock)
        thresholds = self.visualizer._get_asset_thresholds()
        self.assertEqual(6, len(thresholds))
        self.assertEqual(thresholds[0].value, 0.5)
        self.assertEqual(thresholds[-1].name, "$F(K)$")

    def test_outcomes_asset_range(self):
        self.setUpMock(
            asset_threshold=1.2815515655446004,
            asset_threshold_late_takeover=0.5244005127080407,
        )
        self.visualizer: FMT20.AssetRange = FMT20.AssetRange(self.mock)
        outcomes = self.visualizer._get_outcomes_asset_range()
        self.assertEqual(5, len(outcomes))
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
        self.setUpVisualizer(self.mock)
        self.view_plot(show=TestVisualize.show_plots)

    def test_asset_range_plot(self):
        self.setUpMock(asset_threshold=3, asset_threshold_late_takeover=1)
        self.setUpVisualizer(self.mock)
        self.view_plot(show=TestVisualize.show_plots)

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
        self.setUpVisualizer(self.mock, plot_type="MergerPolicies")
        self.view_plot(show=TestVisualize.show_plots)

    def test_timeline_plot(self):
        self.setUpMock(policy=FMT20.MergerPolicies.Laissez_faire)
        self.setUpVisualizer(self.mock, plot_type="Timeline")
        self.view_plot(show=TestVisualize.show_plots)

    def test_timeline_plot_takeover_shelving(self):
        self.setUpMock(takeover=True, shelving=True, successful=False)
        self.setUpVisualizer(self.mock, plot_type="Timeline")
        self.view_plot(show=TestVisualize.show_plots)

    def test_timeline_plot_takeover_shelving_credit_constraint(self):
        FMT20.IVisualize.set_dark_mode()
        self.setUpMock(
            takeover=True, shelving=True, successful=False, credit_constrained=True
        )
        self.setUpVisualizer(self.mock, plot_type="Timeline")
        self.view_plot(show=TestVisualize.show_plots)

    def test_payoff_plot(self):
        self.setUpMock()
        self.setUpVisualizer(self.mock, plot_type="Payoff", dark_mode=True)
        self.view_plot(show=TestVisualize.show_plots)

    def test_overview_plot(self):
        self.setUpMock()
        self.setUpVisualizer(self.mock, plot_type="Overview", default_style=False)
        self.view_plot(show=(TestVisualize.show_plots or TestVisualize.show_always))
