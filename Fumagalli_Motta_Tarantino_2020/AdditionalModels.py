import Fumagalli_Motta_Tarantino_2020.Models as Models


class MicroFoundationModel(Models.OptimalMergerPolicy):
    def __init__(self, gamma=0.2, *args, **kwargs):
        assert 0 < gamma < 1, "Gamma has to be between 0 and 1."
        self._gamma = gamma
        super(MicroFoundationModel, self).__init__(*args, **kwargs)
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

    def incumbent_expected_additional_profit_from_innovation(self) -> float:
        return (self.success_probability - 4 * self.development_costs) / (
            self.success_probability + 4 * self.development_costs
        ) - self.gamma

    @property
    def asset_threshold(self) -> float:
        return (
            self.private_benefit
            + self.development_costs
            - (self.success_probability / ((2 + self.gamma) ** 2))
        )

    @property
    def asset_threshold_late_takeover_cdf(self) -> float:
        return 0

    @property
    def gamma(self) -> float:
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
        return False

    def is_intermediate_optimal(self) -> bool:
        return (
            self.is_investment_cost_sufficiently_high()
            and self.is_degree_substitutability_moderate()
            and self.is_financial_imperfection_severe()
        )

    def is_strict_optimal(self) -> bool:
        return not self.is_intermediate_optimal()

    def is_investment_cost_sufficiently_high(self) -> float:
        return (
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
        ) / (
            8
            * self.success_probability
            * ((4 * self.development_costs + 3 * self.success_probability) ** 2)
        ) > 0

    def is_degree_substitutability_moderate(self):
        gamma_inv = (
            self.incumbent_expected_additional_profit_from_innovation() + self.gamma
        )
        gamma_hat = min(self._gamma_assumption_three, self._gamma_assumption_four)
        return gamma_inv < self.gamma <= gamma_hat

    def is_financial_imperfection_severe(self) -> bool:
        return self.asset_threshold_cdf > 1 - (
            self.success_probability
            * (self.w_with_innovation - self.w_without_innovation)
            - self.development_costs
        ) / (
            self.success_probability * (self.w_duopoly - self._cs_without_innovation)
            - self.development_costs
        )
