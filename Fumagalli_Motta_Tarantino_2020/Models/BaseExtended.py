import Fumagalli_Motta_Tarantino_2020.Models.Types as Types
import Fumagalli_Motta_Tarantino_2020.Models.Exceptions as Exceptions
import Fumagalli_Motta_Tarantino_2020.Models.Base as Base


class CournotCompetition(Base.OptimalMergerPolicy):
    """
    In this model is assumed that the product of the start-up is an imperfect substitute of the existing product of the
    incumbent. The competition in the market is like a Cournot Competition.

    See section 7 of Fumagalli et al. (2020).
    """

    def __init__(self, gamma=0.3, *args, **kwargs):
        """

        Parameters
        ----------
        gamma:float
            Degree of substitutability of the product of the start-up and the existing product of the incumbent
            (between 0 and 1).
        """
        assert 0 < gamma < 1, "Gamma has to be between 0 and 1."
        self._gamma = gamma
        super(CournotCompetition, self).__init__(*args, **kwargs)
        assert (
            self.development_costs < self.success_probability / 4
        ), "K >= p/4 is not valid"
        self._calculate_cournot_payoffs()

    def _calculate_cournot_payoffs(self):
        self._incumbent_profit_without_innovation = 0.25
        self._cs_without_innovation = 0.125
        self._incumbent_profit_with_innovation = 1 / (2 + 2 * self.gamma)
        self._cs_with_innovation = 1 / (4 + 4 * self.gamma)
        self._incumbent_profit_duopoly = 1 / (2 + self.gamma) ** 2
        self._startup_profit_duopoly = self._incumbent_profit_duopoly
        self._cs_duopoly = (1 + self.gamma) / ((2 + self.gamma) ** 2)

    def _check_assumption_one(self):
        assert (self.gamma**2) / (
            ((2 + self.gamma) ** 2) * (2 + 2 * self.gamma)
        ) > 0, "A1 adjusted for the micro foundation model."

    def _check_assumption_two(self):
        assert (self.gamma * (self.gamma**2 + 3 * self.gamma + 4)) / (
            ((2 + self.gamma) ** 2) * (4 + 4 * self.gamma)
        ) > 0, "A2 adjusted for the micro foundation model."

    def _check_assumption_three(self):
        assert (
            self._gamma_assumption_three > self.gamma
        ), "A3 adjusted for the micro foundation model."

    def _check_assumption_four(self):
        assert (
            self._gamma_assumption_four > self.gamma
        ), "A4 adjusted for the micro foundation model."

    def _check_assumption_five(self):
        assert (
            self.success_probability / ((2 + self.gamma) ** 2) - self.development_costs
            < self.private_benefit
            < self.development_costs
        ), "A5 adjusted for the micro foundation model."

    @property
    def gamma(self) -> float:
        """
        Degree of substitutability of the product of the start-up and the existing product of the incumbent.
        """
        return self._gamma

    @property
    def _gamma_assumption_three(self) -> float:
        return ((self.success_probability / self.development_costs) ** (1 / 2)) - 2

    @property
    def _gamma_assumption_four(self) -> float:
        return (3 * self.success_probability - 8 * self.development_costs) / (
            8 * self.development_costs + 3 * self.success_probability
        )

    def is_laissez_faire_optimal(self) -> bool:
        """
        In this model a laissez-faire merger policy is never optimal.
        """
        return False

    def is_intermediate_optimal(self) -> bool:
        """
        Returns whether an intermediate merger policy (late takeover allowed) is optimal.

        An intermediate merger policy (late takeovers allowed) is optimal, if:
        1. The investment is sufficiently large.
        2. The degree of substitutability is moderate.
        3. Detrimental effect of less intense product market competition is dominated by the benefit of making it more
        likely that the innovation is commercialised (Condition 6 not satisfied).

        Returns
        -------
        True
            If an intermediate merger policy (late takeover allowed) is optimal.
        """
        return (
            self.is_intermediate_policy_feasible()
            and not self.is_competition_effect_dominating()
        )

    def is_strict_optimal(self) -> bool:
        return not self.is_intermediate_optimal()

    def is_intermediate_policy_feasible(self) -> bool:
        """
        Returns whether an intermediate (with late takeovers) merger policy is feasible.

        This implies, that the investment costs are sufficiently high and the degree of substitutability is moderate.

        Returns
        -------
        True
            If an intermediate policy is feasible.
        """
        return (
            (
                -5 * (self.success_probability**3)
                + 64 * (self.development_costs**3) * (3 + self.success_probability)
                + 12
                * self.development_costs
                * (self.success_probability**2)
                * (3 * self.success_probability - 1)
                + 16
                * (self.development_costs**2)
                * self.success_probability
                * (5 + 6 * self.success_probability)
            )
            / (
                8
                * self.success_probability
                * ((4 * self.development_costs + 3 * self.success_probability) ** 2)
            )
        ) > 0


