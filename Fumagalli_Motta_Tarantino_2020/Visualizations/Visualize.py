from abc import abstractmethod
from typing import Final, Optional
import warnings

import math
import numpy as np
import matplotlib.pyplot as plt

import Fumagalli_Motta_Tarantino_2020.Models as FMT20


class IVisualize:
    """
    Interface for all visualization classes containing useful methods.

    Notes
    -----
    This module is compatible with python versions starting from 3.9, due to introduction of PEP 585. Therefore, the compatibility
    with mybinder.org is not guaranteed (uses python 3.7 at the moment ).
    """

    COLORS: Final[list[str]] = ["salmon", "gold", "lawngreen", "turquoise", "thistle"]
    """Standard colors used in visualizations."""
    fontsize = "x-small"
    """Default font size for all plots."""

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
            Model to create the visualization from.
        ax: Optional[matplotlib.pyplot.Axes]
            Axes used for the plot, if not specified, a new set of axes is generated.
        default_style: bool
            If true, default matplotlib style is used.
        dark_mode
            If true, dark mode is used.
        **kwargs
            Arguments for the creation of a new figure.
        """
        self._set_mode(default_style, dark_mode)
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

    def _set_mode(self, default_style: bool, dark_mode: bool) -> None:
        if dark_mode:
            self._set_dark_mode()
        else:
            self._set_light_mode(default_style)

    @staticmethod
    def _set_dark_mode() -> None:
        plt.style.use("dark_background")

    @staticmethod
    def _set_light_mode(default_style=False) -> None:
        if ("science" in plt.style.available) and not default_style:
            plt.style.use("science")
        else:
            plt.style.use("default")

    def set_model(self, model: FMT20.OptimalMergerPolicy) -> None:
        """
        Change the model for the visualization.

        Example
        -------
        ```python
        import Fumagalli_Motta_Tarantino_2020 as FMT20

        model_one = FMT20.OptimalMergerPolicy()
        model_two = FMT20.OptimalMergerPolicy(development_success=False)
        visualizer = FMT20.Overview(model_one)
        visualizer.show()
        # set the new model
        visualizer.set_model(model_two)
        # overwrite the previous plot
        visualizer.show()
        ```

        Parameters
        ----------
        model: Fumagalli_Motta_Tarantino_2020.Models.OptimalMergerPolicy
            New model to generate the plots from.
        """
        self.model = model
        self.ax.clear()
        self._reset_legend()
        self._set_axes(self.ax)

    def _reset_legend(self) -> None:
        try:
            self.ax.get_legend().remove()
        except AttributeError:
            pass

    def _set_primary_legend(self, equal_opacity=True) -> None:
        legend: plt.legend = self.ax.legend(
            bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0, framealpha=0
        )
        if equal_opacity:
            for entry in legend.legend_handles:
                entry.set_alpha(1)

    def _set_tight_layout(self, y_spacing: float = None, x_spacing: float = 0) -> None:
        if y_spacing is not None or x_spacing is not None:
            self.ax.margins(y=y_spacing, x=x_spacing)
        self.fig.tight_layout()

    @abstractmethod
    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        """
        Plots the visual representation for the object.

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
            Options for further customization of the plots .

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
        **kwargs
            Same options as Fumagalli_Motta_Tarantino_2020.Visualize.IVisualize.plot.
        """
        self.plot(**kwargs)
        self.fig.show()

    @staticmethod
    def get_model_label(m: type(FMT20.OptimalMergerPolicy)) -> str:
        """
        Returns a label for a given model extending Fumagalli_Motta_Tarantino_2020.Models.OptimalMergerPolicy.

        Parameters
        ----------
        m: type(FMT20.OptimalMergerPolicy)
            Type of the model
        """

        def _check_type(model_to_check, type_to_check):
            return (
                isinstance(model_to_check, type_to_check)
                or model_to_check == type_to_check
            )

        if _check_type(m, FMT20.OptimalMergerPolicy):
            return "Optimal Merger Policy"
        if _check_type(m, FMT20.ProCompetitive):
            return "Pro-Competitive"
        if _check_type(m, FMT20.ResourceWaste):
            return "Resource Waste"
        if _check_type(m, FMT20.PerfectInformation):
            return "Perfect Information"
        if _check_type(m, FMT20.CournotCompetition):
            return "Cournot Competition"
        if _check_type(m, FMT20.EquityContract):
            return "Equity Contract"

    def _get_parameter_legend(self, **kwargs) -> str:
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
        counter = 2
        number_parameters_per_line = kwargs.get("parameter_number", 6)
        for parameter, value in [
            ("A", self.model.startup_assets),
            ("B", self.model.private_benefit),
            ("K", self.model.development_costs),
            ("p", self.model.success_probability),
            ("CS^m", self.model.cs_without_innovation),
            ("\\pi^m_I", self.model.incumbent_profit_without_innovation),
            ("CS^M", self.model.cs_with_innovation),
            ("\\pi^M_I", self.model.incumbent_profit_with_innovation),
            ("CS^d", self.model.cs_duopoly),
            ("\\pi^d_I", self.model.incumbent_profit_duopoly),
            ("\\pi^d_S", self.model.startup_profit_duopoly),
        ]:
            separator = (
                ""
                if counter == 12
                else (
                    "\n"
                    if counter % number_parameters_per_line == 0
                    else separator_parameters
                )
            )
            output_str += f"${parameter}{separator_name_value}{round(value, ndigits=3)}${separator}"
            counter += 1
        return output_str

    @staticmethod
    def _get_summary_latex(summary: FMT20.Outcome) -> str:
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
            f"{IVisualize._get_takeover_legend(summary.early_bidding_type, summary.early_takeover)}{separator}"
            f"{IVisualize._get_development_attempt_legend(summary.development_attempt)}"
            f"{IVisualize._get_development_outcome_legend(summary.development_attempt, summary.development_outcome)}{separator}"
            f"{summary.late_bidding_type.abbreviation()}"
            f"{IVisualize._get_takeover_legend(summary.late_bidding_type, summary.late_takeover)}"
        )

    @staticmethod
    def _get_takeover_legend(bid_attempt: FMT20.Takeover, is_takeover: bool) -> str:
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
            f"$\\checkmark$: Product development was attempted and successful\n"
            f"$\\times$: Product development was attempted and not successful\n"
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
            "${\\bf Market\\thickspace configurations}$\n"
            f"{payoff_str}"
            "$m$: Monopoly without the innovation\n"
            "$M$: Monopoly (innovation in possession of incumbent)\n"
            "$d$: Duopoly (requires successful development by the start-up)\n"
        )

    def _get_model_characteristics(
        self,
        separator=" ; ",
        model_parameters=True,
        model_thresholds=True,
        thresholds_newline=True,
        optimal_policy=False,
        **kwargs,
    ) -> str:
        newline = "\n" if thresholds_newline else separator
        parameter_text = (
            f"${{\\bf Parameters}}$\n{self._get_parameter_legend(separator=separator, **kwargs)}\n"
            if model_parameters
            else ""
        )
        threshold_title = kwargs.get(
            "threshold_title",
            "Thresholds\\thickspace for\\thickspace the\\thickspace Start-up\\thickspace Assets",
        )
        thresholds = (
            f"${{\\bf {threshold_title}}}$\n"
            f"{self._get_model_characteristics_thresholds(separator, newline)}"
            if model_thresholds
            else ""
        )
        optimal = (
            f"Optimal policy: {self.model.get_optimal_merger_policy().abbreviation()}\n"
            if optimal_policy
            else ""
        )
        return f"{parameter_text}{thresholds}{optimal}"

    def _get_model_characteristics_thresholds(
        self, separator: str, newline: str
    ) -> str:
        return (
            f"$F(0) = {self._round_floats(self._get_asset_distribution_value(0))}${separator}"
            f"$F(K) = {self._round_floats(self._get_asset_distribution_value(self.model.development_costs))}${separator}"
            f"$F(\\bar{{A}}) = {self._round_floats(self.model.asset_threshold_cdf)}${separator}"
            f"$F(\\bar{{A}}^T) = {self._round_floats(self.model.asset_threshold_late_takeover_cdf)}${newline}"
            f"$\\Gamma(\\cdot) = {self._round_floats(self.model.asset_distribution_threshold_welfare)}${separator}"
            f"$\\Phi(\\cdot) = {self._round_floats(self.model.asset_distribution_threshold_profitable_without_late_takeover)}${separator}"
            f"$\\Phi'(\\cdot) = {self._round_floats(self.model.asset_distribution_threshold_unprofitable_without_late_takeover)}${separator}"
            f"$\\Phi^T(\\cdot) = {self._round_floats(self.model.asset_distribution_threshold_with_late_takeover)}${separator}"
            f"$\\Lambda(\\cdot) = {self._round_floats(self.model.asset_distribution_threshold_shelving_approved)}$\n"
        )

    def _get_asset_distribution_value(self, value: float) -> float:
        return self.model.asset_distribution.cumulative(
            value, **self.model.asset_distribution_kwargs
        )

    def _get_inverse_asset_distribution_value(self, value: float) -> float:
        return self.model.asset_distribution.inverse_cumulative(
            value, **self.model.asset_distribution_kwargs
        )

    @staticmethod
    def _round_floats(value: float, digits=3) -> str:
        return f"{value:.{digits}f}"

    def _get_model_characteristics_ax(self, ax: plt.Axes, **kwargs) -> None:
        ax.set_title(kwargs.get("title", "Model Characteristics"))
        ax.axis("off")
        model_characteristics = self._get_model_characteristics(**kwargs)
        text_to_annotate = (
            f"{model_characteristics}"
            f"{self._get_payoff_legend(market_situations_only=True)}"
            f"{self._get_symbol_legend()}"
        )
        ax.annotate(
            text_to_annotate,
            xy=(0.5, 1),
            xytext=(0, 0),
            textcoords="offset points",
            horizontalalignment="center",
            verticalalignment="top",
            fontsize=kwargs.get("fontsize", IVisualize.fontsize),
        )


class Timeline(IVisualize):
    """
    Visualizes the timeline of events for a specific model.
    """

    def __init__(self, model: FMT20.OptimalMergerPolicy, **kwargs):
        super(Timeline, self).__init__(model, **kwargs)
        self.high_stem = 0.6
        self.low_stem = 0.3
        self.stem_levels = [
            -self.high_stem,
            self.high_stem,
            self.low_stem,
            -self.high_stem,
            self.high_stem,
            -self.high_stem,
            -self.low_stem,
            self.high_stem,
        ]
        self._x_ticks = list(range(len(self.stem_levels)))

    def _get_stem_labels(self) -> list[str]:
        """
        Generates the label and points in time of the events in the model.

        Returns
        -------
        (list[str], list[str])
            List containing label for the events and list containing the points in time of the events.
        """
        (
            earl_takeover_attempt,
            early_takeover,
            late_takeover_attempt,
            late_takeover,
        ) = self._get_takeover_labels()
        return [
            "Competition authority\nestablishes "
            + self._policy_label()
            + "\nmerger policy",
            earl_takeover_attempt,
            early_takeover,
            self._development_label(),
            self._success_str(),
            late_takeover_attempt,
            late_takeover,
            self._get_payoff_label(),
        ]

    def _get_payoff_label(self):
        label = "Payoffs\n"
        if self.model.is_early_takeover or self.model.is_late_takeover:
            if self.model.is_development_successful:
                return label + "($CS^M$, $\\pi^M_I$)"
            return label + "($CS^m$, $\\pi^m_I$)"
        return label + "($CS^d$, $\\pi^d_I$, $\\pi^d_S$)"

    def _get_takeover_labels(self) -> list[str, str, str, str]:
        if self.model.is_early_takeover:
            late_takeover_attempt = "Start-up already\nacquired"
            late_takeover = ""
            self.stem_levels[5] = -self.low_stem
            self.stem_levels[6] = 0
        elif self.model.merger_policy in [
            FMT20.MergerPolicies.Strict,
            FMT20.MergerPolicies.Intermediate_late_takeover_prohibited,
        ]:
            late_takeover_attempt = "Competition authority\nblocks late\ntakeovers"
            late_takeover = ""
            self.stem_levels[5] = -self.low_stem
            self.stem_levels[6] = 0
        else:
            late_takeover_attempt = self._takeover_attempt_label(
                self.model.late_bidding_type
            )
            late_takeover = self._takeover_label(
                self.model.late_bidding_type, self.model.is_late_takeover
            )

        return [
            self._takeover_attempt_label(self.model.early_bidding_type),
            self._takeover_label(
                self.model.early_bidding_type, self.model.is_early_takeover
            ),
            late_takeover_attempt,
            late_takeover,
        ]

    @staticmethod
    def _get_x_labels() -> list[str]:
        return [
            "t=0",
            "t=1a",
            "t=1b",
            "t=1c",
            "t=1d",
            "t=2a",
            "t=2b",
            "t=3",
        ]

    @staticmethod
    def _takeover_attempt_label(takeover: FMT20.Takeover) -> str:
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

    def _policy_label(self) -> str:
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
    def _takeover_label(
        takeover_attempt: FMT20.Takeover, is_takeover_accepted: bool
    ) -> str:
        """
        Generates a label about the takeover event (option and approval).

        Parameters
        ----------
        takeover_attempt: FMT20.Takeover
            Type of the bid by the incumbent.
        is_takeover_accepted: bool
            If true, the takeover is approved by AA and the start-up.

        Returns
        -------
        str
            Label about the takeover event (option and approval).
        """
        is_takeover_attempt = takeover_attempt is not FMT20.Takeover.No
        if is_takeover_attempt and is_takeover_accepted:
            return "Takeover\napproved"
        if is_takeover_attempt and not is_takeover_accepted:
            return "Takeover rejected\nby start-up"
        return "No takeover\noccurs"

    def _development_label(self) -> str:
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
        """
        Plots the visual representation for the object.

        Example
        -------
        ```
        import Fumagalli_Motta_Tarantino_2020 as FMT20

        model = FMT20.OptimalMergerPolicy()
        visualizer = FMT20.Timeline(m)
        fig, ax = visualizer.plot()
        # use the figure and axes as you wish, for example:
        fig.show()
        ```

        Parameters
        ----------
        **kwargs
            Options for further customization of the plots.
            - title(str): Title for timeline<br>
            - parameters(bool): If true, a legend containing the parameters is shown.
            - x_offset(int): Moves the text at the stems horizontally.

        Returns
        -------
        Figure
            Containing the axes with the plots (use Figure.show() to display).
        Axes
            Containing the plots (arrange custom summary).
        """
        self.ax.set(title=kwargs.get("title", "Timeline"))
        self._set_parameter_legend(kwargs.get("parameters", True))
        self._draw_timeline(**kwargs)
        self._set_x_axis()
        self._set_y_axis()
        self._set_tight_layout(y_spacing=0.45, x_spacing=0.02)
        return self.fig, self.ax

    def _draw_timeline(self, **kwargs):
        self._annotate_stems(kwargs.get("x_offset", 0))
        self._draw_vertical_stems()
        self._draw_baseline()

    def _annotate_stems(
        self,
        x_offset: int,
    ) -> None:
        for d, l, r in zip(self._x_ticks, self.stem_levels, self._get_stem_labels()):
            self.ax.annotate(
                str(r),
                xy=(d, l),
                xytext=(x_offset, np.sign(l) * 8),
                textcoords="offset points",
                horizontalalignment="center",
                verticalalignment="bottom" if l > 0 else "top",
                fontsize=IVisualize.fontsize,
            )

    def _draw_vertical_stems(self) -> None:
        self.ax.vlines(
            self._x_ticks, 0, self.stem_levels, color="lightgray", linewidths=1
        )

    def _draw_baseline(self) -> None:
        self.ax.plot(
            self._x_ticks,
            np.zeros_like(self._x_ticks),
            "-o",
            color="k",
            markerfacecolor="w",
        )

    def _set_x_axis(self) -> None:
        self.ax.set_xticks(self._x_ticks)
        self.ax.set_xticklabels(self._get_x_labels())
        self.ax.xaxis.set_ticks_position("bottom")

    def _set_y_axis(self) -> None:
        self.ax.yaxis.set_visible(False)
        self.ax.spines[["left", "top", "right"]].set_visible(False)

    def _set_parameter_legend(self, show_parameters: bool) -> None:
        x_coordinate = math.fsum(self._x_ticks) / len(self._x_ticks)
        if show_parameters:
            self.ax.annotate(
                self._get_parameter_legend(),
                xy=(x_coordinate, self.high_stem * 1.8),
                horizontalalignment="center",
                verticalalignment="top",
                fontsize=IVisualize.fontsize,
            )


class Payoffs(IVisualize):
    """
    Visualizes the payoffs for a specific model.
    """

    def plot(self, **kwargs) -> (plt.Figure, plt.Axes):
        """
        Plots the visual representation for the object.

        Example
        -------
        ```
        import Fumagalli_Motta_Tarantino_2020 as FMT20

        model = FMT20.OptimalMergerPolicy()
        visualizer = FMT20.Payoffs(m)
        fig, ax = visualizer.plot()
        # use the figure and axes as you wish, for example:
        fig.show()
        ```

        Parameters
        ----------
        **kwargs
            Options for further customization of the plots.
            - title(str): Title for plot<br>
            - legend(bool): If true, a secondary legend is shown.<br>
            - width(float): Width of the bars.<br>
            - spacing(float): Spacing between the bars.<br>
            - max_opacity(float): Opacity of the optimal payoffs.<br>
            - min_opacity(float): Opacity of the not optimal payoffs.<br>

        Returns
        -------
        Figure
            Containing the axes with the plots (use Figure.show() to display).
        Axes
            Containing the plots (arrange custom summary).
        """
        payoffs: dict[str, float] = self._get_payoffs()
        bar_width = kwargs.get("width", 0.35)
        spacing = kwargs.get("spacing", 0.05)
        self._plot_payoffs_bars(payoffs, bar_width, spacing, **kwargs)
        self.ax.set_title(
            kwargs.get("title", "Payoffs for different Market Configurations")
        )
        self._set_primary_legend()
        self._set_secondary_legend(bar_width, kwargs.get("legend", True))
        self._set_tight_layout(x_spacing=spacing)

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
            - max_opacity(float): Opacity of the optimal payoffs.<br>
            - min_opacity(float): Opacity of the not optimal payoffs.<br>
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
                alpha=(
                    kwargs.get("max_opacity", 1)
                    if number_bar in max_values
                    else kwargs.get("min_opacity", 0.5)
                ),
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
        color_id = len(IVisualize.COLORS) - color_id - 1 if reverse_cycle else color_id
        return IVisualize.COLORS[color_id]

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
