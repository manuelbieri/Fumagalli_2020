from typing import Literal, Dict

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
        | $\\pi^M_I>\\pi^m_I$          | Industry profits are higher with a multi-product monopolist than a single product monopolist.                                                                                                                                                                                                                                                                 | p.7               |
        | $CS^M \\ge CS^m$             | Consumer surplus with the innovation has to weakly bigger than without the innovation.                                                                                                                                                                                                                                                                        | p.7               |
        | $\\pi^M_I>\\pi^d_I+\\pi^d_S$ | Industry profits are higher under monopoly than under duopoly. If this assumption did not hold, the takeover would not take place.                                                                                                                                                                                                                            | p.7 (A1)          |
        | $\\pi^d_S>\\pi^M_I-\\pi^m_I$ | An incumbent has less incentive to innovate (in a new/better product or a more efficient production process) than a potential entrant because the innovation would cannibalise the incumbent’s current profits. (Corresponds to Arrow's replacement effect)                                                                                                   | p.7 (A2)          |
        | $p\\pi^d_S>K$                | In case of effort it is efficient to develop the prototype, i.e., development has a positive net present value (NPV) for the start-up                                                                                                                                                                                                                         | p.8 (A3)          |
        | $p(W^M-W^m)>K$               | The development of the project is not only privately beneficial for the start-up, but also for society as a whole, whether undertaken by the incumbent or the start-up.                                                                                                                                                                                       | p.8 (A4)          |
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
            Decide whether a development will be successful (God mode).
        private_benefit : float
            ($B$) Private benefit of the entrepreneur in case of failure.
        consumer_surplus_without_innovation : float
            ($CS^m$) Consumer surplus for the case that the innovation is not introduced into the market.
        incumbent_profit_without_innovation : float
            ($\\pi^m_I$) Profit of the monopolist with a single product (without innovation).
        consumer_surplus_duopoly : float
            Consumer surplus for the case that the innovation is introduced into the market and a duopoly exists.
        incumbent_profit_duopoly : float
            ($\\pi^d_I$) Profit of the incumbent in the case of a duopoly.
        startup_profit_duopoly : float
            ($\\pi^d_S$) Profit of the startup in the case of a duopoly.
        consumer_surplus_with_innovation : float
             ($CS^M$) Consumer surplus for the case that the innovation is introduced into the market.
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
        self._w_with_innovation = (
            self._cs_with_innovation + self._incumbent_profit_with_innovation
        )
        # without innovation
        self._incumbent_profit_without_innovation = incumbent_profit_without_innovation
        self._cs_without_innovation = consumer_surplus_without_innovation
        self._w_without_innovation = (
            self._cs_without_innovation + self._incumbent_profit_without_innovation
        )
        # with duopoly
        self._startup_profit_duopoly = startup_profit_duopoly
        self._incumbent_profit_duopoly = incumbent_profit_duopoly
        self._cs_duopoly = consumer_surplus_duopoly
        self._w_duopoly = (
            self._cs_duopoly
            + self._startup_profit_duopoly
            + self._incumbent_profit_duopoly
        )

        # pre-conditions given for the parameters (p.6-8)
        self._check_preconditions()

        # post-condition given (p.6-8)
        self._check_post_conditions()

    def _check_post_conditions(self):
        assert (
            self._w_without_innovation < self._w_with_innovation < self._w_duopoly
        ), "Ranking of total welfare not valid (p.7)"
        assert (
            self._success_probability
            * (self._w_with_innovation - self._w_without_innovation)
            > self._development_costs
        ), "A4 not satisfied (p.8)"

    def _check_preconditions(self):
        # preconditions given (p.6-8)
        assert self._tolerated_harm >= 0, "Level of harm has to be bigger than 0"
        assert self._private_benefit > 0, "Private benefit has to be bigger than 0"
        assert (
            self._incumbent_profit_without_innovation > self._incumbent_profit_duopoly
        ), "Profit of the incumbent has to be bigger without the innovation than in the duopoly"
        assert (
            self._incumbent_profit_with_innovation
            > self._incumbent_profit_without_innovation
        ), "Profit of the incumbent has to be bigger with the innovation than without the innovation"
        assert (
            self._cs_with_innovation >= self._cs_without_innovation
        ), "Consumer surplus with the innovation has to weakly bigger than without the innovation"
        assert (
            self._incumbent_profit_with_innovation
            > self._incumbent_profit_duopoly + self._startup_profit_duopoly
        ), "A1 not satisfied (p.7)"
        assert (
            self._startup_profit_duopoly
            > self._incumbent_profit_with_innovation
            - self._incumbent_profit_without_innovation
        ), "A2 not satisfied (p.7)"
        assert (
            0 < self._success_probability <= 1
        ), "Success probability of development has to be between 0 and 1"
        assert (
            self._success_probability * self._startup_profit_duopoly
            > self._development_costs
        ), "A3 not satisfied (p.8)"
        assert (
            self._private_benefit - self._development_costs
            < 0
            < self._private_benefit
            * (
                self._success_probability * self._startup_profit_duopoly
                - self._development_costs
            )
        ), "A5 not satisfied (p.8)"
        assert (
            0 < self._startup_assets < self._development_costs
        ), "Startup has not enough assets for development"

    @property
    def tolerated_harm(self) -> float:
        return self._tolerated_harm

    @property
    def development_costs(self) -> float:
        return self._development_costs

    @property
    def startup_assets(self) -> float:
        return self._startup_assets

    @property
    def success_probability(self) -> float:
        return self._success_probability

    @property
    def development_success(self) -> bool:
        return self._development_success

    @property
    def private_benefit(self) -> float:
        return self._private_benefit

    @property
    def incumbent_profit_with_innovation(self):
        return self._incumbent_profit_with_innovation

    @property
    def cs_with_innovation(self) -> float:
        return self._cs_with_innovation

    @property
    def w_with_innovation(self) -> float:
        return self._w_with_innovation

    @property
    def incumbent_profit_without_innovation(self) -> float:
        return self._incumbent_profit_without_innovation

    @property
    def cs_without_innovation(self) -> float:
        return self._cs_without_innovation

    @property
    def w_without_innovation(self) -> float:
        return self._w_without_innovation

    @property
    def startup_profit_duopoly(self) -> float:
        return self._startup_profit_duopoly

    @property
    def incumbent_profit_duopoly(self) -> float:
        return self._incumbent_profit_duopoly

    @property
    def cs_duopoly(self) -> float:
        return self._cs_duopoly

    @property
    def w_duopoly(self) -> float:
        return self._w_duopoly


class MergerPolicyModel(BaseModel):
    def __init__(self, **kwargs):
        super(MergerPolicyModel, self).__init__(**kwargs)
        self._asset_threshold = self.private_benefit - (
            self.success_probability * self.startup_profit_duopoly
            - self.development_costs
        )
        self._asset_threshold_cdf = MergerPolicyModel._get_cdf_value(
            self.asset_threshold
        )

        self._asset_threshold_laissez_faire = self.private_benefit - (
            self.success_probability * self.incumbent_profit_with_innovation
            - self.development_costs
        )
        self._asset_threshold_laissez_faire_cdf = self._get_cdf_value(
            self.asset_threshold_laissez_faire
        )

        self._probability_credit_constrained_threshold = (
            self.success_probability
            * (self.w_duopoly - self.w_with_innovation)
            / (
                self.success_probability
                * (self.w_duopoly - self.incumbent_profit_without_innovation)
                - self.development_costs
            )
        )
        self._merger_policy: Literal[
            "Strict",
            "Intermediate (late takeover prohibited)",
            "Intermediate (late takeover allowed)",
            "Laissez-faire",
        ] = "Strict"
        self._probability_credit_constrained_default: float = 0
        self._probability_credit_constrained_merger_policy: float = 0

        self._early_bid_attempt: Literal["No", "Separating", "Pooling"] = "No"
        self._late_bid_attempt: Literal["No", "Separating", "Pooling"] = "No"
        self._owner_invests_in_development: bool = False
        self._successful_development_outcome: bool = False
        self._startup_credit_rationed: bool = False
        self._early_takeover: bool = False
        self._late_takeover: bool = False
        assert (
            0 < self._probability_credit_constrained_threshold < 1
        ), "Violates A.1 (has to be between 0 and 1)"
        self._determine_merger_policy()
        self._calculate_probability_credit_rationed()
        self._solve_game()

    def _determine_merger_policy(self):
        if self.tolerated_harm <= self._calculate_h0():
            self._merger_policy = "Strict"
        elif self.tolerated_harm < self._calculate_h1():
            self._merger_policy = "Intermediate (late takeover prohibited)"
        elif self.tolerated_harm < self._calculate_h2():
            self._merger_policy = "Intermediate (late takeover allowed)"
        else:
            self._merger_policy = "Laissez-faire"

    def _calculate_probability_credit_rationed(self) -> None:
        self._probability_credit_constrained_default = (
            self.success_probability
            * (
                self.incumbent_profit_with_innovation
                - self.incumbent_profit_duopoly
                - self.startup_profit_duopoly
            )
            / (
                self.success_probability
                * (
                    self.incumbent_profit_with_innovation
                    - self.incumbent_profit_duopoly
                )
                - self.development_costs
            )
        )
        if self.get_merger_policy == "Strict":
            self._probability_credit_constrained_merger_policy = (
                self._probability_credit_constrained_default
            )
        elif self.get_merger_policy == "Laissez-faire":
            self._probability_credit_constrained_merger_policy = (
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
        else:
            self._probability_credit_constrained_merger_policy = (
                self.success_probability
                * (
                    self.incumbent_profit_without_innovation
                    - self.incumbent_profit_duopoly
                    - self.startup_profit_duopoly
                )
                + self.development_costs
            ) / (
                self.success_probability
                * (
                    self.incumbent_profit_without_innovation
                    - self.incumbent_profit_duopoly
                )
            )

        assert (
            0 < self.probability_credit_constrained_default < 1
        ), "Violates A.2 (has to be between 0 and 1)"
        assert (
            0 < self.probability_credit_constrained_merger_policy[0] < 1
            or self.success_probability
            * (
                self.incumbent_profit_with_innovation
                - self.incumbent_profit_without_innovation
            )
            - self.development_costs
            > 0
        ), "Violates Proposition 2 (laissez-faire) or Lemma A-1 (intermediate) (has to be between 0 and 1)"
        assert (
            self.probability_credit_constrained_merger_policy[1]
            == self.get_merger_policy
        ), "Probability calculated for the wrong merger policy"

    @property
    def get_merger_policy(
        self,
    ) -> Literal[
        "Strict",
        "Intermediate (late takeover prohibited)",
        "Intermediate (late takeover allowed)",
        "Laissez-faire",
    ]:
        return self._merger_policy

    @property
    def asset_threshold(self) -> float:
        return self._asset_threshold

    @property
    def asset_threshold_laissez_faire(self) -> float:
        return self._asset_threshold_laissez_faire

    @property
    def get_early_bidding_type(self) -> Literal["No", "Separating", "Pooling"]:
        return self._early_bid_attempt

    @property
    def get_late_bidding_type(self) -> Literal["No", "Separating", "Pooling"]:
        return self._late_bid_attempt

    @property
    def is_owner_investing(self) -> bool:
        return self._owner_invests_in_development

    @property
    def is_development_successful(self) -> bool:
        return self._successful_development_outcome

    @property
    def is_startup_credit_rationed(self) -> bool:
        return self._startup_credit_rationed

    @property
    def probability_credit_constrained_threshold(self) -> float:
        return self._probability_credit_constrained_threshold

    @property
    def probability_credit_constrained_default(self) -> float:
        return self._probability_credit_constrained_default

    @property
    def probability_credit_constrained_merger_policy(
        self,
    ) -> (
        float,
        Literal[
            "Strict",
            "Intermediate (late takeover prohibited)",
            "Intermediate (late takeover allowed)",
            "Laissez-faire",
        ],
    ):
        return (
            self._probability_credit_constrained_merger_policy,
            self.get_merger_policy,
        )

    @property
    def is_early_takeover(self) -> bool:
        return self._early_takeover

    @property
    def is_late_takeover(self) -> bool:
        return self._late_takeover

    @staticmethod
    def _get_cdf_value(value: float) -> float:
        return float(scipy.stats.norm.cdf(value))

    def _calculate_h0(self) -> float:
        return max(
            (1 - self._asset_threshold_cdf)
            * (self.success_probability * (self.w_duopoly - self.w_with_innovation))
            - self._asset_threshold_cdf
            * (
                self.success_probability
                * (self.w_with_innovation - self.w_without_innovation)
                - self.development_costs
            ),
            0,
        )

    def _calculate_h1(self) -> float:
        return (1 - self._asset_threshold_cdf) * (
            self.success_probability * (self.w_duopoly - self.w_without_innovation)
            - self.development_costs
        )

    def _calculate_h2(self) -> float:
        return max(
            self.w_duopoly - self.w_with_innovation,
            (1 - self._asset_threshold_laissez_faire_cdf)
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
        if self.get_merger_policy == "Strict":
            self._solve_game_strict_merger_policy()
        elif self.get_merger_policy == "Intermediate (late takeover prohibited)":
            self._solve_game_late_takeover_prohibited()
        elif self.get_merger_policy == "Intermediate (late takeover allowed)":
            self._solve_game_late_takeover_allowed()
        else:
            self._solve_game_laissez_faire()
        self._calculate_investment_decision()

    def _solve_game_laissez_faire(self):
        self._calculate_startup_credit_rationed_laissez_faire()
        self._calculate_takeover_decision_laissez_faire()

    def _solve_game_late_takeover_allowed(self):
        self._calculate_startup_credit_rationed_late_takeover_allowed()
        self._calculate_takeover_decision_late_takeover_allowed()

    def _solve_game_late_takeover_prohibited(self):
        self._calculate_startup_credit_rationed_late_takeover_prohibited()
        self._calculate_takeover_decision_late_takeover_prohibited()

    def _solve_game_strict_merger_policy(self):
        self._calculate_startup_credit_rationed_strict_merger_policy()
        self._calculate_takeover_decision_strict_merger_policy()

    def _calculate_takeover_decision_strict_merger_policy(self):
        # decision of the AA and the startup (chapter 3.4.1)
        # takeover bid of the incumbent (chapter 3.4.2)
        if (
            self.success_probability
            * (
                self.incumbent_profit_with_innovation
                - self.incumbent_profit_without_innovation
            )
        ) >= self.development_costs:
            if (
                self.probability_credit_constrained_threshold
                < self._asset_threshold_cdf
                < max(
                    self._probability_credit_constrained_default,
                    self.probability_credit_constrained_threshold,
                )
            ):
                self._early_bid_attempt = "Pooling"
                self._early_takeover = True
            else:
                self._early_bid_attempt = "Separating"
                if self.is_startup_credit_rationed:
                    self._early_takeover = True

    def _calculate_takeover_decision_late_takeover_allowed(self):
        if (
            self.success_probability
            * (
                self.incumbent_profit_with_innovation
                - self.incumbent_profit_without_innovation
            )
            < self.development_costs
        ):
            if not self.is_startup_credit_rationed and self.development_success:
                self._late_takeover = True
                self._late_bid_attempt = "Pooling"
        else:
            self._early_bid_attempt = "Separating"
            if self.is_startup_credit_rationed:
                self._early_takeover = True
            elif self.development_success:
                self._late_bid_attempt = "Pooling"
                self._late_takeover = True

    def _calculate_takeover_decision_late_takeover_prohibited(self):
        (
            probability_credit_constrained_intermediate,
            merger_policy,
        ) = self.probability_credit_constrained_merger_policy
        assert merger_policy == "Intermediate (late takeover prohibited)"
        if (
            self.success_probability
            * (
                self.incumbent_profit_with_innovation
                - self.incumbent_profit_without_innovation
            )
            < self.development_costs
        ):
            if self._asset_threshold_cdf < probability_credit_constrained_intermediate:
                self._early_takeover = True
                self._early_bid_attempt = "Pooling"
        else:
            if self._asset_threshold_cdf >= self.probability_credit_constrained_default:
                self._early_bid_attempt = "Separating"
                if self.is_startup_credit_rationed:
                    self._early_takeover = True
            else:
                self._early_bid_attempt = "Pooling"
                self._early_takeover = True

    def _calculate_takeover_decision_laissez_faire(self):
        (
            probability_credit_constrained_laissez_faire,
            merger_policy,
        ) = self.probability_credit_constrained_merger_policy
        assert merger_policy == "Laissez-faire"
        if (
            self.success_probability
            * (
                self.incumbent_profit_with_innovation
                - self.incumbent_profit_without_innovation
            )
            < self.development_costs
        ):
            if (
                self._asset_threshold_laissez_faire_cdf
                >= probability_credit_constrained_laissez_faire
            ):
                if not self.is_startup_credit_rationed and self.development_success:
                    self._late_takeover = True
                    self._late_bid_attempt = "Pooling"
            else:
                self._early_takeover = True
                self._early_bid_attempt = "Pooling"
                self._owner_invests_in_development = False
        else:
            self._early_bid_attempt = "Separating"
            if self.is_startup_credit_rationed:
                self._early_takeover = True
            elif self.development_success:
                self._late_takeover = True
                self._late_bid_attempt = "Pooling"

    def _calculate_investment_decision(self):
        # investment decision (chapter 3.3)
        if (not self.is_startup_credit_rationed and not self.is_early_takeover) or (
            (
                self.success_probability
                * (
                    self.incumbent_profit_with_innovation
                    - self.incumbent_profit_without_innovation
                )
            )
            >= self.development_costs
            and self.is_early_takeover
        ):
            self._owner_invests_in_development = True
        self._successful_development_outcome = (
            self.is_owner_investing and self._development_success
        )

    def _calculate_startup_credit_rationed_strict_merger_policy(self):
        # financial contracting (chapter 3.2)
        if self.startup_assets < self.asset_threshold:
            self._startup_credit_rationed = True

    def _calculate_startup_credit_rationed_late_takeover_prohibited(self):
        self._calculate_startup_credit_rationed_strict_merger_policy()

    def _calculate_startup_credit_rationed_late_takeover_allowed(self):
        self._calculate_startup_credit_rationed_strict_merger_policy()

    def _calculate_startup_credit_rationed_laissez_faire(self):
        # financial contracting (chapter 4.2)
        if self.startup_assets < self.asset_threshold_laissez_faire:
            self._startup_credit_rationed = True

    def summary(self) -> Dict[str, any]:
        """
        Returns the calculated outcome of the model with the defined parameters.

        The resulting dictionary contains the following information (and keys):
        - 'credit_rationed' : True, if the start-up is credit rationed.
        - 'early_bidding_type' : 'No', 'Pooling' or 'Separating' -> Defines the bidding type of the incumbent at t=1.
        - 'late_bidding_type' : 'No', 'Pooling' or 'Separating' -> Defines the bidding type of the incumbent at t=2.
        - 'development_attempt' : True, if the owner (start-up or incumbent after a takeover) tries to develop the product.
        - 'development_outcome' : True, if the product is developed successfully.
        - 'early_takeover' : True, if a takeover takes place at t=1.
        - 'late_takeover' : True, if a takeover takes place at t=2.

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
