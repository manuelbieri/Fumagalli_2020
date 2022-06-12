from abc import abstractmethod
from typing import Optional, Callable
import warnings

import math

import matplotlib.gridspec
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator

import Fumagalli_Motta_Tarantino_2020 as FMT20


class IVisualize:
    """
    Interface for all visualization classes containing useful methods.

    Notes
    -----
    This module is compatible with python versions starting from 3.9, due to introduction of PEP 585. Therefore, the compatibility
    with mybinder.org is not guaranteed (uses at the moment python 3.7).
    """

    colors: list[str] = [
        "indianred",
        "salmon",
        "khaki",
        "greenyellow",
        "limegreen",
        "turquoise",
        "powderblue",
        "lavender",
        "thistle",
        "lavenderblush",
        "pink",
    ]
    """Standard colors used in visualizations."""
    fontsize = "x-small"
    """Default font size"""

    def __init__(
        self,
        model: FMT20.OptimalMergerPolicy,
        ax: Optional[plt.Axes] = None,
        default_style=True,
        dark_mode=False,
        **kwargs,
    ):
        """
        Parameters
        ----------
        model: Fumagalli_Motta_Tarantino_2020.Models.OptimalMergerPolicy
            Model to plot the outcomes from a range of assets.
        """
        self.set_mode(default_style, dark_mode)
        self.model: FMT20.OptimalMergerPolicy = model
        self._set_axes(ax, **kwargs)
        warnings.filterwarnings("ignore")

    def _set_axes(self, ax, **kwargs) -> None:
        if ax is None:
            self.fig, self.ax = plt.subplots(**kwargs)
        else:
            self.ax = ax
            self.fig = self.ax.get_figure()
        self.ax.patch.set_alpha(0)

    def set_mode(self, default_style: bool, dark_mode: bool) -> None:
        if dark_mode:
            self.set_dark_mode()
        else:
            self.set_light_mode(default_style)

    @staticmethod
    def set_dark_mode() -> None:
        plt.style.use("dark_background")

    @staticmethod
    def set_light_mode(default_style=False) -> None:
        if ("science" in plt.style.available) and not default_style:
            plt.style.use("science")
        else:
            plt.style.use("default")

    def set_model(self, m: FMT20.OptimalMergerPolicy) -> None:
        self.model = m
        self.ax.clear()
        self._reset_legend()
        self._set_axes(self.ax)

    def _reset_legend(self) -> None:
        try:
            self.ax.get_legend().remove()
        except AttributeError:
            pass

    def _set_primary_legend(self) -> None:
        legend = self.ax.legend(
            bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0
        )
        for entry in legend.legendHandles:
            entry.set_alpha(1)

    def _set_tight_layout(self) -> None:
        self.fig.tight_layout()

    @abstractmethod
    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        """
        Plots the visual representation for the object.

        Example
        -------
        ```
        model = Models.OptimalMergerPolicy()
        visualizer = MergerPoliciesAssetRange(m)
        fig, ax = visualizer.plot()
        # use the figure and axes as you wish, but for example:
        fig.show()
        ```

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

    def show(self, **kwargs) -> None:
        """
        Shows the visual representation for the object.

        Example
        -------
        ```
        model = Models.OptimalMergerPolicy()
        visualizer = MergerPoliciesAssetRange(m)
        visualizer.show()
        ```

        Parameters
        ----------
        kwargs
            Same options as Fumagalli_Motta_Tarantino_2020.Visualize.IVisualize.plot.
        """
        self.plot(**kwargs)
        self.fig.show()

    def _parameter_latex(self, **kwargs) -> str:
        """
        Generates a legend for the parameter values of a Fumagalli_Motta_Tarantino_2020.Models.BaseModel in latex format.

        Returns
        -------
        str
            Containing the legend for the parameter values.
        """
        separator_name_value = "="
        separator_parameters = kwargs.get("separator", " ; ")
        output_str = ""
        for (parameter, value, separator) in [
            ("A", self.model.startup_assets, separator_parameters),
            ("B", self.model.private_benefit, separator_parameters),
            ("K", self.model.development_costs, separator_parameters),
            ("p", self.model.success_probability, "\n"),
            ("CS^m", self.model.cs_without_innovation, separator_parameters),
            (
                "\\pi^m_I",
                self.model.incumbent_profit_without_innovation,
                separator_parameters,
            ),
            ("CS^M", self.model.cs_with_innovation, separator_parameters),
            (
                "\\pi^M_I",
                self.model.incumbent_profit_with_innovation,
                separator_parameters,
            ),
            ("CS^d", self.model.cs_duopoly, separator_parameters),
            ("\\pi^d_I", self.model.incumbent_profit_duopoly, separator_parameters),
            ("\\pi^d_S", self.model.startup_profit_duopoly, ""),
        ]:
            output_str += f"${parameter}{separator_name_value}{round(value, ndigits=3)}${separator}"
        return output_str

    @staticmethod
    def _get_summary_latex(summary: FMT20.OptimalMergerPolicySummary) -> str:
        """
        Generates a chronological entry for the legend based on the input model.

        Returns
        -------
        str
            Chronological entry for the legend of the input model.
        """
        separator: str = "$\\to$"
        return (
            f"{summary.early_bidding_type.abbreviation()}"
            f"{IVisualize._get_is_takeover_legend(summary.early_bidding_type, summary.early_takeover)}{separator}"
            f"{IVisualize._get_development_attempt_legend(summary.development_attempt)}"
            f"{IVisualize._get_development_outcome_legend(summary.development_attempt, summary.development_outcome)}{separator}"
            f"{summary.late_bidding_type.abbreviation()}"
            f"{IVisualize._get_is_takeover_legend(summary.late_bidding_type, summary.late_takeover)}"
        )

    @staticmethod
    def _get_is_takeover_legend(bid_attempt: FMT20.Takeover, is_takeover: bool) -> str:
        """
        Generates a string representation for legend about the takeover (option and approval).

        Parameters
        ----------
        bid_attempt: Fumagalli_Motta_Tarantino_2020.FMT20.Takeover
            Option for takeover chosen by the incumbent.
        is_takeover: bool
            If true, the takeover is approved by AA and the start-up.

        Returns
        -------
        str
            String representation for legend about takeover (option and approval).
        """
        if bid_attempt is FMT20.Takeover.No:
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
        return "" if is_developing else "$\\emptyset$"

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
            return "$\\checkmark$" if is_successful else "$\\times$"
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
            f"{FMT20.MergerPolicies.legend()}\n"
            "${\\bf Bidding\\thickspace types}$:\n"
            f"{FMT20.Takeover.legend()}\n"
            "${\\bf Takeover\\thickspace outcome\\thickspace}$:\n"
            f"{FMT20.Takeover.Pooling.abbreviation()}|{FMT20.Takeover.Separating.abbreviation()}$(\\checkmark)$: Takeover is approved by the startup and AA\n"
            f"{FMT20.Takeover.Pooling.abbreviation()}|{FMT20.Takeover.Separating.abbreviation()}$(\\times)$: Takeover is blocked  by AA or not accepted by the startup\n"
            "${\\bf Development\\thickspace outcome}$:\n"
            f"$\\emptyset$: Product development was shelved\n"
            f"$D(\\checkmark)$: Product development was attempted and successful\n"
            f"$D(\\times)$: Product development was attempted and not successful\n"
        )

    @staticmethod
    def _get_payoff_legend(market_situations_only=False) -> str:
        payoff_str = (
            "$\\pi_S$: Profit of the start-up\n"
            "$\\pi_I$: Profit of the incumbent\n"
            "$CS$: Consumer surplus\n"
            "$W$: Total welfare\n"
            if not market_situations_only
            else ""
        )
        return (
            f"{payoff_str}"
            "$m$: Monopoly without the innovation\n"
            "$M$: Monopoly after successful development by the incumbent\n"
            "$d$: Duopoly (requires successful development by the start-up)\n"
        )

    def _get_model_characteristics_latex(
        self,
        separator=" ; ",
        model_parameters=True,
        thresholds_newline=True,
        thresholds_title="Thresholds for the Start-up Assets",
        optimal_policy=False,
    ) -> str:
        parameter_text = (
            f"${{\\bf Parameters}}$\n{self._parameter_latex(separator=separator)}\n\n"
            if model_parameters
            else ""
        )
        optimal = (
            f"Optimal policy: {self.model.get_optimal_merger_policy().abbreviation()}\n"
            if optimal_policy
            else ""
        )
        thresholds_title = thresholds_title.replace(" ", "\\thickspace ")
        newline = "\n" if thresholds_newline else separator
        return (
            f"{parameter_text}"
            f"${{\\bf {thresholds_title}}}$\n"
            f"{self._get_model_characteristics_thresholds(separator, newline)}"
            f"{optimal}"
        )

    def _get_model_characteristics_thresholds(
        self, separator: str, newline: str
    ) -> str:
        return (
            f"$F(0) = {self._round_floats(self.model.asset_distribution.cumulative(0))}${separator}"
            f"$F(K) = {self._round_floats(self.model.asset_distribution.cumulative(self.model.development_costs))}${newline}"
            f"$F(\\bar{{A}}) = {self._round_floats(self.model.asset_threshold_cdf)}${separator}"
            f"$F(\\bar{{A}}^T) = {self._round_floats(self.model.asset_threshold_late_takeover_cdf)}${separator}"
            f"$\\Gamma(\\cdot) = {self._round_floats(self.model.asset_distribution_threshold_welfare)}${separator}"
            f"$\\Phi(\\cdot) = {self._round_floats(self.model.asset_distribution_threshold_profitable_without_late_takeover)}${separator}"
            f"$\\Phi'(\\cdot) = {self._round_floats(self.model.asset_distribution_threshold_unprofitable_without_late_takeover)}${separator}"
            f"$\\Phi^T(\\cdot) = {self._round_floats(self.model.asset_distribution_threshold_with_late_takeover)}$\n"
        )

    @staticmethod
    def _round_floats(value: float, digits=3) -> str:
        return f"{value:.{digits}f}"

    def _get_model_characteristics_ax(self, ax: plt.Axes) -> None:
        ax.set_title("Model Characteristics")
        ax.axis("off")
        self._annotate_model_characteristics(ax)
        self._annotate_payoff_legend(ax)
        self._annotate_symbol_legend(ax)

    def _annotate_symbol_legend(self, ax: plt.Axes) -> None:
        ax.annotate(
            self._get_symbol_legend(),
            xy=(0.5, 0.57),
            horizontalalignment="center",
            verticalalignment="top",
            fontsize=IVisualize.fontsize,
        )

    def _annotate_payoff_legend(self, ax: plt.Axes) -> None:
        ax.annotate(
            self._get_payoff_legend(market_situations_only=True),
            xy=(0.5, 0.7),
            horizontalalignment="center",
            verticalalignment="top",
            fontsize=IVisualize.fontsize,
        )

    def _annotate_model_characteristics(self, ax: plt.Axes) -> None:
        ax.annotate(
            self._get_model_characteristics_latex(),
            xy=(0.5, 1),
            xytext=(0, 0),
            textcoords="offset points",
            horizontalalignment="center",
            verticalalignment="top",
            fontsize=IVisualize.fontsize,
        )


class AssetRange(IVisualize):
    """
    Visualizes the outcomes over an assets range for a specific model.
    """

    def __init__(self, model: FMT20.OptimalMergerPolicy, **kwargs) -> None:
        super(AssetRange, self).__init__(model, **kwargs)
        self.labels: list[str] = []
        self.colors: dict[str, str] = {}

    def _get_outcomes_asset_range(
        self,
    ) -> list[FMT20.OptimalMergerPolicySummary]:
        """
        Generates a list with all essential threshold concerning the assets of a start-up and an additional list with
        summaries of the outcomes of the model in between the thresholds.

        Returns
        -------
        (list[Fumagalli_Motta_Tarantino_2020.FMT20.ThresholdItem], list[Fumagalli_Motta_Tarantino_2020.FMT20.OptimalMergerPolicySummary])
            List containing the essential asset thresholds in the model and list containing the summaries of the outcomes of the model.
        """
        asset_range: list[FMT20.ThresholdItem] = self._get_asset_thresholds()
        summaries: list[FMT20.OptimalMergerPolicySummary] = []
        for i in range(len(asset_range) - 1):
            self._set_model_startup_assets(asset_range[i], asset_range[i + 1])
            summaries.append(self.model.summary())
        return summaries

    def _set_model_startup_assets(
        self, lower_threshold: FMT20.ThresholdItem, upper_threshold: FMT20.ThresholdItem
    ) -> None:
        self.model.startup_assets = (
            self.model.asset_distribution.inverse_cumulative(lower_threshold.value)
            + self.model.asset_distribution.inverse_cumulative(upper_threshold.value)
        ) / 2

    def _get_asset_thresholds(self) -> list[FMT20.ThresholdItem]:
        """
        Generates a list with all essential threshold concerning the assets of a start-up.

        Returns
        -------
        list[Fumagalli_Motta_Tarantino_2020.FMT20.ThresholdItem]
            List containing the essential asset thresholds in the model.
        """
        thresholds = self._get_essential_thresholds()
        essential_thresholds: list[FMT20.ThresholdItem] = []
        for threshold in thresholds:
            if self._valid_x_tick(threshold):
                essential_thresholds.append(threshold)
        thresholds = sorted(essential_thresholds, key=lambda x: x.value)
        return thresholds

    def _get_essential_thresholds(self) -> list[FMT20.ThresholdItem]:
        return [
            FMT20.ThresholdItem("$F(0)$", self._get_x_min()),
            FMT20.ThresholdItem(
                "$F(K)$",
                self._get_x_max(),
            ),
            FMT20.ThresholdItem(
                "$\\Gamma$", self.model.asset_distribution_threshold_welfare
            ),
            FMT20.ThresholdItem(
                "$\\Phi$",
                self.model.asset_distribution_threshold_profitable_without_late_takeover,
            ),
            FMT20.ThresholdItem(
                "$\\Phi^T$", self.model.asset_distribution_threshold_with_late_takeover
            ),
            FMT20.ThresholdItem(
                "$\\Phi^{\\prime}$",
                self.model.asset_distribution_threshold_unprofitable_without_late_takeover,
            ),
            FMT20.ThresholdItem("$F(\\bar{A})$", self.model.asset_threshold_cdf),
            FMT20.ThresholdItem(
                "$F(\\bar{A}^T)$", self.model.asset_threshold_late_takeover_cdf
            ),
        ]

    def _get_x_labels_ticks(
        self, asset_thresholds: list[FMT20.ThresholdItem]
    ) -> (list[float], list[str]):
        """
        Generates the locations of the ticks on the x-axis and the corresponding labels on the x-axis.

        Parameters
        ----------
        asset_thresholds: list[Fumagalli_Motta_Tarantino_2020.FMT20.ThresholdItem]
            List with all threshold the assets.

        Returns
        -------
        (list[float], list[str])
            A list containing the ticks on the x-axis and a list containing the labels on the x-axis.
        """
        x_ticks: list[float] = []
        x_labels: list[str] = []
        for threshold in asset_thresholds:
            if self._valid_x_tick(threshold):
                x_ticks.append(threshold.value)
                x_labels.append(threshold.name)
        return x_ticks, x_labels

    def _set_x_axis(self, asset_thresholds: list[FMT20.ThresholdItem]) -> None:
        x_ticks, x_labels = self._get_x_labels_ticks(asset_thresholds)
        self._set_x_locators(x_ticks)
        self._set_x_labels(x_labels)
        self._set_x_ticks()

    def _set_x_ticks(self) -> None:
        self.ax.tick_params(
            which="minor",
            bottom=False,
            top=False,
            labelbottom=False,
            labeltop=True,
            axis="x",
        )
        self.ax.tick_params(which="both", bottom=False, top=False, length=6, axis="x")

    def _set_x_labels(self, x_labels: list[str]) -> None:
        self.ax.set_xticklabels(x_labels[::2], fontsize=IVisualize.fontsize)
        self.ax.set_xticklabels(
            x_labels[1::2], minor=True, fontsize=IVisualize.fontsize
        )

    def _set_x_locators(self, x_ticks: list[float]) -> None:
        self.ax.xaxis.set_major_locator(FixedLocator(x_ticks[::2]))
        self.ax.xaxis.set_minor_locator(FixedLocator(x_ticks[1::2]))

    def _draw_vertical_lines(self, asset_thresholds: list[FMT20.ThresholdItem]) -> None:
        for threshold in asset_thresholds:
            if self._valid_x_tick(threshold):
                self.ax.axvline(threshold.value, linestyle=":", color="k", lw=0.5)

    def _valid_x_tick(self, threshold):
        return self._get_x_min() <= threshold.value <= self._get_x_max()

    @staticmethod
    def _get_y_ticks(
        spacing: float, bar_height: float, y_labels: list[str]
    ) -> list[float]:
        return [(i + 1) * spacing + bar_height * i for i in range(len(y_labels))]

    def _set_y_ticks(self, bar_height: float, spacing: float, y_labels: list[str]):
        y_ticks = self._get_y_ticks(spacing, bar_height, y_labels)
        self.ax.set_yticks(y_ticks)
        self.ax.set_yticklabels(y_labels, fontsize=IVisualize.fontsize)
        self.ax.yaxis.set_ticks_position("none")

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

    def _get_summaries(self) -> list[list[FMT20.OptimalMergerPolicySummary]]:
        return [self._get_outcomes_asset_range()]

    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        asset_range = self._get_asset_thresholds()
        merger_policies_summaries = self._get_summaries()
        assert asset_range is not None
        assert merger_policies_summaries is not None
        self._clear_legend_list()
        bar_height, spacing, y_labels = self._draw_all_bars(
            asset_range, merger_policies_summaries, **kwargs
        )
        self._set_primary_legend()
        self._set_secondary_legend(asset_range[0].value, kwargs.get("legend", True))
        self._set_threshold_legend(
            kwargs.get("thresholds", False),
            kwargs.get("optimal_policy", False),
            kwargs.get("y_offset", 0),
        )
        self.ax.margins(y=spacing, x=0)
        self._draw_vertical_lines(asset_range)
        self._set_x_axis(asset_range)
        self._set_y_ticks(bar_height, spacing, y_labels)
        self.ax.set_xlabel(
            kwargs.get("x_label", "Cumulative Distribution Value of Assets $F(A)$")
        )
        self.ax.set_ylabel("Merger Policy")
        self.ax.set_title(kwargs.get("title", "Outcome dependent on Start-up Assets"))
        self._set_tight_layout()
        return self.fig, self.ax

    def _clear_legend_list(self) -> None:
        self.labels.clear()
        self.colors.clear()

    def _draw_all_bars(
        self, asset_range, merger_policies_summaries, **kwargs
    ) -> (float, float, list[str]):
        spacing: float = kwargs.get("spacing", 0.1)
        bar_height: float = kwargs.get("bar_height", 0.2)
        y_labels: list[str] = []
        for number_merger_policy, summaries in enumerate(merger_policies_summaries):
            y_labels.append(summaries[0].set_policy.abbreviation())
            for summary_index, summary in enumerate(summaries):
                label: str = self._get_summary_latex(summary)
                length: float = self._get_bar_length(asset_range, summary_index)
                y_coordinate = self._get_bar_y_coordinate(
                    bar_height, number_merger_policy, spacing
                )
                self._draw_bar(
                    y_coordinate,
                    asset_range[summary_index].value,
                    bar_height,
                    length,
                    label,
                )
        return bar_height, spacing, y_labels

    @staticmethod
    def _get_bar_length(
        asset_range: list[FMT20.ThresholdItem], summary_index: int
    ) -> float:
        return asset_range[summary_index + 1].value - asset_range[summary_index].value

    @staticmethod
    def _get_bar_y_coordinate(
        bar_height: float, number_merger_policy: int, spacing: float
    ) -> float:
        return spacing * (number_merger_policy + 1) + bar_height * number_merger_policy

    def _draw_bar(
        self,
        y_coordinate: float,
        x_coordinate: float,
        bar_height: float,
        length: float,
        label: str,
    ) -> None:
        label, color = self._get_label_color(label)
        self.ax.barh(
            y=y_coordinate,
            width=length,
            left=x_coordinate,
            height=bar_height,
            color=color,
            label=label,
        )

    def _set_threshold_legend(
        self, show_legend: bool, show_optimal_policy: bool, y_offset: int
    ) -> None:
        if show_legend:
            x_coordinate = self._get_x_max()
            self.ax.annotate(
                self._get_model_characteristics_latex(
                    separator="\n",
                    model_parameters=False,
                    thresholds_newline=False,
                    thresholds_title="",
                    optimal_policy=show_optimal_policy,
                ),
                xy=(x_coordinate, 1),
                xytext=(10, y_offset),
                textcoords="offset points",
                horizontalalignment="left",
                verticalalignment="top",
                fontsize=IVisualize.fontsize,
            )

    def _get_x_max(self):
        return self.model.asset_distribution.cumulative(self.model.development_costs)

    def _get_x_min(self):
        return self.model.asset_distribution.cumulative(0)

    def _set_secondary_legend(self, x_coordinate: float, show_legend: bool) -> None:
        if show_legend:
            self.ax.annotate(
                self._get_symbol_legend(),
                xy=(x_coordinate, 0),
                xytext=(0, -50),
                textcoords="offset points",
                horizontalalignment="left",
                verticalalignment="top",
                fontsize=IVisualize.fontsize,
            )


class MergerPoliciesAssetRange(AssetRange):
    def __init__(self, model: FMT20.OptimalMergerPolicy, **kwargs):
        super(MergerPoliciesAssetRange, self).__init__(model, **kwargs)

    def _get_outcomes_different_merger_policies(
        self,
    ) -> list[list[FMT20.OptimalMergerPolicySummary]]:
        outcomes: list[list[FMT20.OptimalMergerPolicySummary]] = []
        for merger_policy in FMT20.MergerPolicies:
            try:
                self.model.merger_policy = merger_policy
                outcomes.append(self._get_outcomes_asset_range())
            except AssertionError:
                pass
        return outcomes

    def _get_summaries(self) -> list[list[FMT20.OptimalMergerPolicySummary]]:
        return self._get_outcomes_different_merger_policies()


class MergerPoliciesAssetRangePerfectInformation(MergerPoliciesAssetRange):
    def __init__(self, model: FMT20.PerfectInformationModel, **kwargs):
        super(MergerPoliciesAssetRangePerfectInformation, self).__init__(
            model, **kwargs
        )

    def _get_essential_thresholds(self) -> list[FMT20.ThresholdItem]:
        return [
            FMT20.ThresholdItem("$0$", 0),
            FMT20.ThresholdItem(
                "$K$",
                self.model.development_costs,
            ),
            FMT20.ThresholdItem("$\\bar{A}$", self.model.asset_threshold),
            FMT20.ThresholdItem(
                "$\\bar{A}^T$", self.model.asset_threshold_late_takeover
            ),
        ]

    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        kwargs["x_label"] = kwargs.get("x_label", "Start-up Assets $A$")
        return super(MergerPoliciesAssetRangePerfectInformation, self).plot(**kwargs)

    def _set_model_startup_assets(
        self, lower_threshold: FMT20.ThresholdItem, upper_threshold: FMT20.ThresholdItem
    ) -> None:
        self.model.startup_assets = (lower_threshold.value + upper_threshold.value) / 2

    def _get_x_max(self) -> float:
        return self.model.development_costs

    def _get_x_min(self) -> float:
        return 0

    def _get_model_characteristics_thresholds(
        self, separator: str, newline: str
    ) -> str:
        return (
            f"$K = {self._round_floats(self.model.development_costs)}${separator}"
            f"$\\bar{{A}} = {self._round_floats(self.model.asset_threshold)}${separator}"
            f"$\\bar{{A}}^T = {self._round_floats(self.model.asset_threshold_late_takeover)}${separator}"
        )


class Timeline(IVisualize):
    """
    Visualizes the timeline of events for a specific model.
    """

    def __init__(self, model: FMT20.OptimalMergerPolicy, **kwargs):
        super(Timeline, self).__init__(model, **kwargs)

    def _prepare_content(self) -> (list[str], list[str]):
        """
        Generates the label and points in time of the events in the model.

        Returns
        -------
        (list[str], list[str])
            List containing label for the events and list containing the points in time of the events.
        """
        stem_labels: list[str] = [
            "Competition authority\nestablishes "
            + self._policy_str()
            + "\nmerger policy",
            self._takeover_attempt_str(self.model.early_bidding_type),
            self._takeover_str(self.model.is_early_takeover),
            self._development_str(),
            self._success_str(),
            self._takeover_attempt_str(self.model.late_bidding_type),
            self._takeover_str(self.model.is_late_takeover),
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
        return stem_labels, x_labels

    @staticmethod
    def _takeover_attempt_str(takeover: FMT20.Takeover) -> str:
        """
        Generate label for takeover event.

        Parameters
        ----------
        takeover: Fumagalli_Motta_Tarantino_2020.FMT20.Takeover
            Option for takeover chosen by the incumbent.

        Returns
        -------
        str
            Label for takeover event.
        """
        return str(takeover) + "\nby incumbent"

    def _policy_str(self) -> str:
        """
        Generate label for establishing of merger policy event.

        Returns
        -------
        str
            Label for establishing of merger policy event.
        """
        policy_str = str(self.model.merger_policy).lower()
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

    def _development_str(self) -> str:
        """
        Generates a label about the development event (attempt and shelving).

        Returns
        -------
        str
            Label about the development event (attempt and shelving).
        """
        if self.model.is_early_takeover:
            return (
                "Incumbent\n"
                + ("develops" if self.model.is_owner_investing else "shelves")
                + " product"
                + "\n(killer acquisition)"
                if self.model.is_killer_acquisition()
                else ""
            )
        return (
            "Start-up"
            + ("" if self.model.is_owner_investing else " does not")
            + "\nobtain"
            + ("s" if self.model.is_owner_investing else "")
            + " enough\nfinancial assets"
        )

    def _success_str(self) -> str:
        """
        Generates a label about the development outcome event.

        Returns
        -------
        str
            Label about the development outcome event.
        """
        if self.model.is_owner_investing:
            if self.model.is_development_successful:
                return "Development is\nsuccessful"
            return "Development is\nnot successful"
        return "Development was\nnot attempted."

    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        stem_labels, x_labels = self._prepare_content()
        x_ticks = list(range(len(x_labels)))
        stem_levels = [-1, 1, 0.6, -1, 1, -1, -0.6, 1]

        # Create figure and plot a stem plot with the date
        self.ax.set(title=kwargs.get("title", "Timeline"))
        self._set_parameter_legend(
            math.fsum(x_ticks) / len(x_ticks), kwargs.get("parameters", True)
        )
        self._draw_vertical_stems(stem_levels, x_ticks)
        self._draw_baseline(x_ticks)
        self._annotate_stems(
            stem_levels, stem_labels, x_ticks, kwargs.get("x-offset", 0)
        )
        self._set_x_axis(x_labels, x_ticks)
        self._set_y_axis()
        self.ax.margins(y=0.45)
        self._set_tight_layout()
        return self.fig, self.ax

    def _annotate_stems(
        self,
        levels: list[int],
        stem_labels: list[str],
        x_ticks: list[int],
        x_offset: int,
    ) -> None:
        for d, l, r in zip(x_ticks, levels, stem_labels):
            self.ax.annotate(
                str(r),
                xy=(d, l),
                xytext=(x_offset, np.sign(l) * 8),
                textcoords="offset points",
                horizontalalignment="center",
                verticalalignment="bottom" if l > 0 else "top",
                fontsize=IVisualize.fontsize,
            )

    def _draw_vertical_stems(self, levels: list[int], x_ticks: list[int]) -> None:
        self.ax.vlines(x_ticks, 0, levels, color="lightgray", linewidths=1)

    def _draw_baseline(self, x_ticks: list[int]) -> None:
        self.ax.plot(
            x_ticks, np.zeros_like(x_ticks), "-o", color="k", markerfacecolor="w"
        )

    def _set_x_axis(self, x_labels: list[str], x_ticks: list[int]) -> None:
        self.ax.set_xticks(x_ticks)
        self.ax.set_xticklabels(x_labels)
        self.ax.xaxis.set_ticks_position("bottom")

    def _set_y_axis(self) -> None:
        self.ax.yaxis.set_visible(False)
        self.ax.spines[["left", "top", "right"]].set_visible(False)

    def _set_parameter_legend(self, x_coordinate: float, show_parameters: bool) -> None:
        if show_parameters:
            self.ax.annotate(
                self._parameter_latex(),
                xy=(x_coordinate, 1.9),
                horizontalalignment="center",
                verticalalignment="top",
                fontsize=IVisualize.fontsize,
            )


class Payoffs(IVisualize):
    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        payoffs: dict[str, float] = self._get_payoffs()
        bar_width = kwargs.get("width", 0.35)
        spacing = kwargs.get("spacing", 0.05)
        self._plot_payoffs_bars(payoffs, bar_width, spacing, **kwargs)
        self.ax.set_title("Payoffs for different Market Configurations")
        self._set_primary_legend()
        self._set_secondary_legend(bar_width, kwargs.get("legend", True))
        self._set_tight_layout()

    def _set_secondary_legend(self, bar_width: float, show_legend: bool) -> None:
        if show_legend:
            self.ax.annotate(
                self._get_payoff_legend(),
                xy=(-bar_width, 0),
                xytext=(0, -30),
                textcoords="offset points",
                horizontalalignment="left",
                verticalalignment="top",
                fontsize=IVisualize.fontsize,
            )

    def _plot_payoffs_bars(
        self, payoffs: dict[str, float], bar_width: float, spacing: float, **kwargs
    ) -> None:
        """
        Plots the bars representing the payoffs for different market configurations of different stakeholders on the specified axis.

        Parameters
        ----------
        axis matplotlib.axes.Axes
            To plot the bars on.
        bar_width: float
            Width of a bar in the plot.
        spacing: float
            Spacing between the bars on the plot.
        **kwargs
            Optional key word arguments for the payoff plot.<br>
            - opacity : Opacity of the not optimal payoffs.<br>
        """
        max_values: list[int] = self._set_max_values(list(payoffs.values()))
        for number_bar, (label, height) in enumerate(payoffs.items()):
            x_coordinate: float = self._get_x_coordinate(bar_width, number_bar, spacing)
            self._set_x_label(label, x_coordinate)
            if number_bar > 3:
                label = "__nolegend__"
            else:
                label = self._set_payoff_label(label)
            self.ax.bar(
                x=x_coordinate,
                width=bar_width,
                height=height,
                label=label,
                color=self._get_color(number_bar),
                alpha=kwargs.get("max_opacity", 1)
                if number_bar in max_values
                else kwargs.get("min_opacity", 0.6),
            )
        self._set_x_ticks()

    def _set_x_label(self, label: str, x_coordinate: float) -> None:
        self.ax.annotate(
            label,
            xy=(x_coordinate, 0),
            xytext=(0, -15),
            textcoords="offset points",
            horizontalalignment="center",
            verticalalignment="bottom",
            fontsize=IVisualize.fontsize,
        )

    def _set_x_ticks(self) -> None:
        self.ax.tick_params(
            axis="x",
            which="both",
            bottom=False,
            top=False,
            labelbottom=False,
        )

    @staticmethod
    def _set_payoff_label(label) -> str:
        payoff_type = label[:-3]
        if "CS" in payoff_type:
            return "Consumer Surplus"
        if "W" in payoff_type:
            return "Total Welfare"
        if "I" in payoff_type:
            return "Profit Incumbent ($\\pi_I$)"
        return "Profit Start-up ($\\pi_S$)"

    @staticmethod
    def _set_max_values(payoffs: list[float]) -> list[int]:
        return [
            Payoffs._get_max_index(0, payoffs),
            Payoffs._get_max_index(1, payoffs),
            Payoffs._get_max_index(2, payoffs),
            Payoffs._get_max_index(3, payoffs),
        ]

    @staticmethod
    def _get_max_index(offset_index: int, payoffs: list[float]) -> int:
        values: list[float] = payoffs[offset_index::4]
        max_value: float = max(values)
        group_index: int = values.index(max_value)
        return group_index * 4 + offset_index

    @staticmethod
    def _get_x_coordinate(bar_width: float, number_bar: int, spacing: float) -> float:
        group_spacing: int = (math.trunc(number_bar / 4) % 4) * 8
        return spacing * (number_bar + 1 + group_spacing) + bar_width * number_bar

    @staticmethod
    def _get_color(number_bar: int, reverse_cycle=True) -> str:
        color_id = number_bar % 4
        color_id = len(IVisualize.colors) - color_id - 1 if reverse_cycle else color_id
        return IVisualize.colors[color_id]

    def _get_payoffs(self) -> dict[str, float]:
        return {
            "$\\pi_S^m$": 0,
            "$\\pi_I^m$": self.model.incumbent_profit_without_innovation,
            "$CS^m$": self.model.cs_without_innovation,
            "$W^m$": self.model.w_without_innovation,
            "$\\pi^M_S$": 0,
            "$\\pi^M_I$": self.model.incumbent_profit_with_innovation,
            "$CS^M$": self.model.cs_with_innovation,
            "$W^M$": self.model.w_with_innovation,
            "$\\pi^d_S$": self.model.startup_profit_duopoly,
            "$\\pi^d_I$": self.model.incumbent_profit_duopoly,
            "$CS^d$": self.model.cs_duopoly,
            "$W^d$": self.model.w_duopoly,
        }


class Overview(IVisualize):
    def __init__(self, model: FMT20.OptimalMergerPolicy, figsize=(14, 10), **kwargs):
        super().__init__(model, figsize=figsize, constrained_layout=True, **kwargs)
        plt.axis("off")

    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        spec = self.fig.add_gridspec(ncols=2, nrows=2)
        self.fig.suptitle("${\\bf Model\\thickspace Overview}$")
        self._generate_ax(spec[1, 0], Timeline, **kwargs)
        self._generate_ax(spec[0, 1], Payoffs, **kwargs)
        self._generate_ax(
            spec[1, 1], self._get_merger_policy_asset_range_type(), **kwargs
        )
        self._generate_characteristics_ax(spec[0, 0])

    def _get_merger_policy_asset_range_type(self) -> Callable:
        return (
            MergerPoliciesAssetRangePerfectInformation
            if type(self.model) is FMT20.PerfectInformationModel
            else MergerPoliciesAssetRange
        )

    def _generate_characteristics_ax(
        self, coordinates: matplotlib.gridspec.GridSpec
    ) -> None:
        ax = self.fig.add_subplot(coordinates)
        self._get_model_characteristics_ax(ax)

    def _generate_ax(
        self, coordinates: matplotlib.gridspec.GridSpec, visualizer: Callable, **kwargs
    ) -> None:
        ax = self.fig.add_subplot(coordinates)
        visualizer(self.model, ax=ax).plot(legend=False, parameters=False, **kwargs)
