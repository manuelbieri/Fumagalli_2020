from typing import Callable
from copy import deepcopy
import matplotlib.gridspec
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
from matplotlib.patches import Rectangle

import Fumagalli_Motta_Tarantino_2020.Models as Models
from Fumagalli_Motta_Tarantino_2020.Models.Types import *
from Fumagalli_Motta_Tarantino_2020.Visualizations.Visualize import *


class AssetRange(IVisualize):
    """
    Visualizes the outcomes over an assets range for a specific model.
    """

    def __init__(self, model: Models.OptimalMergerPolicy, **kwargs) -> None:
        super(AssetRange, self).__init__(model, **kwargs)
        self.labels: list[str] = []
        self.colors: dict[str, dict] = {}
        self._thresholds: list[Models.ThresholdItem] = self._get_essential_thresholds()
        self._check_thresholds()
        self._label_colors: dict[str:dict] = self._init_label_colors()

    @staticmethod
    def _init_label_colors() -> dict[str, dict]:
        o = PossibleOutcomes
        d = {}
        vis_success = 1.0
        vis_fail = 0.7
        vis_no_att = 0.4
        for i in [
            (o.NoTakeoversSuccessfulDevelopment, 0, vis_success),
            (o.NoTakeoversFailedDevelopment, 0, vis_fail),
            (o.NoTakeoversDevelopmentNotAttempted, 0, vis_no_att),
            (o.RejectedEarlySeparatingUnsuccessfulDevelopment, 1, vis_success),
            (o.RejectedEarlySeparatingSuccessfulDevelopment, 1, vis_fail),
            (o.EarlySeparatingSuccessfulDevelopment, 2, vis_success),
            (o.EarlySeparatingUnsuccessfulDevelopment, 2, vis_fail),
            (o.EarlySeparatingDevelopmentNotAttempted, 2, vis_no_att),
            (o.EarlyPoolingSuccessfulDevelopment, 3, vis_success),
            (o.EarlyPoolingUnsuccessfulDevelopment, 3, vis_fail),
            (o.EarlyPoolingDevelopmentNotAttempted, 3, vis_no_att),
            (o.LatePooling, 4, vis_success),
            (o.LatePoolingRejectedEarlySeparating, 4, vis_fail),
        ]:
            d.update(
                AssetRange._init_label_color(
                    outcome_type=i[0], color_id=i[1], opacity=i[2]
                ),
            )
        return d

    @staticmethod
    def _init_label_color(
        outcome_type: Models.PossibleOutcomes, color_id: int, opacity: float
    ) -> dict[dict]:
        return {
            IVisualize._get_summary_latex(outcome_type.outcome): {
                "color": IVisualize.COLORS[color_id],
                "opacity": opacity,
            }
        }

    @staticmethod
    def plot_label_colors(show_plot=False) -> plt.Axes:
        """
        Plots the colors used in the legend for asset ranges matched to the outcome.

        Returns
        -------
        plt.Axes
            Axis containing the plot.
        """
        label_colors = AssetRange._init_label_colors()
        fig, ax = plt.subplots()
        ax.set_axis_off()
        height = 0.1
        width = 0.1
        ax.set_ylim(bottom=0, top=len(label_colors) * height)
        ax.set_xlim(left=0, right=width * 1.05 + 0.02)
        for i, label in enumerate(label_colors):
            ax.text(
                width * 1.1,
                (i + 0.5) * height,
                label,
                horizontalalignment="left",
                verticalalignment="center",
            )

            ax.add_patch(
                Rectangle(
                    xy=(0, i * height),
                    width=width,
                    height=height,
                    facecolor=label_colors[label]["color"],
                    alpha=label_colors[label]["opacity"],
                )
            )
        fig.tight_layout()
        if show_plot:
            fig.show()
        return ax

    def _check_thresholds(self) -> None:
        assert (
            self._thresholds is not None and len(self._thresholds) >= 2
        ), "Essential thresholds are not valid"

    def set_model(self, model: Models.OptimalMergerPolicy) -> None:
        super(AssetRange, self).set_model(model)
        self._thresholds = self._get_essential_thresholds()
        self._check_thresholds()

    def _get_outcomes_asset_range(
        self,
    ) -> list[Models.OptimalMergerPolicySummary]:
        """
        Generates a list with all essential threshold concerning the assets of a start-up and an additional list with
        summaries of the outcomes of the model in between the thresholds.

        Returns
        -------
        (list[Fumagalli_Motta_Tarantino_2020.FMT20.ThresholdItem], list[Fumagalli_Motta_Tarantino_2020.FMT20.OptimalMergerPolicySummary])
            List containing the essential asset thresholds in the model and list containing the summaries of the outcomes of the model.
        """
        original_assets = self.model.startup_assets
        summaries: list[Models.OptimalMergerPolicySummary] = []
        for i in range(len(self._thresholds) - 1):
            self._set_model_startup_assets(self._thresholds[i], self._thresholds[i + 1])
            summaries.append(self.model.summary())
        self.model.startup_assets = original_assets
        return summaries

    def _set_model_startup_assets(
        self,
        lower_threshold: Models.ThresholdItem,
        upper_threshold: Models.ThresholdItem,
    ) -> None:
        self.model.startup_assets = (
            self._get_inverse_asset_distribution_value(lower_threshold.value)
            + self._get_inverse_asset_distribution_value(upper_threshold.value)
        ) / 2

    def _get_essential_thresholds(self) -> list[Models.ThresholdItem]:
        """
        Generates a list with all essential threshold concerning the assets of a start-up.

        Returns
        -------
        list[Fumagalli_Motta_Tarantino_2020.FMT20.ThresholdItem]
            List containing the essential asset thresholds in the model.
        """
        thresholds = self._get_available_thresholds()
        essential_thresholds: list[Models.ThresholdItem] = []
        for threshold in thresholds:
            if self._valid_x_tick(threshold):
                essential_thresholds.append(threshold)
        thresholds = sorted(essential_thresholds, key=lambda x: x.value)
        return thresholds

    def _get_available_thresholds(self) -> list[Models.ThresholdItem]:
        return [
            Models.ThresholdItem("$F(0)$", self._get_x_min(), include=True),
            Models.ThresholdItem(
                "$F(K)$",
                self._get_x_max(),
                include=True,
            ),
            Models.ThresholdItem(
                "$\\Gamma$", self.model.asset_distribution_threshold_welfare
            ),
            Models.ThresholdItem(
                "$\\Phi$",
                self.model.asset_distribution_threshold_profitable_without_late_takeover,
            ),
            Models.ThresholdItem(
                "$\\Phi^T$", self.model.asset_distribution_threshold_with_late_takeover
            ),
            Models.ThresholdItem(
                "$\\Phi^{\\prime}$",
                self.model.asset_distribution_threshold_unprofitable_without_late_takeover,
            ),
            Models.ThresholdItem("$F(\\bar{A})$", self.model.asset_threshold_cdf),
            Models.ThresholdItem(
                "$F(\\bar{A}^T)$", self.model.asset_threshold_late_takeover_cdf
            ),
            Models.ThresholdItem(
                "$\\Lambda(\\cdot)$",
                self.model.asset_distribution_threshold_shelving_approved,
            ),
        ]

    def _get_x_labels_ticks(self) -> (list[float], list[str]):
        """
        Generates the locations of the ticks on the x-axis and the corresponding labels on the x-axis.

        Returns
        -------
        (list[float], list[str])
            A list containing the ticks on the x-axis and a list containing the labels on the x-axis.
        """
        x_ticks: list[float] = []
        x_labels: list[str] = []
        for threshold in self._thresholds:
            x_ticks.append(threshold.value)
            x_labels.append(threshold.name)
        return x_ticks, x_labels

    def _set_x_axis(self, **kwargs) -> None:
        x_ticks, x_labels = self._get_x_labels_ticks()
        self._set_x_locators(x_ticks)
        self._set_x_labels(x_labels)
        self._set_x_ticks()
        self.ax.set_xlabel(
            kwargs.get("x_label", "Cumulative Distribution Value of Assets $F(A)$")
        )

    def _set_x_ticks(self) -> None:
        self.ax.tick_params(
            which="minor",
            bottom=False,
            top=True,
            labelbottom=False,
            labeltop=True,
            axis="x",
            pad=0,
        )
        self.ax.tick_params(which="major", top=False, pad=3, axis="x")
        self.ax.tick_params(which="both", length=2, axis="x")

    def _set_x_labels(self, x_labels: list[str]) -> None:
        self.ax.set_xticklabels(x_labels[::2], fontsize=IVisualize.fontsize)
        self.ax.set_xticklabels(
            x_labels[1::2], minor=True, fontsize=IVisualize.fontsize
        )

    def _set_x_locators(self, x_ticks: list[float]) -> None:
        self.ax.xaxis.set_major_locator(FixedLocator(x_ticks[::2]))
        self.ax.xaxis.set_minor_locator(FixedLocator(x_ticks[1::2]))

    def _draw_vertical_lines(
        self, asset_thresholds: list[Models.ThresholdItem]
    ) -> None:
        for threshold in asset_thresholds:
            if self._valid_x_tick(threshold) or threshold.include:
                self.ax.axvline(threshold.value, linestyle=":", color="k", lw=0.5)

    def _valid_x_tick(self, threshold):
        return (
            self._get_x_min() < threshold.value < self._get_x_max()
        ) or threshold.include

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

    def _get_label_color(self, label) -> (str, str, float):
        """
        Returns the color and the final label for a legend entry.

        Through this method, duplications in the legend are avoided.

        Parameters
        ----------
        label: str

        Returns
        -------
        (str, str, float)
            String representing the final label, a string representing the color and a float representing the opacity.
        """
        if label in self.labels:
            return (
                "_nolegend_",
                self.colors[label]["color"],
                self.colors[label]["opacity"],
            )
        self.colors[label] = self._get_label_specific_color(label)
        self.labels.append(label)
        return label, self.colors[label]["color"], self.colors[label]["opacity"]

    def _get_label_specific_color(self, label: str) -> dict:
        if label in self._label_colors.keys():
            return self._label_colors[label]
        return {"color": IVisualize.COLORS[4], "opacity": 0.5}

    def _get_summaries(self) -> list[list[Models.OptimalMergerPolicySummary]]:
        return [self._get_outcomes_asset_range()]

    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        """
        Plots the outcome of a model over a range of assets.

        Example
        -------
        ```
        import Fumagalli_Motta_Tarantino_2020 as FMT20

        model = FMT20.OptimalMergerPolicy()
        visualizer = FMT20.MergerPoliciesAssetRange(m)
        fig, ax = visualizer.plot()
        # use the figure and axes as you wish, for example:
        fig.show()
        ```

        Parameters
        ----------
        **kwargs
            Options for further customization of the plots.
            - title(str): Title for plot<br>
            - x_label(str): Title for x-axis.<br>
            - y_label(str): Title for y-axis.<br>
            - legend(bool): If true, a secondary legend is shown.<br>
            - thresholds(bool): If true, the essential thresholds are shown.<br>
            - optimal_policy(bool): If true, the optimal policy is shown.
            - y_offset(int): Moves the threshold legend vertically.

        Returns
        -------
        Figure
            Containing the axes with the plots (use Figure.show() to display).
        Axes
            Containing the plots (arrange custom summary).
        """
        merger_policies_summaries = self._get_summaries()
        assert merger_policies_summaries is not None
        self._clear_legend_list()
        bar_height, spacing, y_labels = self._draw_all_bars(
            merger_policies_summaries, **kwargs
        )
        self._set_asset_range_legends(**kwargs)
        self._draw_vertical_lines(self._thresholds)
        self._set_x_axis(**kwargs)
        self._set_y_axis(bar_height, spacing, y_labels, **kwargs)
        self.ax.set_title(kwargs.get("title", "Outcome dependent on Start-up Assets"))
        self._set_tight_layout(y_spacing=spacing)
        return self.fig, self.ax

    def _set_y_axis(self, bar_height, spacing, y_labels, **kwargs):
        self._set_y_ticks(bar_height, spacing, y_labels)
        self.ax.set_ylabel(kwargs.get("y_label", "Merger Policy"))

    def _set_asset_range_legends(self, **kwargs):
        self._set_primary_legend(equal_opacity=False)
        self._set_secondary_legend(
            self._thresholds[0].value, kwargs.get("legend", True)
        )
        self._set_threshold_legend(
            kwargs.get("thresholds", False),
            kwargs.get("optimal_policy", False),
            kwargs.get("y_offset", 0),
        )

    def _clear_legend_list(self) -> None:
        self.labels.clear()
        self.colors.clear()

    def _draw_all_bars(
        self, merger_policies_summaries, **kwargs
    ) -> (float, float, list[str]):
        spacing: float = kwargs.get("spacing", 0.1)
        bar_height: float = kwargs.get("bar_height", 0.2)
        y_labels: list[str] = []
        for number_merger_policy, summaries in enumerate(merger_policies_summaries):
            y_labels.append(summaries[0].set_policy.abbreviation())
            for summary_index, summary in enumerate(summaries):
                label: str = self._get_summary_latex(summary)
                length: float = self._get_bar_length(summary_index)
                y_coordinate = self._get_bar_y_coordinate(
                    bar_height, number_merger_policy, spacing
                )
                self._draw_bar(
                    y_coordinate,
                    self._thresholds[summary_index].value,
                    bar_height,
                    length,
                    label,
                )
        return bar_height, spacing, y_labels

    def _get_bar_length(self, summary_index: int) -> float:
        return (
            self._thresholds[summary_index + 1].value
            - self._thresholds[summary_index].value
        )

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
        label, color, opacity = self._get_label_color(label)
        self.ax.barh(
            y=y_coordinate,
            width=length,
            left=x_coordinate,
            height=bar_height,
            color=color,
            label=label,
            alpha=opacity,
        )

    def _set_threshold_legend(
        self, show_legend: bool, show_optimal_policy: bool, y_offset: int
    ) -> None:
        if show_legend:
            x_coordinate = self._get_x_max()
            y_coordinate = self._get_y_max()
            self.ax.annotate(
                self._get_model_characteristics(
                    separator="\n",
                    model_parameters=False,
                    thresholds_newline=False,
                    threshold_title="",
                    optimal_policy=show_optimal_policy,
                ),
                xy=(x_coordinate, y_coordinate),
                xytext=(10, y_offset),
                textcoords="offset points",
                horizontalalignment="left",
                verticalalignment="top",
                fontsize=IVisualize.fontsize,
            )

    @staticmethod
    def _get_y_max() -> float:
        return 1

    def _get_x_max(self):
        return self._get_asset_distribution_value(self.model.development_costs)

    def _get_x_min(self):
        return self._get_asset_distribution_value(0)

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
    def _get_outcomes_different_merger_policies(
        self,
    ) -> list[list[Models.OptimalMergerPolicySummary]]:
        original_policy = self.model.merger_policy
        outcomes: list[list[Models.OptimalMergerPolicySummary]] = []
        for merger_policy in Models.MergerPolicies:
            try:
                self.model.merger_policy = merger_policy
                outcomes.append(self._get_outcomes_asset_range())
            except Models.Exceptions.MergerPolicyNotAvailable:
                pass
        self.model.merger_policy = original_policy
        return outcomes

    def _get_summaries(self) -> list[list[Models.OptimalMergerPolicySummary]]:
        return self._get_outcomes_different_merger_policies()


