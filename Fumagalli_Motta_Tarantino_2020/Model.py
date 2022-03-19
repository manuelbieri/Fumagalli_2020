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
    consists of the di↵erence between the expected welfare levels if the merger goes ahead, and in the counterfactual
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
        tolerated_level_of_harm: float = 1,
        development_costs: float = 0.1,
        startup_assets: float = 0.05,
        success_probability: float = 0.75,
        private_benefit: float = 0.05,
        consumer_surplus_monopoly_without_innovation: float = 0.2,
        incumbent_profit_without_innovation: float = 0.4,
        consumer_surplus_duopoly: float = 0.5,
        incumbent_profit_duopoly: float = 0.2,
        startup_profit_duopoly: float = 0.2,
        consumer_surplus_monopoly_with_innovation: float = 0.3,
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
        private_benefit : float
            ($B$) Private benefit of the entrepreneur in case of failure.
        consumer_surplus_monopoly_without_innovation : float
            ($CS^m$) Consumer surplus for the case that the innovation is not introduced into the market.
        incumbent_profit_without_innovation : float
            ($\\pi^m_I$) Profit of the monopolist with a single product (without innovation).
        consumer_surplus_duopoly : float
            Consumer surplus for the case that the innovation is introduced into the market and a duopoly exists.
        incumbent_profit_duopoly : float
            ($\\pi^d_I$) Profit of the incumbent in the case of a duopoly.
        startup_profit_duopoly : float
            ($\\pi^d_S$) Profit of the startup in the case of a duopoly.
        consumer_surplus_monopoly_with_innovation : float
             ($CS^M$) Consumer surplus for the case that the innovation is introduced into the market.
        incumbent_profit_with_innovation : float
            ($\\pi^M_I$) Profit of the monopolist with multiple products (with innovation).
        """

        # preconditions given (p.6-8)
        assert tolerated_level_of_harm >= 0, "Level of harm has to be bigger than 0"
        assert private_benefit > 0, "Private benefit has to be bigger than 0"
        assert (
            incumbent_profit_without_innovation > incumbent_profit_duopoly
        ), "Profit of the incumbent has to be bigger without the innovation than in the duopoly"
        assert (
            incumbent_profit_with_innovation > incumbent_profit_without_innovation
        ), "Profit of the incumbent has to be bigger with the innovation than without the innovation"
        assert (
            consumer_surplus_monopoly_with_innovation >= consumer_surplus_monopoly_without_innovation
        ), "Consumer surplus with the innovation has to weakly bigger than without the innovation"
        assert (
            incumbent_profit_with_innovation > incumbent_profit_duopoly + startup_profit_duopoly
        ), "A1 not satisfied (p.7)"
        assert (
            startup_profit_duopoly > incumbent_profit_with_innovation - incumbent_profit_without_innovation
        ), "A2 not satisfied (p.7)"
        assert 0 < success_probability <= 1, "Success probability of development has to be between 0 and 1"
        assert success_probability * startup_profit_duopoly > development_costs, "A3 not satisfied (p.8)"
        assert private_benefit - development_costs < 0 and 0 < private_benefit * (
            success_probability * startup_profit_duopoly - development_costs
        ), "A5 not satisfied (p.8)"

        self._tolerated_harm = tolerated_level_of_harm
        self._development_costs = development_costs
        self._startup_assets = startup_assets
        self._success_probability = success_probability
        self._private_benefit = private_benefit

        # product market payoffs (p.6ff.)
        # with innovation
        self._incumbent_profit_with_innovation = incumbent_profit_with_innovation
        self._cs_with_innovation = consumer_surplus_monopoly_with_innovation
        self._w_with_innovation = self._cs_with_innovation + self._incumbent_profit_with_innovation
        # without innovation
        self._incumbent_profit_without_innovation = incumbent_profit_without_innovation
        self._cs_without_innovation = consumer_surplus_monopoly_without_innovation
        self._w_without_innovation = self._cs_without_innovation + self._incumbent_profit_without_innovation
        # with duopoly
        self._startup_profit_duopoly = startup_profit_duopoly
        self._incumbent_profit_duopoly = incumbent_profit_duopoly
        self._cs_duopoly = consumer_surplus_duopoly
        self._w_duopoly = self._cs_duopoly + self._startup_profit_duopoly + self._incumbent_profit_duopoly

        # post-condition given (p.6-8)
        assert 0 < startup_assets < development_costs, "Startup has not enough assets for development"
        assert (
            self._w_without_innovation < self._w_with_innovation < self._w_duopoly
        ), "Ranking of total welfare not valid (p.7)"
        assert (
            success_probability * (self._w_with_innovation - self._w_without_innovation) > development_costs
        ), "A4 not satisfied (p.8)"
