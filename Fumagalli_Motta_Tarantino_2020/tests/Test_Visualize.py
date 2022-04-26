from typing import Literal
import unittest
import matplotlib.pyplot as plt

import Fumagalli_Motta_Tarantino_2020.tests.MockModels as MockModels

import Fumagalli_Motta_Tarantino_2020.Types as Types
import Fumagalli_Motta_Tarantino_2020.Models as Models
import Fumagalli_Motta_Tarantino_2020.Visualize as Visualize


class TestVisualize(unittest.TestCase):
    show_plots:bool = True

    def setUpMock(self, **kwargs) -> None:
        self.mock: Models.OptimalMergerPolicy = MockModels.mock_optimal_merger_policy(
            **kwargs
        )

    def setUpVisualizer(
        self,
        model: Models.OptimalMergerPolicy,
        plot_type: Literal["Outcome", "Timeline"] = "Outcome",
    ) -> None:
        if plot_type == "Timeline":
            self.visualizer: Visualize.IVisualize = Visualize.Timeline(model)
        else:
            self.visualizer: Visualize.IVisualize = Visualize.AssetRange(model)

    @staticmethod
    def view_plot(fig: plt.Figure, show: bool=False) -> None:
        if show:
            fig.show()


    def test_plot_interface(self):
        self.setUpMock()
        self.assertRaises(NotImplementedError, Visualize.IVisualize(self.mock).plot)

    def test_essential_asset_thresholds(self):
        self.setUpMock(asset_threshold=2, asset_threshold_late_takeover=1)
        self.visualizer: Visualize.AssetRange = Visualize.AssetRange(self.mock)
        thresholds = self.visualizer._get_asset_thresholds()
        self.assertEqual(6, len(thresholds))
        self.assertEqual("0.5", thresholds[0].name)
        self.assertEqual("$F(K)$", thresholds[-1].name)

    def test_essential_asset_thresholds_negative_values(self):
        self.setUpMock()
        self.visualizer: Visualize.AssetRange = Visualize.AssetRange(self.mock)
        thresholds = self.visualizer._get_asset_thresholds()
        self.assertEqual(6, len(thresholds))
        self.assertEqual(thresholds[0].value, 0.5)
        self.assertEqual(thresholds[-1].name, "$F(K)$")

    def test_outcomes_asset_range(self):
        self.setUpMock(
            asset_threshold=1.2815515655446004,
            asset_threshold_late_takeover=0.5244005127080407,
        )
        self.visualizer: Visualize.AssetRange = Visualize.AssetRange(self.mock)
        thresholds, outcomes = self.visualizer._get_outcomes_asset_range()
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

    def test_outcome_plot_negative_threshold(self):
        self.setUpMock()
        self.setUpVisualizer(self.mock)
        self.view_plot(self.visualizer.plot()[0], show=TestVisualize.show_plots)

    def test_outcome_plot(self):
        self.setUpMock(asset_threshold=3, asset_threshold_late_takeover=1)
        self.setUpVisualizer(self.mock)
        self.view_plot(self.visualizer.plot()[0], show=TestVisualize.show_plots)

    def test_timeline_plot(self):
        self.setUpMock(policy=Types.MergerPolicies.Laissez_faire)
        self.setUpVisualizer(self.mock, plot_type="Timeline")
        self.view_plot(self.visualizer.plot()[0], show=TestVisualize.show_plots)

    def test_timeline_plot_takeover_shelving(self):
        self.setUpMock(takeover=True, shelving=True, successful=False)
        self.setUpVisualizer(self.mock, plot_type="Timeline")
        self.view_plot(self.visualizer.plot()[0], show=TestVisualize.show_plots)