class MergerPoliciesAssetRangePerfectInformation(MergerPoliciesAssetRange):
    def __init__(self, model: Models.PerfectInformation, **kwargs):
        """
        Uses a Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.PerfectInformation for the visualization. See
        Fumagalli_Motta_Tarantino_2020.Models.Base.CoreModel for other parameters.

        Parameters
        ----------
        model: Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.PerfectInformation
            Model to create the visualization from.
        """
        super(MergerPoliciesAssetRangePerfectInformation, self).__init__(
            model, **kwargs
        )

    def _get_available_thresholds(self) -> list[Models.ThresholdItem]:
        return [
            Models.ThresholdItem("$0$", self._get_x_min(), include=True),
            Models.ThresholdItem("$K$", self._get_x_max(), include=True),
            Models.ThresholdItem("$\\bar{A}$", self.model.asset_threshold),
            Models.ThresholdItem(
                "$\\bar{A}^T$", self.model.asset_threshold_late_takeover
            ),
        ]

    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        """
        Plots the visual representation for the object.

        Example
        -------
        ```
        import Fumagalli_Motta_Tarantino_2020 as FMT20

        model = FMT20.PerfectInformation()
        visualizer = FMT20.MergerPoliciesAssetRangePerfectInformation(m)
        fig, ax = visualizer.plot()
        # use the figure and axes as you wish, for example:
        fig.show()
        ```

        Parameters
        ----------
        **kwargs
            Options for further customization of the plots (see Fumagalli_Motta_Tarantino_2020.Visualizations.VisualizeRanges.AssetRange.plot).

        Returns
        -------
        Figure
            Containing the axes with the plots (use Figure.show() to display).
        Axes
            Containing the plots (arrange custom summary).
        """
        kwargs["x_label"] = kwargs.get("x_label", "Start-up Assets $A$")
        return super(MergerPoliciesAssetRangePerfectInformation, self).plot(**kwargs)

    def _set_model_startup_assets(
        self,
        lower_threshold: Models.ThresholdItem,
        upper_threshold: Models.ThresholdItem,
    ) -> None:
        self.model.startup_assets = (lower_threshold.value + upper_threshold.value) / 2

    @staticmethod
    def _get_y_max() -> float:
        return 0.55

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


