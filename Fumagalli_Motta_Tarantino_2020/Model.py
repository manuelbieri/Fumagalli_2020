from typing import Literal, Dict, Optional

import scipy.stats


class BaseModel:
    """
    There are three players in our game: an Antitrust Authority (AA), which at the beginning of the game decides its
    merger policy; a monopolist $\t{I}$ncumbent; and a $\t{S}$tart-up. The start-up owns a “prototype” (or project)
    that, if developed, can give rise to an innovation: for instance a substitute/higher quality product to the
    incumbent’s existing product, or a more efficient production process. The start-up does not have enough own
    resources to develop the project. It has two options: it can either obtain additional funds from competitive
    capital markets, or sell out to the incumbent. The incumbent will have to decide whether and when it wants to
    acquire the start-up (and if it does so before product development, it has to decide whether to develop the
    prototype or shelve it), conditional on the AA’s approval of the acquisition. We assume that the takeover
    involves a negligible but positive transaction cost. The AA commits at the beginning of the game to a merger
    policy, in the form of a maximum threshold of “harm”, that it is ready to tolerate. Harm from a proposed merger
    consists of the difference between the expected welfare levels if the merger goes ahead, and in the counterfactual
    where it does not take place (derived of course by correctly anticipating the continuation equilibrium of the
    game). A proposed merger will be prohibited only if the tolerated harm level H is lower than the expected harm
    from the merger, if any.

    Timing of the game:

    | Time | Action                                                                                                                                                 |
    |------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
    | 0    | The AA commits to the standard for merger approval, $\\bar{H}$.                                                                                        |
    | 1(a) | $\t{I}$ can make a takeover offer to $\t{S}$, which can accept or reject.                                                                              |
    | 1(b) | The AA approves or blocks the takeover proposal.                                                                                                       |
    | 1(c) | The firm ($\t{I}$ or $\t{S}$) that owns the prototype decides whether to develop or shelve it.                                                         |
    | 1(d) | The owner of the prototype engages in financial contracting (if needed). After that, uncertainty about the success or failure of the project resolves. |
    | 2(a) | $\t{I}$ can make a take-it-or-leave-it offer to $\t{S}$ (if it did not already buy it at t = 1, and if the development of the project was successful). |
    | 2(b) | The AA approves or blocks the takeover proposal.                                                                                                       |
    | 3    | Active firms sell in the product market, payoffs are realised and contracts are honored.
    """

    def __init__(
        self,
        tolerated_level_of_harm: float = 0,
        development_costs: float = 0.1,
        startup_assets: float = 0.05,
        success_probability: float = 0.7,
        development_success: bool = True,
        private_benefit: float = 0.05,
        consumer_surplus_without_innovation: float = 0.2,
        incumbent_profit_without_innovation: float = 0.4,
        consumer_surplus_duopoly: float = 0.5,
        incumbent_profit_duopoly: float = 0.2,
        startup_profit_duopoly: float = 0.2,
        consumer_surplus_with_innovation: float = 0.3,
        incumbent_profit_with_innovation: float = 0.5,
    ):
        """
        Initializes a valid base model according to the assumptions given in the paper.

        The following assumptions have to be met:

        | Condition                    | Remark                                                                                                                                                                                                                                                                                                                                                        | Page (Assumption) |
        |------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
        | $\\bar{H} \\ge 0$            | The tolerated level of harm has to be bigger than 0.                                                                                                                                                                                                                                                                                                          | p.6               |
        | $p \\in (0,1]$               | Probability that the prototype is developed successfully depends on the non-contractible effort exerted by the entrepreneur of the firm that owns the project. In case of no effort the project fails for sure, but the entrepreneur obtains a positive private benefit. In case of failure the project yields no profit.                                     | p.8               |
        | $B>0$                        | Private benefit of the entrepreneur in case of failure.                                                                                                                                                                                                                                                                                                       | p.8               |
        | $A \\in (0,K)$               | The startup does not hold sufficient assets at the beginning to cover the costs.                                                                                                                                                                                                                                                                              | p.8               |
        | $\\pi^m_I>\\pi^d_I$          | Profit of the incumbent has to be bigger without the innovation than in the duopoly.                                                                                                                                                                                                                                                                          | p.7               |
        | $\\pi^M_I>\\pi^m_I$          | Industry profits are higher with a multi-product monopolist than a single product monopolist (otherwise, the incumbent would always shelve).                                                                                                                                                                                                                                                                 | p.7               |
        | $CS^M \\ge CS^m$             | Consumer surplus with the innovation has to weakly bigger than without the innovation (consumers like variety).                                                                                                                                                                                                                                                                        | p.7               |
        | $\\pi^M_I>\\pi^d_I+\\pi^d_S$ | Industry profits are higher under monopoly than under duopoly. If this assumption did not hold, the takeover would not take place.                                                                                                                                                                                                                            | p.7 (A1)          |
        | $\\pi^d_S>\\pi^M_I-\\pi^m_I$ | An incumbent has less incentive to innovate (in a new/better product or a more efficient production process) than a potential entrant because the innovation would cannibalise the incumbent’s current profits. (Corresponds to Arrow's replacement effect)                                                                                                   | p.7 (A2)          |
        | $p\\pi^d_S>K$                | In case of effort it is efficient to develop the prototype, i.e., development has a positive net present value (NPV) for the start-up                                                                                                                                                                                                                         | p.8 (A3)          |
        | $p(W^M-W^m)>K$               | The development of the project is not only privately beneficial for the start-up, but also for society as a whole, whether undertaken by the incumbent or the start-up (implies $\\;p(W^d-W^m)>K\\;$).                                                                                                                                                                                       | p.8 (A4)          |
        | $B-K<0$$B-(p\\pi^d_S-K)>0$   | The first inequality implies that if S shirks the project has negative value; thus, no financial contract could be signed unless the startup makes effort. The second implies that the start-up may be financially constrained, that is, it may hold insufficient assets to fund the development of the prototype even though the project has a positive NPV. | p.8 (A5)          |

        Parameters
        ----------
        tolerated_level_of_harm : float
            ($\\bar{H}$) The AA commits at the beginning of the game to a merger policy, in the form of a maximum threshold of “harm”, that it is ready to tolerate.
        development_costs : float
            ($K$) Fixed costs to invest for development.
        startup_assets : float
            ($A$) Assets of the startup at the beginning.
        success_probability : float
            ($p$) Probability of success in case of effort (otherwise the projects fails for sure).
        development_success : bool
            Decides whether an attempted development will be successful (true $\\rightarrow$ attempted development succeeds).
        private_benefit : float
            ($B$) Private benefit of the entrepreneur in case of failure.
        consumer_surplus_without_innovation : float
            ($CS^m$) Consumer surplus for the case that the innovation is not introduced by the incumbent into the market.
        incumbent_profit_without_innovation : float
            ($\\pi^m_I$) Profit of the monopolist with a single product (without innovation).
        consumer_surplus_duopoly : float
            ($CS^d$) Consumer surplus for the case that the innovation is introduced into the market and a duopoly exists.
        incumbent_profit_duopoly : float
            ($\\pi^d_I$) Profit of the incumbent in the case of a duopoly.
        startup_profit_duopoly : float
            ($\\pi^d_S$) Profit of the startup in the case of a duopoly.
        consumer_surplus_with_innovation : float
             ($CS^M$) Consumer surplus for the case that the innovation is introduced by the incumbent into the market.
        incumbent_profit_with_innovation : float
            ($\\pi^M_I$) Profit of the monopolist with multiple products (with innovation).
        """
        self._tolerated_harm = tolerated_level_of_harm
        self._development_costs = development_costs
        self._startup_assets = startup_assets
        self._success_probability = success_probability
        self._development_success = development_success
        self._private_benefit = private_benefit

        # product market payoffs (p.6ff.)
        # with innovation
        self._incumbent_profit_with_innovation = incumbent_profit_with_innovation
        self._cs_with_innovation = consumer_surplus_with_innovation

        # without innovation
        self._incumbent_profit_without_innovation = incumbent_profit_without_innovation
        self._cs_without_innovation = consumer_surplus_without_innovation

        # with duopoly
        self._startup_profit_duopoly = startup_profit_duopoly
        self._incumbent_profit_duopoly = incumbent_profit_duopoly
        self._cs_duopoly = consumer_surplus_duopoly

        # pre-conditions given for the parameters (p.6-8)
        self._check_preconditions()

        # post-condition given (p.6-8)
        self._check_postconditions()

    def _check_postconditions(self):
        assert (
            self.w_without_innovation < self.w_with_innovation < self.w_duopoly
        ), "Ranking of total welfare not valid (p.7)"
        assert (
            self._success_probability
            * (self.w_with_innovation - self.w_without_innovation)
            > self._development_costs
        ), "A4 not satisfied (p.8)"

    def _check_preconditions(self):
        # preconditions given (p.6-8)
        assert self.tolerated_harm >= 0, "Level of harm has to be bigger than 0"
        assert self.private_benefit > 0, "Private benefit has to be bigger than 0"
        assert (
            0 < self.success_probability <= 1
        ), "Success probability of development has to be between 0 and 1"
        assert (
            0 < self.startup_assets < self.development_costs
        ), "Startup has not enough assets for development"
        assert (
            self.incumbent_profit_without_innovation > self.incumbent_profit_duopoly
        ), "Profit of the incumbent has to be bigger without the innovation than in the duopoly"
        assert (
            self.incumbent_profit_with_innovation
            > self.incumbent_profit_without_innovation
        ), "Profit of the incumbent has to be bigger with the innovation than without the innovation"
        assert (
            self.cs_with_innovation >= self.cs_without_innovation
        ), "Consumer surplus with the innovation has to weakly bigger than without the innovation"
        assert (
            self.incumbent_profit_with_innovation
            > self.incumbent_profit_duopoly + self.startup_profit_duopoly
        ), "A1 not satisfied (p.7)"
        assert (
            self.startup_profit_duopoly
            > self.incumbent_profit_with_innovation
            - self.incumbent_profit_without_innovation
        ), "A2 not satisfied (p.7)"
        assert (
            self.success_probability * self.startup_profit_duopoly
            > self._development_costs
        ), "A3 not satisfied (p.8)"
        assert (
            self.private_benefit - self.development_costs
            < 0
            < self.private_benefit
            - (
                self.success_probability * self._startup_profit_duopoly
                - self.development_costs
            )
        ), "A5 not satisfied (p.8)"

    @property
    def tolerated_harm(self) -> float:
        """
        ($\\bar{H}$) The AA commits at the beginning of the game to a merger policy, in the form of a maximum threshold of “harm”, that it is ready to tolerate.
        """
        return self._tolerated_harm

    @property
    def development_costs(self) -> float:
        """
        ($K$) Fixed costs to invest for development.
        """
        return self._development_costs

    @property
    def startup_assets(self) -> float:
        """
        ($A$) Assets of the startup at the beginning.
        """
        return self._startup_assets

    @property
    def success_probability(self) -> float:
        """
        ($p$) Probability of success in case of effort (otherwise the projects fails for sure).
        """
        return self._success_probability

    @property
    def development_success(self) -> bool:
        """
        Decides whether an attempted development will be successful.

        If true, every attempted development will be successful.
        """
        return self._development_success

    @property
    def private_benefit(self) -> float:
        """
        ($B$) Private benefit of the entrepreneur in case of failure.
        """
        return self._private_benefit

    @property
    def incumbent_profit_with_innovation(self):
        """
        ($\\pi^M_I$) Profit of the monopolist with multiple products (with innovation).
        """
        return self._incumbent_profit_with_innovation

    @property
    def cs_with_innovation(self) -> float:
        """
        ($CS^M$) Consumer surplus for the case that the innovation is introduced by the incumbent into the market.
        """
        return self._cs_with_innovation

    @property
    def w_with_innovation(self) -> float:
        """
        ($W^M$) Total welfare for the case that the innovation is introduced by the incumbent into the market.
        """
        return self._cs_with_innovation + self._incumbent_profit_with_innovation

    @property
    def incumbent_profit_without_innovation(self) -> float:
        """
        ($\\pi^m_I$) Profit of the monopolist with a single product (without innovation).
        """
        return self._incumbent_profit_without_innovation

    @property
    def cs_without_innovation(self) -> float:
        """
        ($CS^m$) Consumer surplus for the case that the innovation is not introduced by the incumbent into the market.
        """
        return self._cs_without_innovation

    @property
    def w_without_innovation(self) -> float:
        """
        ($W^m$) Total welfare for the case that the innovation is not introduced by the incumbent into the market.
        """
        return self._cs_without_innovation + self._incumbent_profit_without_innovation

    @property
    def startup_profit_duopoly(self) -> float:
        """
        ($\\pi^d_S$) Profit of the startup in the case of a duopoly.
        """
        return self._startup_profit_duopoly

    @property
    def incumbent_profit_duopoly(self) -> float:
        """
        ($\\pi^d_I$) Profit of the incumbent in the case of a duopoly.
        """
        return self._incumbent_profit_duopoly

    @property
    def cs_duopoly(self) -> float:
        """
        ($CS^d$) Consumer surplus for the case that the innovation is introduced into the market and a duopoly exists.
        """
        return self._cs_duopoly

    @property
    def w_duopoly(self) -> float:
        """
        ($W^d$) Total welfare for the case that the innovation is introduced into the market and a duopoly exists.
        """
        return (
            self._cs_duopoly
            + self._startup_profit_duopoly
            + self._incumbent_profit_duopoly
        )