class PerfectInformation(Base.OptimalMergerPolicy):
    """
    Assume the incumbent knows the realisation of the start-up’s resources when it bids at t = 1(a) and the AA also
    knows it when it reviews the merger proposal. We maintain the assumption that, when it establishes the standard for
    merger policy at t = 0, the AA only knows the distribution of A

    See section 8.5 of Fumagalli et al. (2020).
    """

    def _check_merger_policy(self):
        super(PerfectInformation, self)._check_merger_policy()
        if (
            self.merger_policy
            is Types.MergerPolicies.Intermediate_late_takeover_prohibited
        ):
            raise Exceptions.MergerPolicyNotAvailable(
                "This merger policy is not available in this model"
            )

    def _solve_game_strict_merger_policy(self) -> None:
        assert self.merger_policy is Types.MergerPolicies.Strict
        if (
            self.is_startup_credit_rationed
            and not self.is_incumbent_expected_to_shelve()
        ):
            self._set_takeovers(early_takeover=Types.Takeover.Separating)
        else:
            self._set_takeovers(
                early_takeover=Types.Takeover.No, late_takeover=Types.Takeover.No
            )

    def _solve_game_laissez_faire(self) -> None:
        assert self.merger_policy is Types.MergerPolicies.Laissez_faire
        if self.is_startup_credit_rationed and self.is_incumbent_expected_to_shelve():
            self._set_takeovers(
                early_takeover=Types.Takeover.No, late_takeover=Types.Takeover.No
            )
        else:
            if self.is_startup_credit_rationed:
                self._set_takeovers(early_takeover=Types.Takeover.Separating)
            else:
                self._set_takeovers(early_takeover=Types.Takeover.Pooling)

    def _solve_game_late_takeover_allowed(self) -> None:
        assert (
            self.merger_policy
            is Types.MergerPolicies.Intermediate_late_takeover_allowed
        )
        if self.is_incumbent_expected_to_shelve():
            if self.is_startup_credit_rationed or not self.development_success:
                self._set_takeovers(
                    early_takeover=Types.Takeover.No, late_takeover=Types.Takeover.No
                )
            else:
                self._set_takeovers(late_takeover=Types.Takeover.Pooling)
        else:
            if self.is_startup_credit_rationed:
                self._set_takeovers(early_takeover=Types.Takeover.Separating)
            else:
                self._set_takeovers(early_takeover=Types.Takeover.Pooling)

    def is_laissez_faire_optimal(self) -> bool:
        """
        In this model a laissez-faire merger policy is never optimal.
        """
        return False

    def is_intermediate_optimal(self) -> bool:
        """
        Returns whether an intermediate merger policy (late takeover allowed) is optimal.

        An intermediate merger policy (late takeovers allowed) is optimal, if:
        1. Incumbent is expected to shelve ($p(\\pi^M_I-\\pi^m_I) < K$).
        2. The intermediate policy is feasible.
        3. Detrimental effect of less intense product market competition is dominated by the benefit of making it more
        likely that the innovation is commercialised (Condition 6 not satisfied).

        Returns
        -------
        True
            If an intermediate merger policy (late takeover allowed) is optimal.
        """
        return (
            self.is_incumbent_expected_to_shelve()
            and not self.is_competition_effect_dominating()
            and self.is_intermediate_policy_feasible()
        )

    def is_intermediate_policy_feasible(self) -> bool:
        return (
            self.success_probability
            * (self.w_with_innovation - self.w_without_innovation)
            - self.development_costs
            >= self.w_duopoly - self.w_with_innovation
        )


class EquityContract(Base.OptimalMergerPolicy):
    """
    Aan equity contract gives rise to different results in the financial contracting game. With equity, when the
    incumbent acquires the start-up in $t = 2$, it pays the investors and the entrepreneur. Going backwards, the
    investors do not expect an increase in the pledgeable income, and there is no relaxation of financial constraints,
    as much as under the strict merger policy. It follows that under the laissez-faire or the intermediate policy the
    start-up will prefer debt to equity.

    See section 8.4 of Fumagalli et al. (2020).
    """

    @property
    def asset_threshold_late_takeover(self) -> float:
        return self.asset_threshold

    def does_startup_prefer_debt(self) -> bool:
        """
        Returns whether the start-up prefers debt or equity.

        The start-up prefers debt to equity, if late takeovers are allowed.

        Returns
        -------
        True
            If the start-up prefers debt to equity.
        """
        if self.merger_policy in [
            Types.MergerPolicies.Intermediate_late_takeover_allowed,
            Types.MergerPolicies.Laissez_faire,
        ]:
            return True
        return False

    def is_intermediate_optimal(self) -> bool:
        """
        In this model an intermediate merger policy is never optimal.
        """
        return False

    def is_laissez_faire_optimal(self) -> bool:
        """
        In this model a laissez-faire merger policy is never optimal.
        """
        return False
