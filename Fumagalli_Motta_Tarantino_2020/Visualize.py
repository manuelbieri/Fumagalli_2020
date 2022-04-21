from typing import List
from abc import abstractmethod
import math
import numpy as np
import datetime
import matplotlib.pyplot as plt

import Fumagalli_Motta_Tarantino_2020.Models as Models
import Fumagalli_Motta_Tarantino_2020.Types as Types


class IVisualize:
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


class AssetRange(IVisualize):
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
            Types.ThresholdItem("$\\bar{A}$", self.model.asset_threshold),
            Types.ThresholdItem(
                "$\\bar{A}^T$", self.model.asset_threshold_late_takeover
            ),
            Types.ThresholdItem("K", self.model.development_costs),
        ]
        for threshold in thresholds:
            if threshold.value <= 0:
                thresholds.remove(threshold)
        thresholds = sorted(thresholds, key=lambda x: x.value)
        thresholds.insert(0, Types.ThresholdItem("0", 0))
        return thresholds

    @staticmethod
    def _get_is_takeover_legend(bid_attempt: Types.Takeover, is_takeover: bool) -> str:
        if bid_attempt is Types.Takeover.No:
            return ""
        return "$(\\checkmark)$" if is_takeover else "$(\\times)$"

    @staticmethod
    def _get_development_attempt_legend(is_developing: bool) -> str:
        return "$D$" if is_developing else "$\\emptyset$"

    @staticmethod
    def _get_development_outcome_legend(
        is_developing: bool, is_successful: bool
    ) -> str:
        if is_developing:
            return "$(\\checkmark)$" if is_successful else "$(\\times)$"
        return ""

    @staticmethod
    def _get_symbol_legend():
        return (
            "${\\bf Merger\\thickspace policies}$:\n"
            f"{Types.MergerPolicies.legend()}\n"
            "${\\bf Bidding\\thickspace types}$:\n"
            f"{Types.Takeover.legend()}\n"
            "${\\bf Takeover\\thickspace outcome\\thickspace}$:\n"
            f"{Types.Takeover.Pooling.abbreviation()}|{Types.Takeover.Separating.abbreviation()}$(\\checkmark)$: Takeover is approved by the startup and AA\n"
            f"{Types.Takeover.Pooling.abbreviation()}|{Types.Takeover.Separating.abbreviation()}$(\\times)$: Takeover is blocked  by AA or not accepted by the startup\n"
            "${\\bf Development\\thickspace outcome}$:\n"
            f"$\\emptyset$: Product development was shelved\n"
            f"$D(\\checkmark)$: Product development was attempted and successful\n"
            f"$D(\\times)$: Product development was attempted and not successful\n"
        )

    @staticmethod
    def _get_summary_latex(summary: Types.OptimalMergerPolicySummary) -> str:
        separator: str = "$\\to$"
        return (
            f"{summary.set_policy.abbreviation()}: "
            f"{summary.early_bidding_type.abbreviation()}"
            f"{AssetRange._get_is_takeover_legend(summary.early_bidding_type, summary.early_takeover)}{separator}"
            f"{AssetRange._get_development_attempt_legend(summary.development_attempt)}"
            f"{AssetRange._get_development_outcome_legend(summary.development_attempt, summary.development_outcome)}{separator}"
            f"{summary.late_bidding_type.abbreviation()}"
            f"{AssetRange._get_is_takeover_legend(summary.late_bidding_type, summary.late_takeover)}"
        )

    @staticmethod
    def _get_x_labels_ticks(
        asset_thresholds: List[Types.ThresholdItem],
    ) -> (List[float], List[str]):
        x_ticks: List[float] = []
        x_labels: List[str] = []
        for threshold in asset_thresholds:
            x_ticks.append(threshold.value)
            x_labels.append(threshold.name)
        return x_ticks, x_labels

    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        asset_range, summaries = self.get_outcomes_asset_range()
        assert asset_range is not None
        assert summaries is not None
        for i, summary in enumerate(summaries):
            length: float = asset_range[i + 1].value - asset_range[i].value
            self.ax.barh(
                y=0.1,
                width=length,
                left=asset_range[i].value,
                height=0.2,
                label=self._get_summary_latex(summary),
            )
        self.ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0)
        self.ax.annotate(
            self._get_symbol_legend(),
            xy=(asset_range[0].value, 0),
            xytext=(0, -35),
            textcoords="offset points",
            horizontalalignment="left",
            verticalalignment="top",
        )
        self.ax.margins(y=0.2, x=0)
        x_ticks, x_labels = self._get_x_labels_ticks(asset_range)
        self.ax.set_xticks(x_ticks)
        self.ax.set_xticklabels(x_labels)
        self.fig.tight_layout()
        # self._legend_delete_duplicate_labels() # avoid duplication in legend
        return self.fig, self.ax


class Timeline(IVisualize):
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