class MergerPolicyModel(BaseModel):
    """
    In this class all merger policies and their respective outcomes are considered.

    Available merger policies are:
    - Strict: The AA authorises only takeovers that, at the moment in which they are reviewed, are expected to increase total welfare.
    - Intermediate (late takeover prohibited): The AA blocks late takeovers, but is more lenient with early takeovers.
    - Intermediate (late takeover allowed): The AA authorises late takeovers, but is stricter with early takeovers.
    - Laissez-faire: The intervention threshold of the AA is so high that any acquisition would be allowed.
    """

    def __init__(self, **kwargs):
        """
        Takes the same arguments as BaseModel.__init__.
        """
        super(MergerPolicyModel, self).__init__(**kwargs)
        self._probability_credit_constrained_default: float = 0
        self._probability_credit_constrained_merger_policy: float = 0

        self._early_bid_attempt: Optional[Literal["No", "Separating", "Pooling"]] = None
        self._late_bid_attempt: Optional[Literal["No", "Separating", "Pooling"]] = None
        self._early_takeover: Optional[bool] = None
        self._late_takeover: Optional[bool] = None

        self._check_asset_distribution_thresholds()
        self._solve_game()

    def _check_asset_distribution_thresholds(self) -> None:
        assert (
            0 < self.asset_distribution_threshold < 1
        ), "Violates A.2 (has to be between 0 and 1)"
        if self.merger_policy == "Strict":
            assert (
                0 < self.asset_distribution_threshold_strict < 1
            ), "Violates Condition 2 (has to be between 0 and 1)"
        elif (
            self.merger_policy == "Intermediate (late takeover prohibited)"
            and self.is_incumbent_expected_to_shelve()
        ):
            assert (
                0 <= self.asset_distribution_threshold_intermediate < 1
            ), "Violates Condition A-3 (has to be between 0 and 1)"
        elif (
            self.merger_policy == "Laissez-faire"
            and self.is_incumbent_expected_to_shelve()
        ):
            assert (
                0 < self.asset_distribution_threshold_laissez_faire < 1
            ), "Violates Condition 4 (has to be between 0 and 1)"

    @property
    def merger_policy(
        self,
    ) -> Literal[
        "Strict",
        "Intermediate (late takeover prohibited)",
        "Intermediate (late takeover allowed)",
        "Laissez-faire",
    ]:
        """
        Returns the merger policy used to determine the outcome.
        """
        if self.tolerated_harm <= self._calculate_h0():
            return "Strict"
        if self.tolerated_harm < self._calculate_h1():
            return "Intermediate (late takeover prohibited)"
        if self.tolerated_harm < self._calculate_h2():
            return "Intermediate (late takeover allowed)"
        return "Laissez-faire"

    @property
    def asset_threshold(self) -> float:
        """
        Threshold level $\\bar{A} = B - (\\pi^d_S - K)$
        """
        return self.private_benefit - (
            self.success_probability * self.startup_profit_duopoly
            - self.development_costs
        )

    @property
    def asset_threshold_cdf(self) -> float:
        """
        Returns the value of the continuous distribution function for the asset threshold.
        """
        return MergerPolicyModel._get_cdf_value(self.asset_threshold)

    @property
    def asset_threshold_late_takeover(self) -> float:
        """
        The prospect that the start-up will be acquired at $t = 2$ alleviates financial constraints: there exists a
        threshold level $\\bar{A}^T = B - (\\pi_I^M - K)$
        """
        return self.private_benefit - (
            self.success_probability * self.incumbent_profit_with_innovation
            - self.development_costs
        )

    @property
    def asset_threshold_laissez_faire_cdf(self) -> float:
        """
        Returns the value of the continuous distribution function for the asset threshold under laissez-faire.
        """
        return MergerPolicyModel._get_cdf_value(self.asset_threshold_late_takeover)

    @property
    def get_early_bidding_type(self) -> Literal["No", "Separating", "Pooling"]:
        """
        Returns the bidding attempt of the incumbent at $t = 1$.

        Possible options of an actual attempt:
        - Pooling: The incumbent offers a high takeover price such that a start-up would always accept, irrespective of the amount of own assets.
        - Separating: The incumbent offers a low takeover price targeting only the credit-rationed start-ups.

        Otherwise, the option 'No' is returned.
        """
        assert self._early_bid_attempt is not None
        return self._early_bid_attempt

    @property
    def get_late_bidding_type(self) -> Literal["No", "Separating", "Pooling"]:
        """
        Returns the bidding attempt of the incumbent at $t = 2$.

        Possible options of an actual attempt:
        - 'Pooling': The incumbent offers a high takeover price such that a start-up would always accept, irrespective of the amount of own assets.
        - 'Separating': The incumbent offers a low takeover price targeting only the credit-rationed start-ups.

        Otherwise, the option 'No' is returned.
        """
        assert self._late_bid_attempt is not None
        return self._late_bid_attempt

    @property
    def is_early_takeover(self) -> bool:
        """
        Returns whether the start-up is acquired by the incumbent at $t=1$.

        Returns
        -------
        True
            If the start-up is acquired by the incumbent at $t=1$.
        """
        assert self._early_takeover is not None
        return self._early_takeover

    @property
    def is_late_takeover(self) -> bool:
        """
        Returns whether the start-up is acquired by the incumbent at $t=2$.

        Returns
        -------
        True
            If the start-up is acquired by the incumbent at $t=2$.
        """
        assert self._late_takeover is not None
        return self._late_takeover

    @property
    def is_owner_investing(self) -> bool:
        """
        A start-up that expects external investors to deny financing will not undertake the investment. Conversely, the incumbent
        has the financial ability to invest, but it does not always have the incentive to do so. Indeed, the innovation
        increases the incumbent’s profits less than the (unconstrained) start-up’s. (This result follows directly from
        the Arrow’s replacement effect) The increase in the incumbent’s profits may not be large enough to cover the investment
        cost. When this is the case, the incumbent will shelve the project and the acquisition turns out to be a killer acquisition.

        Investment decision under the strict merger policy:
        - An unconstrained start-up always invests in the development of the prototype.
        - The incumbent invests if (and only if): $p*(\\pi^M_I-\\pi^m_I) \\ge K$

        Returns
        -------
        True
            If the owner of the innovation at $t=1$ invests in the project, instead of shelving.
        """
        assert self.is_startup_credit_rationed is not None
        assert self.is_early_takeover is not None
        if (not self.is_startup_credit_rationed and not self.is_early_takeover) or (
            not self.is_incumbent_expected_to_shelve() and self.is_early_takeover
        ):
            return True
        return False

    @property
    def is_development_successful(self) -> bool:
        """
        Returns whether the development was successful or not.

        The following two conditions have to be satisfied:
        - The owner of the product at $t=1$ has to invest in the development
        - The development success variable has to be set to True (attempted development always successful).

        Returns
        -------
        True
            If both conditions are met.
        """
        assert self.is_owner_investing is not None
        return self.is_owner_investing and self._development_success

    @property
    def is_startup_credit_rationed(self) -> bool:
        """
        If no takeover took place at t = 1(b), a start-up that decided to develop the project searches for funding at $t = 1(d)$.

        Strict and Intermediate (late takeover prohibited):
        - $A < \\bar{A}$, the start-up is credit-rationed and cannot invest.
        - $A \\ge \\bar{A}$, the start-up obtains external funding.

        Laissez-Faire and Intermediate (late takeover allowed): $$
        - $A < \\bar{A}^T$, the start-up is credit-rationed and cannot invest.
        - $A \\ge \\bar{A}^T$, the start-up obtains external funding.

        Returns
        -------
        True
            If the start-up is credit rationed.
        """
        # financial contracting (chapter 3.2)
        if self.merger_policy in ["Strict", "Intermediate (late takeover prohibited)"]:
            if self.startup_assets < self.asset_threshold:
                return True
            return False
        if self.startup_assets < self.asset_threshold_late_takeover:
            return True
        return False

    @property
    def asset_distribution_threshold_strict(self) -> float:
        """
        Threshold defined in Lemma 3 :$\\;\\Gamma(\\cdot)=\\frac{p(W^d-W^M)}{p(W^d-W^m)-K}$
        """
        return (
            self.success_probability * (self.w_duopoly - self.w_with_innovation)
        ) / (
            self.success_probability * (self.w_duopoly - self.w_without_innovation)
            - self.development_costs
        )

    @property
    def asset_distribution_threshold(self) -> float:
        """
        Threshold defined in Condition 3 :$\\;\\Phi(\\cdot)=\\frac{p(\\pi^M_I-\\pi^d_I-\\pi^d_S)}{p(\\pi^M_I-\\pi^d_I)-K}$
        """
        return (
            self.success_probability
            * (
                self.incumbent_profit_with_innovation
                - self.incumbent_profit_duopoly
                - self.startup_profit_duopoly
            )
        ) / (
            self.success_probability
            * (self.incumbent_profit_with_innovation - self.incumbent_profit_duopoly)
            - self.development_costs
        )

    @property
    def asset_distribution_threshold_laissez_faire(self) -> float:
        """
        Threshold defined in Condition 4 :$\\;\\Phi^T(\\cdot)=\\frac{p(\\pi^m_I-\\pi^M_I)+K}{p(\\pi^m_I+\\pi^d_S-\\pi^M_I)}$
        """
        return (
            self.success_probability
            * (
                self.incumbent_profit_without_innovation
                - self.incumbent_profit_with_innovation
            )
            + self.development_costs
        ) / (
            self.success_probability
            * (
                self.incumbent_profit_without_innovation
                + self.startup_profit_duopoly
                - self.incumbent_profit_with_innovation
            )
        )

    @property
    def asset_distribution_threshold_intermediate(self) -> float:
        """
        Threshold defined in A-3 :$\\;\\Phi^{\\prime}(\\cdot)=\\frac{p(\\pi^m_I-\\pi^d_I-\\pi^d_S)+K}{p(\\pi^m_I+\\pi^d_I)}$
        """
        return (
            self.success_probability
            * (
                self.incumbent_profit_without_innovation
                - self.incumbent_profit_duopoly
                - self.startup_profit_duopoly
            )
            + self.development_costs
        ) / (
            self.success_probability
            * (self.incumbent_profit_without_innovation - self.incumbent_profit_duopoly)
        )

    @staticmethod
    def _get_cdf_value(value: float) -> float:
        return float(scipy.stats.norm.cdf(value))

    def is_incumbent_expected_to_shelve(self) -> bool:
        """
        Returns whether the incumbent is expected to shelve, whenever it acquires the entrant (Condition 1).

        - True (expected to shelve): $p*(\\pi^M_I-\\pi^m_I) < K$

        - False (not expected to shelve): $p*(\\pi^M_I-\\pi^m_I) \\ge K$

        """
        return self.incumbent_expected_additional_profit_from_innovation() < 0

    def incumbent_expected_additional_profit_from_innovation(self) -> float:
        """
        Returns the additional expected profit for the incumbent, if it does not shelve the product after an acquisition.

        $ Expected \\; additional \\; profit = p*(\\pi^M_I-\\pi^m_I)-K$
        """
        return (
            self.success_probability
            * (
                self.incumbent_profit_with_innovation
                - self.incumbent_profit_without_innovation
            )
            - self.development_costs
        )

    def _calculate_h0(self) -> float:
        return max(
            (1 - self.asset_threshold_cdf)
            * (self.success_probability * (self.w_duopoly - self.w_with_innovation))
            - self.asset_threshold_cdf
            * (
                self.success_probability
                * (self.w_with_innovation - self.w_without_innovation)
                - self.development_costs
            ),
            0,
        )

    def _calculate_h1(self) -> float:
        return (1 - self.asset_threshold_cdf) * (
            self.success_probability * (self.w_duopoly - self.w_without_innovation)
            - self.development_costs
        )

    def _calculate_h2(self) -> float:
        return max(
            self.w_duopoly - self.w_with_innovation,
            (1 - self.asset_threshold_laissez_faire_cdf)
            * (
                self.success_probability
                * (self.w_with_innovation - self.w_without_innovation)
                - self.development_costs
            ),
        )

    def _solve_game(self):
        """
        Solves the game according to the policies given by the thresholds for tolerated harm.

        The levels of tolerated harm are defined in A.4 (p.36ff.).
        """
        if self.merger_policy == "Strict":
            self._solve_game_strict_merger_policy()
        elif self.merger_policy == "Intermediate (late takeover prohibited)":
            self._solve_game_late_takeover_prohibited()
        elif self.merger_policy == "Intermediate (late takeover allowed)":
            self._solve_game_late_takeover_allowed()
        else:
            self._solve_game_laissez_faire()

    def _solve_game_laissez_faire(self):
        if self.is_incumbent_expected_to_shelve():
            if (
                self.asset_threshold_laissez_faire_cdf
                >= self.asset_distribution_threshold_laissez_faire
            ):
                if not self.is_startup_credit_rationed and self.development_success:
                    self._set_takeovers(late_takeover="Pooling")
                else:
                    self._set_takeovers(early_takeover="No", late_takeover="No")
            else:
                self._set_takeovers(early_takeover="Pooling")
        else:
            if self.is_startup_credit_rationed:
                self._set_takeovers(early_takeover="Separating")
            else:
                if self.development_success:
                    self._set_takeovers(
                        early_takeover="Separating",
                        early_takeover_accepted=False,
                        late_takeover="Pooling",
                    )
                else:
                    self._set_takeovers(
                        early_takeover="Separating",
                        early_takeover_accepted=False,
                        late_takeover="No",
                    )

    def _solve_game_late_takeover_allowed(self):
        if self.is_incumbent_expected_to_shelve():
            if not self.is_startup_credit_rationed and self.development_success:
                self._set_takeovers(late_takeover="Pooling")
            else:
                self._set_takeovers(early_takeover="No", late_takeover="No")
        else:
            if self.is_startup_credit_rationed:
                self._set_takeovers(early_takeover="Separating")
            else:
                if self.development_success:
                    self._set_takeovers(
                        early_takeover="Separating",
                        early_takeover_accepted=False,
                        late_takeover="Pooling",
                    )
                else:
                    self._set_takeovers(
                        early_takeover="Separating", early_takeover_accepted=False
                    )

    def _solve_game_late_takeover_prohibited(self):
        if self.is_incumbent_expected_to_shelve():
            if (
                self.asset_threshold_cdf
                >= self.asset_distribution_threshold_intermediate
            ):
                self._set_takeovers(early_takeover="No", late_takeover="No")
            else:
                self._set_takeovers(early_takeover="Pooling")
        else:
            if self.asset_threshold_cdf >= self.asset_distribution_threshold:
                if self.is_startup_credit_rationed:
                    self._set_takeovers(early_takeover="Separating")
                else:
                    self._set_takeovers(
                        early_takeover="Separating", early_takeover_accepted=False
                    )
            else:
                self._set_takeovers("Pooling")

    def _solve_game_strict_merger_policy(self):
        # decision of the AA and the startup (chapter 3.4.1)
        # takeover bid of the incumbent (chapter 3.4.2)
        if self.is_incumbent_expected_to_shelve():
            self._set_takeovers(early_takeover="No", late_takeover="No")
        else:
            if (
                self.asset_distribution_threshold_strict
                < self.asset_threshold_cdf
                < max(
                    self.asset_distribution_threshold,
                    self.asset_distribution_threshold_strict,
                )
            ):
                self._set_takeovers(early_takeover="Pooling")
            else:
                if self.is_startup_credit_rationed:
                    self._set_takeovers(early_takeover="Separating")
                else:
                    self._set_takeovers(
                        early_takeover="Separating", early_takeover_accepted=False
                    )

    def _set_takeovers(
        self,
        early_takeover: Literal["No", "Separating", "Pooling"] = "No",
        late_takeover: Literal["No", "Separating", "Pooling"] = "No",
        early_takeover_accepted=True,
        late_takeover_accepted=True,
    ) -> None:
        assert self._early_bid_attempt is None and self._early_takeover is None
        assert self._late_bid_attempt is None and self._late_takeover is None
        assert not (
            early_takeover in ["Separating", "Pooling"]
            and early_takeover_accepted
            and late_takeover in ["Separating", "Pooling"]
            and late_takeover_accepted
        ), "Only one takeover can occur."
        self._early_takeover = (
            False if early_takeover == "No" or not early_takeover_accepted else True
        )
        self._early_bid_attempt = early_takeover
        self._late_takeover = (
            False if late_takeover == "No" or not late_takeover_accepted else True
        )
        self._late_bid_attempt = late_takeover

    def summary(self) -> Dict[str, any]:
        """
        Returns the calculated outcome of the model with the defined parameters.

        The resulting dictionary contains the following information (and keys):
        - 'credit_rationed' : True, if the start-up is credit rationed.
        - 'early_bidding_type' : 'No', 'Pooling' or 'Separating' -> Defines the bidding type of the incumbent at t=1.
        - 'late_bidding_type' : 'No', 'Pooling' or 'Separating' -> Defines the bidding type of the incumbent at t=2.
        - 'development_attempt' : True, if the owner (start-up or incumbent after a takeover) tries to develop the product.
        - 'development_outcome' : True, if the product is developed successfully.
        - 'early_takeover' : True, if a takeover takes place at $t=1$.
        - 'late_takeover' : True, if a takeover takes place at $t=2$.

        Returns
        -------
        Dict[str, any]
            Containing the result of the model with the defined parameters.
        """
        return {
            "credit_rationed": self.is_startup_credit_rationed,
            "early_bidding_type": self.get_early_bidding_type,
            "late_bidding_type": self.get_early_bidding_type,
            "development_attempt": self.is_owner_investing,
            "development_outcome": self.is_development_successful,
            "early_takeover": self.is_early_takeover,
            "late_takeover": self.is_late_takeover,
        }