class Overview(IVisualize):
    """
    Combines Fumagalli_Motta_Tarantino_2020.Visualizations.Visualize.Timeline, Fumagalli_Motta_Tarantino_2020.Visualizations.Visualize.Payoffs,
    Fumagalli_Motta_Tarantino_2020.Visualizations.VisualizeRanges.MergerPoliciesAssetRange as well as a legend for the
    model characteristics.
    """

    def __init__(self, model: Models.OptimalMergerPolicy, figsize=(14, 10), **kwargs):
        super().__init__(model, figsize=figsize, constrained_layout=True, **kwargs)
        self.timeline: Optional[IVisualize] = None
        self.payoffs: Optional[IVisualize] = None
        self.range: Optional[IVisualize] = None
        self.kwargs = kwargs
        self._clear_main_axes()

    def set_model(self, model: Models.OptimalMergerPolicy) -> None:
        assert (
            self.timeline is not None
            and self.payoffs is not None
            and self.range is not None
        )
        super(Overview, self).set_model(model)
        self.timeline.set_model(model)
        self.payoffs.set_model(model)
        self.range.set_model(model)
        self.fig.clear()

    @staticmethod
    def _clear_main_axes() -> None:
        plt.axis("off")

    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        """
        Plots the visual representation for the object.

        Example
        -------
        ```
        import Fumagalli_Motta_Tarantino_2020 as FMT20

        model = FMT20.OptimalMergerPolicy()
        visualizer = FMT20.Overview(m)
        fig, ax = visualizer.plot()
        # use the figure and axes as you wish, for example:
        fig.show()
        ```

        Parameters
        ----------
        **kwargs
            Options for further customization of the plots (Note: all subplots use the same kwargs).
            - figure_title(str): Title for plot.<br>
            - fontsize(int): Fontsize for model characteristics.<br>
            - model_thresholds(bool): If true, the essential thresholds are shown in model characteristics.<br>
            $\\Rightarrow$ see the included visualizations for further arguments.

        Returns
        -------
        Figure
            Containing the axes with the plots (use Figure.show() to display).
        Axes
            Containing the plots (arrange custom summary).
        """
        spec = self.fig.add_gridspec(ncols=2, nrows=2)
        self._set_fig_title(**kwargs)
        self.timeline = self._generate_visualizer(spec[1, 0], Timeline, **kwargs)
        self.payoffs = self._generate_visualizer(spec[0, 1], Payoffs, **kwargs)
        self.range = self._generate_visualizer(
            spec[1, 1], self._get_merger_policy_asset_range_type(), **kwargs
        )
        self._generate_characteristics_ax(spec[0, 0], **kwargs)
        return self.fig, self.ax

    def _set_fig_title(self, **kwargs):
        self.fig.suptitle(
            kwargs.get("figure_title", "Model Overview"),
            fontsize=18,
        )

    def _get_merger_policy_asset_range_type(self) -> Callable:
        return (
            MergerPoliciesAssetRangePerfectInformation
            if type(self.model) is Models.PerfectInformation
            else MergerPoliciesAssetRange
        )

    def _generate_characteristics_ax(
        self, coordinates: matplotlib.gridspec.GridSpec, **kwargs
    ) -> None:
        ax = self.fig.add_subplot(coordinates)
        characteristics_kwargs = deepcopy(kwargs)
        characteristics_kwargs["model_thresholds"] = characteristics_kwargs.get(
            "model_thresholds", not characteristics_kwargs.get("thresholds", False)
        )
        characteristics_kwargs["optimal_policy"] = False
        self._get_model_characteristics_ax(ax, **characteristics_kwargs)

    def _generate_visualizer(
        self, coordinates: matplotlib.gridspec.GridSpec, visualizer: Callable, **kwargs
    ) -> IVisualize:
        ax = self.fig.add_subplot(coordinates)
        visualization: IVisualize = visualizer(self.model, ax=ax, **self.kwargs)
        visualization.plot(legend=False, parameters=False, **kwargs)
        return visualization
