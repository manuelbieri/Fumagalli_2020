from abc import abstractmethod

import math
import numpy as np
import datetime
import matplotlib.pyplot as plt

import Fumagalli_Motta_Tarantino_2020.Models as Models
import Fumagalli_Motta_Tarantino_2020.Types as Types
import Fumagalli_Motta_Tarantino_2020.Utilities as Utilities


class IVisualize:
    """
    Interface for all visualization classes containing useful methods.
    """

    colors: list[str] = [
        "salmon",
        "khaki",
        "limegreen",
        "turquoise",
        "powderblue",
        "thistle",
        "pink",
    ]
    """Standard colors used in visualizations."""

    def __init__(self, model: Models.OptimalMergerPolicy):
        """
        Parameters
        ----------
        model: Fumagalli_Motta_Tarantino_2020.Models.OptimalMergerPolicy
            Model to plot the outcomes on asset range from.
        """
        self.model: Models.OptimalMergerPolicy = model
        self.fig, self.ax = plt.subplots()

    @abstractmethod
    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        """
        Plots the visual representation for the object.

        Parameters
        ----------
        kwargs
            Options for the plots for further customization.

        Returns
        -------
        Figure
            Containing the axes with the plots (use Figure.show() to display).
        Axes
            Containing the plots (arrange custom summary).
        """
        raise NotImplementedError

    @staticmethod
    def _parameter_latex(model: Models.BaseModel) -> str:
        """
        Generates a legend for the parameter values of a Fumagalli_Motta_Tarantino_2020.Models.BaseModel in latex format.

        Parameters
        ----------
        model: Fumagalli_Motta_Tarantino_2020.Models.BaseModel
            Input model to generate the legend from.

        Returns
        -------
        str
            Containing the legend for the parameter values.
        """
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
    """
    Visualizes the outcomes over an assets range for a specific model.
    """

    def __init__(self, model: Models.OptimalMergerPolicy) -> None:
        super(AssetRange, self).__init__(model)
        self.labels: list[str] = []
        self.colors: dict[str, str] = {}

    def _get_outcomes_asset_range(
        self,
    ) -> (list[Types.ThresholdItem], list[Types.OptimalMergerPolicySummary]):
        """
        Generates a list with all essential threshold concerning the assets of a start-up and an additional list with
        summaries of the outcomes of the model in between the thresholds.

        Returns
        -------
        (list[Fumagalli_Motta_Tarantino_2020.Types.ThresholdItem], list[Fumagalli_Motta_Tarantino_2020.Types.OptimalMergerPolicySummary])
            List containing the essential asset thresholds in the model and list containing the summaries of the outcomes of the model.

        """
        asset_range: list[Types.ThresholdItem] = self._get_asset_thresholds()
        summaries: list[Types.OptimalMergerPolicySummary] = []
        for i in range(len(asset_range) - 1):
            self.model.startup_assets = (
                Utilities.NormalDistributionFunction.inverse_cumulative(
                    asset_range[i].value
                )
                + Utilities.NormalDistributionFunction.inverse_cumulative(
                    asset_range[i + 1].value
                )
            ) / 2
            summaries.append(self.model.summary())
        return asset_range, summaries

    def _get_asset_thresholds(self) -> list[Types.ThresholdItem]:
        """
        Generates a list with all essential threshold concerning the assets of a start-up.

        Returns
        -------
        list[Fumagalli_Motta_Tarantino_2020.Types.ThresholdItem]
            List containing the essential asset thresholds in the model.
        """
        min_threshold = Types.ThresholdItem("0.5", 0.5)
        max_threshold = Types.ThresholdItem(
            "$F(K)$",
            Utilities.NormalDistributionFunction.cumulative(
                self.model.development_costs
            ),
        )
        thresholds: list[Types.ThresholdItem] = [
            Types.ThresholdItem(
                "$\\Gamma$", self.model.asset_distribution_threshold_strict
            ),
            Types.ThresholdItem("$\\Phi$", self.model.asset_distribution_threshold),
            Types.ThresholdItem(
                "$\\Phi^T$", self.model.asset_distribution_threshold_laissez_faire
            ),
            Types.ThresholdItem(
                "$\\Phi^{\\prime}$",
                self.model.asset_distribution_threshold_intermediate,
            ),
            Types.ThresholdItem("$F(\\bar{A})$", self.model.asset_threshold_cdf),
            Types.ThresholdItem(
                "$F(\\bar{A}^T)$", self.model.asset_threshold_late_takeover_cdf
            ),
        ]
        essential_thresholds: list[Types.ThresholdItem] = []
        for threshold in thresholds:
            if min_threshold.value < threshold.value < max_threshold.value:
                essential_thresholds.append(threshold)
        thresholds = sorted(essential_thresholds, key=lambda x: x.value)
        thresholds.insert(0, min_threshold)
        thresholds.append(max_threshold)
        return thresholds

    @staticmethod
    def _get_is_takeover_legend(bid_attempt: Types.Takeover, is_takeover: bool) -> str:
        """
        Generates a string representation for legend about the takeover (option and approval).

        Parameters
        ----------
        bid_attempt: Fumagalli_Motta_Tarantino_2020.Types.Takeover
            Option for takeover chosen by the incumbent.
        is_takeover: bool
            If true, the takeover is approved by AA and the start-up.

        Returns
        -------
        str
            String representation for legend about takeover (option and approval).
        """
        if bid_attempt is Types.Takeover.No:
            return ""
        return "$(\\checkmark)$" if is_takeover else "$(\\times)$"

    @staticmethod
    def _get_development_attempt_legend(is_developing: bool) -> str:
        """
        Generates a string representation for legend about the development attempt.

        Parameters
        ----------
        is_developing: bool
            True, if the owner is developing the product (otherwise, the product is shelved).

        Returns
        -------
        str
            String representation for legend about the development attempt.
        """
        return "$D$" if is_developing else "$\\emptyset$"

    @staticmethod
    def _get_development_outcome_legend(
        is_developing: bool, is_successful: bool
    ) -> str:
        """
        Generates a string representation for legend about the development outcome.

        Parameters
        ----------
        is_developing: bool
            True, if the owner is developing the product (otherwise, the product is shelved).
        is_successful: bool
            True, if the development of the product is successful.

        Returns
        -------
        str
            String representation for legend about the development outcome.
        """
        if is_developing:
            return "$(\\checkmark)$" if is_successful else "$(\\times)$"
        return ""

    @staticmethod
    def _get_symbol_legend() -> str:
        """
        Generates a legend for the used abbreviations in the plot legends.

        Returns
        -------
        str
            Containing the legend for the used abbreviations.
        """
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
        """
        Generates a chronological entry for the legend based on the input model.

        Parameters
        ----------
        summary: Fumagalli_Motta_Tarantino_2020.Types.OptimalMergerPolicySummary
            Summary of the model.

        Returns
        -------
        str
            Chronological entry for the legend of the input model.
        """
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
        asset_thresholds: list[Types.ThresholdItem],
    ) -> (list[float], list[str]):
        """
        Generates the locations of the ticks on the x-axis and the corresponding labels on the x-axis.

        Parameters
        ----------
        asset_thresholds: list[Fumagalli_Motta_Tarantino_2020.Types.ThresholdItem]
            List with all threshold the assets.

        Returns
        -------
        (list[float], list[str])
            A list containing the ticks on the x-axis and a list containing the labels on the x-axis.
        """
        x_ticks: list[float] = []
        x_labels: list[str] = []
        for threshold in asset_thresholds:
            x_ticks.append(threshold.value)
            x_labels.append(threshold.name)
        return x_ticks, x_labels

    def _get_label_color(self, label) -> (str, str):
        """
        Returns the color and the final label for a legend entry.

        Through this method, duplications in the legend are avoided.

        Parameters
        ----------
        label: str

        Returns
        -------
        (str, str)
            String representing the final label and a string representing the color.
        """
        if label in self.labels:
            return "_nolegend_", self.colors[label]
        self.colors[label] = IVisualize.colors[len(self.labels)]
        self.labels.append(label)
        return label, self.colors[label]

    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        asset_range, summaries = self._get_outcomes_asset_range()
        assert asset_range is not None
        assert summaries is not None
        self.labels.clear()
        self.colors.clear()
        for threshold in asset_range:
            if 0 < threshold.value < self.model.development_costs:
                self.ax.axvline(threshold.value, linestyle="--", color="k")

        for i, summary in enumerate(summaries):
            length: float = asset_range[i + 1].value - asset_range[i].value
            label: str = self._get_summary_latex(summary)
            label, color = self._get_label_color(label)
            self.ax.barh(
                y=0.1,
                width=length,
                left=asset_range[i].value,
                height=0.2,
                color=color,
                label=label,
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
        self.ax.yaxis.set_visible(False)
        self.fig.tight_layout()
        # self._legend_delete_duplicate_labels() # avoid duplication in legend
        return self.fig, self.ax


class Timeline(IVisualize):
    """
    Visualizes the timeline of events for a specific model.
    """

    def __init__(self, model: Models.OptimalMergerPolicy):
        super(Timeline, self).__init__(model)

    def _prepare_content(self) -> (list[str], list[str]):
        """
        Generates the label and points in time of the events in the model.

        Returns
        -------
        (list, list[datetime.date])
            List containing label for the events and list containing the points in time of the events.
        """
        summary: Types.OptimalMergerPolicySummary = self.model.summary()
        values: list[str] = [
            "AA establishes "
            + self._policy_str(summary.set_policy)
            + "\nmerger policy",
            self._takeover_attempt_str(summary.early_bidding_type),
            self._takeover_str(summary.early_takeover),
            self._development_str(summary.development_attempt, summary.early_takeover),
            self._success_str(summary.development_outcome),
            self._takeover_attempt_str(summary.late_bidding_type),
            self._takeover_str(summary.late_takeover),
            "Payoffs",
        ]
        x_labels: list[str] = [
            "t=0",
            "t=1a",
            "t=1b",
            "t=1c",
            "t=1d",
            "t=2a",
            "t=2b",
            "t=3",
        ]
        return values, x_labels

    @staticmethod
    def _takeover_attempt_str(takeover: Types.Takeover) -> str:
        """
        Generate label for takeover event.

        Parameters
        ----------
        takeover: Fumagalli_Motta_Tarantino_2020.Types.Takeover
            Option for takeover chosen by the incumbent.

        Returns
        -------
        str
            Label for takeover event.
        """
        return str(takeover) + "\nby incumbent"

    @staticmethod
    def _policy_str(policy: Types.MergerPolicies) -> str:
        """
        Generate label for establishing of merger policy event.

        Parameters
        ----------
        policy: Fumagalli_Motta_Tarantino_2020.Types.MergerPolicies
            Policy established by the AA at beginning.

        Returns
        -------
        str
            Label for establishing of merger policy event.
        """
        policy_str = str(policy).lower()
        if "intermediate" in policy_str:
            return policy_str.replace("intermediate", "intermediate\n")
        return policy_str

    @staticmethod
    def _takeover_str(is_takeover: bool) -> str:
        """
        Generates a label about the takeover event (option and approval).

        Parameters
        ----------
        is_takeover: bool
            If true, the takeover is approved by AA and the start-up.

        Returns
        -------
        str
            Label about the takeover event (option and approval).
        """
        if is_takeover:
            return "Takeover\napproved"
        return "No takeover\noccurs"

    @staticmethod
    def _development_str(is_development: bool, is_early_takeover: bool) -> str:
        """
        Generates a label about the development event (attempt and shelving).

        Parameters
        ----------
        is_development: bool
            True, if the owner is developing the product (otherwise, the product is shelved).
        is_early_takeover: bool
            True, if an early takeover occurs.

        Returns
        -------
        str
            Label about the development event (attempt and shelving).
        """
        owner = "Incumbent" if is_early_takeover else "Start-up"
        is_killer_acquisition = "\n(killer acquisition)" if is_early_takeover else ""
        if is_development:
            return f"{owner}\ndevelops product"
        return f"{owner}\nshelves product{is_killer_acquisition}"

    @staticmethod
    def _success_str(is_successful: bool) -> str:
        """
        Generates a label about the development outcome event.

        Parameters
        ----------
        is_successful: bool
            True, if the development of the product is successful.

        Returns
        -------
        str
            Label about the development outcome event.
        """
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