class OptimalMergerPolicy(MergerPolicyModel):
    def __init__(self, **kwargs):
        super(OptimalMergerPolicy, self).__init__(**kwargs)

    def is_strict_beneficial_compared_to_laissez_faire(self) -> bool:
        # section 6.1
        return (
            self.success_probability * (self.w_duopoly - self.w_without_innovation)
            - self.development_costs
        ) / (
            self.success_probability
            * (self.w_with_innovation - self.w_without_innovation)
            - self.development_costs
        ) > (
            1 - self.asset_threshold_laissez_faire_cdf
        ) / (
            1 - self.asset_threshold_cdf
        )

    def is_strict_beneficial_compared_to_intermediate(self) -> bool:
        # section 6.2
        return self.is_strict_beneficial_compared_to_laissez_faire()

    def get_optimal_merger_policy(
        self,
    ) -> Literal[
        "Strict",
        "Intermediate (late takeover prohibited)",
        "Intermediate (late takeover allowed)",
        "Laissez-faire",
    ]:
        # section 6.3
        if self.is_laissez_faire_optimal():
            return "Laissez-faire"
        if self.is_intermediate_optimal():
            return "Intermediate (late takeover allowed)"
        return "Strict"

    def is_laissez_faire_optimal(self) -> bool:
        return (
            self.is_incumbent_expected_to_shelve()
            and self.is_financial_imperfection_severe()
            and self.is_early_takeover_followed_by_shelving_optimal()
            and not self.is_strict_beneficial_compared_to_laissez_faire()
        )

    def is_intermediate_optimal(self) -> bool:
        return (
            self.is_incumbent_expected_to_shelve()
            and not self.is_early_takeover_followed_by_shelving_optimal()
            and not self.is_strict_beneficial_compared_to_intermediate()
        )

    def is_financial_imperfection_severe(self) -> bool:
        return (
            self.asset_threshold_laissez_faire_cdf
            >= self.asset_distribution_threshold_laissez_faire
        )

    def is_early_takeover_followed_by_shelving_optimal(self) -> bool:
        return (
            self.asset_threshold_laissez_faire_cdf
            >= self.threshold_approved_takeover_followed_pooling_offer()
        )

    def threshold_approved_takeover_followed_pooling_offer(self) -> float:
        return (
            self.success_probability
            * (self.w_with_innovation - self.w_without_innovation)
            - self.development_costs
            - (self.w_duopoly - self.w_with_innovation)
        ) / (
            self.success_probability
            * (self.w_with_innovation - self.w_without_innovation)
            - self.development_costs
        )
