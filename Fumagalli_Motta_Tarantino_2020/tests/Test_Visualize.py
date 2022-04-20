from typing import Literal
import unittest
import MockModels

import Fumagalli_Motta_Tarantino_2020.Types as Types
import Fumagalli_Motta_Tarantino_2020.Models as Models
import Fumagalli_Motta_Tarantino_2020.Visualize as Visualize


class TestPlotOptimalMergerPolicy(unittest.TestCase):
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
            self.visualizer: Visualize.VisualizeInterface = Visualize.Timeline(model)
        else:
            self.visualizer: Visualize.VisualizeInterface = Visualize.Outcome(model)

    def test_plot_interface(self):
        self.assertRaises(NotImplementedError, Visualize.VisualizeInterface().plot)

    def test_essential_asset_thresholds(self):
        self.setUpMock()
        self.visualizer: Visualize.Outcome = Visualize.Outcome(self.mock)
        thresholds = self.visualizer.get_asset_thresholds()
        self.assertEqual(4, len(thresholds))
        self.assertEqual(thresholds[0].name, "start")
        self.assertEqual(thresholds[1].value, 1)
        self.assertEqual(thresholds[2].value, 3)
        self.assertEqual(thresholds[3].name, "end")

    def test_essential_asset_thresholds_negative_values(self):
        self.setUpMock(asset_threshold_late_takeover=-1)
        self.visualizer: Visualize.Outcome = Visualize.Outcome(self.mock)
        thresholds = self.visualizer.get_asset_thresholds()
        self.assertEqual(3, len(thresholds))
        self.assertEqual(thresholds[0].value, 0)
        self.assertEqual(thresholds[1].value, 3)
        self.assertEqual(thresholds[2].value, 4)

    def test_outcomes_asset_range(self):
        self.setUpMock()
        self.visualizer: Visualize.Outcome = Visualize.Outcome(self.mock)
        thresholds, outcomes = self.visualizer.get_outcomes_asset_range()
        self.assertEqual(3, len(outcomes))
        self.assertTrue(outcomes[0].credit_rationed)
        self.assertFalse(outcomes[0].development_outcome)
        self.assertFalse(outcomes[1].credit_rationed)
        self.assertFalse(outcomes[1].development_outcome)
        self.assertFalse(outcomes[2].credit_rationed)
        self.assertTrue(outcomes[2].development_outcome)

    def test_outcome_plot(self):
        self.setUpMock()
        self.setUpVisualizer(self.mock)
        self.visualizer.plot()[0].show()

    def test_timeline_plot(self):
        self.setUpMock(policy=Types.MergerPolicies.Laissez_faire)
        self.setUpVisualizer(self.mock, plot_type="Timeline")
        self.visualizer.plot()[0].show()

    def test_timeline_plot_takeover_shelving(self):
        self.setUpMock(takeover=True, shelving=True, successful=False)
        self.setUpVisualizer(self.mock, plot_type="Timeline")
        self.visualizer.plot()[0].show()
