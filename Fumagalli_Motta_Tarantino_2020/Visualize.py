from typing import List
from abc import abstractmethod
import math
import numpy as np
import datetime
import matplotlib.pyplot as plt

import Fumagalli_Motta_Tarantino_2020.Models as Models
import Fumagalli_Motta_Tarantino_2020.Types as Types


class VisualizeInterface:
    @abstractmethod
    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        raise NotImplementedError

    @staticmethod
    def _parameter_latex(model: Models.BaseModel) -> str:
        separator_name_value = "="
        separator_parameters = " | "
        output_str = ""
        for (parameter, value, separator) in [
            ("A", model.startup_assets, separator_parameters),
            ("B", model.private_benefit, separator_parameters),
            ("K", model.development_costs, separator_parameters),
            ("\\bar{H}", model.tolerated_harm, separator_parameters),
            ("p", model.success_probability, "\n"),
            ("CS^m", model.cs_without_innovation, separator_parameters),
            (
                "\\pi^m_I",
                model.incumbent_profit_without_innovation,
                separator_parameters,
            ),
            ("CS^M", model.cs_with_innovation, separator_parameters),
            ("\\pi^M_I", model.incumbent_profit_with_innovation, separator_parameters),
            ("CS^d", model.cs_duopoly, separator_parameters),
            ("\\pi^d_I", model.incumbent_profit_duopoly, separator_parameters),
            ("\\pi^d_S", model.startup_profit_duopoly, ""),
        ]:
            output_str += f"${parameter}{separator_name_value}{value}${separator}"
        return output_str


class Outcome(VisualizeInterface):
    def __init__(self, model: Models.OptimalMergerPolicy):
        self.model = model
        self.fig, self.ax = plt.subplots()

    def get_outcomes_asset_range(
        self,
    ) -> (List[Types.ThresholdItem], List[Types.OptimalMergerPolicySummary]):
        asset_range: List[Types.ThresholdItem] = self.get_asset_thresholds()
        summaries: List[Types.OptimalMergerPolicySummary] = []
        for i in range(len(asset_range) - 1):
            self.model.startup_assets = (
                asset_range[i].value + asset_range[i + 1].value
            ) / 2
            summaries.append(self.model.summary())
        return asset_range, summaries

    def get_asset_thresholds(self) -> List[Types.ThresholdItem]:
        thresholds: List[Types.ThresholdItem] = [
            Types.ThresholdItem("F(\\bar{A})", self.model.asset_threshold),
            Types.ThresholdItem(
                "F(\\bar{A}^T)", self.model.asset_threshold_late_takeover
            ),
        ]
        essential_thresholds = [Types.ThresholdItem("start", 0)]
        for threshold in thresholds:
            if threshold.value > 0:
                essential_thresholds.append(threshold)
        essential_thresholds = sorted(essential_thresholds, key=lambda x: x.value)
        essential_thresholds.append(
            Types.ThresholdItem("end", self._get_max_asset_range(essential_thresholds))
        )
        return essential_thresholds

    @staticmethod
    def _get_max_asset_range(d: List[Types.ThresholdItem]) -> float:
        return math.floor(max(i.value for i in d) + 1)

    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        asset_range, summaries = self.get_outcomes_asset_range()
        assert asset_range is not None
        assert summaries is not None
        for i in range(len(summaries)):
            length: float = asset_range[i + 1].value - asset_range[i].value
            self.ax.barh(y=1, width=length, left=asset_range[i].value, height=0.4)
        return self.fig, self.ax


class Timeline(VisualizeInterface):
    def __init__(self, model: Models.OptimalMergerPolicy):
        self.model = model
        self.fig, self.ax = plt.subplots()

    def _prepare_content(self) -> (list, List[datetime.date]):
        summary: Types.OptimalMergerPolicySummary = self.model.summary()
        values = [
            "AA establishes "
            + self._policy_str(summary.set_policy)
            + "\nmerger policy",
            self._bid_attempt_str(summary.early_bidding_type),
            self._takeover_str(summary.early_takeover),
            self._development_str(summary.development_attempt, summary.early_takeover),
            self._success_str(summary.development_outcome),
            self._bid_attempt_str(summary.late_bidding_type),
            self._takeover_str(summary.late_takeover),
            "Payoffs",
        ]
        x_labels = ["t=0", "t=1a", "t=1b", "t=1c", "t=1d", "t=2a", "t=2b", "t=3"]

        return values, x_labels

    @staticmethod
    def _bid_attempt_str(bid_attempt: Types.Takeover) -> str:
        return str(bid_attempt) + "\nby incumbent"

    @staticmethod
    def _policy_str(policy: Types.MergerPolicies) -> str:
        policy_str = str(policy).lower()
        if "intermediate" in policy_str:
            return policy_str.replace("intermediate", "intermediate\n")
        return policy_str

    @staticmethod
    def _takeover_str(is_takeover: bool) -> str:
        if is_takeover:
            return "Takeover\napproved"
        return "No takeover\noccurs"

    @staticmethod
    def _development_str(is_development: bool, is_early_takeover: bool) -> str:
        owner = "Incumbent" if is_early_takeover else "Start-up"
        is_killer_acquisition = "\n(killer acquisition)" if is_early_takeover else ""
        if is_development:
            return f"{owner}\ndevelops product"
        return f"{owner}\nshelves product{is_killer_acquisition}"

    @staticmethod
    def _success_str(is_successful: bool) -> str:
        if is_successful:
            return "Development is\nsuccessful"
        return "Development is\nnot successful"

    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        values, x_labels = self._prepare_content()
        x_ticks = range(len(x_labels))

        # height of lines from points in time
        # levels = np.tile([1, -1], int(np.ceil(len(x_ticks) / 2)))[: len(x_ticks)]
        levels = [-1, 1, 0.6, -1, 1, -1, -0.6, 1]

        # Create figure and plot a stem plot with the date
        self.ax.set(title="Timeline")
        self.ax.annotate(
            self._parameter_latex(self.model),
            xy=(math.fsum(x_ticks) / len(x_ticks), 1.9),
            horizontalalignment="center",
            verticalalignment="top",
            fontsize="x-small",
        )

        self.ax.vlines(
            x_ticks, 0, levels, color="lightgray", linewidths=1
        )  # The vertical stems.
        self.ax.plot(
            x_ticks, np.zeros_like(x_ticks), "-o", color="k", markerfacecolor="w"
        )  # Baseline and markers on it.

        # annotate lines
        for d, l, r in zip(x_ticks, levels, values):
            self.ax.annotate(
                str(r),
                xy=(d, l),
                xytext=(0, np.sign(l) * 8),
                textcoords="offset points",
                horizontalalignment="center",
                verticalalignment="bottom" if l > 0 else "top",
            )

        # set x-axis
        self.ax.set_xticks(x_ticks)
        self.ax.set_xticklabels(x_labels)

        # remove y-axis and spines
        self.ax.yaxis.set_visible(False)
        self.ax.spines[["left", "top", "right"]].set_visible(False)

        self.ax.margins(y=0.45)
        return self.fig, self.ax
