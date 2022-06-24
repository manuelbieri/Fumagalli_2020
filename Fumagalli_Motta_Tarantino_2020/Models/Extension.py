import Fumagalli_Motta_Tarantino_2020.Models.Types as Types
import Fumagalli_Motta_Tarantino_2020.Models.Base as Base


class ProCompetitive(Base.OptimalMergerPolicy):
    """
    Relaxes the assumption (A4), that the innovation of the start-up is always welfare beneficial. Instead, the
    innovation is only welfare beneficial if the start-up develops and markets the innovation. In contrast, owned by the
    incumbent, the innovation reduces the total welfare. This is implying a pure positive effect of the innovation on
    competition.
    """

    def __init__(self, consumer_surplus_without_innovation: float = 0.3, **kwargs):
        super(ProCompetitive, self).__init__(
            consumer_surplus_without_innovation=consumer_surplus_without_innovation,
            **kwargs
        )

    def _check_assumption_four(self):
        assert (
            self._success_probability
            * (self.w_with_innovation - self.w_without_innovation)
            < self.development_costs
            < self._success_probability * (self.w_duopoly - self.w_without_innovation)
        ), "Adjusted assumption 4 in this model"

    def _check_asset_distribution_threshold_strict(self):
        pass

    def _calculate_h0(self) -> float:
        return 0

    def _calculate_h1(self) -> float:
        return (1 - self.asset_threshold_cdf) * (
            self.success_probability * (self.w_duopoly - self.w_without_innovation)
            - self.development_costs
        )

    def _calculate_h2(self) -> float:
        return 0

    def _solve_game_strict_merger_policy(self) -> None:
        assert self.merger_policy is Types.MergerPolicies.Strict
        self._set_takeovers(
            early_takeover=Types.Takeover.No, late_takeover=Types.Takeover.No
        )

    def _solve_game_late_takeover_prohibited(self) -> None:
        if (
            self.asset_threshold_cdf
            < self.asset_distribution_threshold_unprofitable_without_late_takeover
        ):
            self._set_takeovers(early_takeover=Types.Takeover.Pooling)
        else:
            self._set_takeovers(
                early_takeover=Types.Takeover.No, late_takeover=Types.Takeover.No
            )

    def _solve_game_late_takeover_allowed(self) -> None:
        if (
            self.asset_threshold_late_takeover_cdf
            < self.asset_distribution_threshold_with_late_takeover
        ):
            self._set_takeovers(early_takeover=Types.Takeover.Pooling)
        else:
            if self.is_startup_credit_rationed:
                self._set_takeovers(
                    early_takeover=Types.Takeover.No,
                    late_takeover=Types.Takeover.No,
                )
            else:
                if self.development_success:
                    self._set_takeovers(late_takeover=Types.Takeover.Pooling)
                else:
                    self._set_takeovers(
                        early_takeover=Types.Takeover.No,
                        late_takeover=Types.Takeover.No,
                    )

    def is_strict_optimal(self) -> bool:
        """
        In this model a strict merger policy is always optimal.
        """
        return True

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


class ResourceWaste(ProCompetitive):
    """
    In this model is assumed, that the innovation is never welfare beneficial, therefore a development is always a waste
    of resources regarding total welfare.
    """

    def __init__(self, consumer_surplus_duopoly=0.41, **kwargs):
        super(ResourceWaste, self).__init__(
            consumer_surplus_duopoly=consumer_surplus_duopoly, **kwargs
        )

    def _check_assumption_four(self):
        assert (
            self._success_probability
            * (self.w_with_innovation - self.w_without_innovation)
            < self._success_probability * (self.w_duopoly - self.w_without_innovation)
            < self.development_costs
        ), "Adjusted assumption 4 in this model"

    def _calculate_h1(self) -> float:
        return 0

    def _solve_game_strict_merger_policy(self) -> None:
        assert self.merger_policy is Types.MergerPolicies.Strict
        if (
            self.asset_threshold_cdf
            < self.asset_distribution_threshold_unprofitable_without_late_takeover
        ):
            self._set_takeovers(early_takeover=Types.Takeover.Pooling)
        else:
            self._set_takeovers(
                early_takeover=Types.Takeover.No, late_takeover=Types.Takeover.No
            )

    def is_strict_optimal(self) -> bool:
        """
        In this model is a strict merger policy never optimal
        """
        return False

    def is_intermediate_optimal(self) -> bool:
        """
        Returns whether the intermediate (WITHOUT late takeovers) merger policy is optimal.

        The intermediate (WITHOUT late takeovers) merger is optimal, if a laissez-faire merger policy is not optimal.

        Returns
        -------
        True
            If the intermediate (WITHOUT late takeovers) merger policy is optimal.
        """
        return not self.is_laissez_faire_optimal()

    @staticmethod
    def _get_intermediate_optimal_candidate() -> Types.MergerPolicies:
        return Types.MergerPolicies.Intermediate_late_takeover_prohibited

    def is_laissez_faire_optimal(self) -> bool:
        """
        Returns whether a laissez-faire policy is optimal.

        A laissez-faire policy (that authorises any takeover) is optimal, if:
        1. Financial imperfections are not severe ($F(\\bar{A}^T)<\\Phi^T(\\cdot)$).

        Or as well if:
        1. Financial imperfections are always severe ($F(\\bar{A}^T)\\ge\\Phi^T(\\cdot)$ and
        $F(\\bar{A})\\ge\\Phi(\\cdot)$).
        2. Detrimental effect of less intense product market competition is dominated by the benefit of making it more
        likely that the innovation is commercialised (Condition 6 not satisfied).

        Returns
        -------
        True
            If a laissez-faire merger policy is optimal.
        """
        return not self.is_financial_imperfection_severe() or (
            self.is_financial_imperfection_severe()
            and self.is_financial_imperfection_severe_without_late_takeover()
            and not self.is_competition_effect_dominating()
        )

    def is_financial_imperfection_severe_without_late_takeover(self):
        return (
            self.asset_threshold_cdf
            > self.asset_distribution_threshold_unprofitable_without_late_takeover
        )
