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
    """

    def __init__(self, tolerated_level_of_harm: float = 1,
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

        | Condition | Remark | Page (Assumption) |
        |-----------|--------|--------------|
        | $\\bar{H} \\ge 0$ | The tolerated level of harm has to be bigger than 0. | p.6 |
        | $p \\in (0,1]$ | probability that the prototype is developed successfully depends on the non-contractible effort exerted by the entrepreneur of the firm that owns the project. In case of no effort the project fails for sure, but the entrepreneur obtains a positive private benefit. In case of failure the project yields no profit. | p.8 |
        | $B>0$ | Private benefit of the entrepreneur in case of failure. | p.8 |
        | $\\pi^m_I>\\pi^d_I$ | Profit of the incumbent has to be bigger without the innovation than in the duopoly. | p.7 |
        | $\\pi^M_I>\\pi^m_I$ | Industry profits are higher with a multi-product monopolist than a single product monopolist. | p.7 |
        | $CS^M \\ge CS^m$ | Consumer surplus with the innovation has to weakly bigger than without the innovation. | p.7 |
        | $\\pi^M_I>\\pi^d_I+\\pi^d_S$ | Industry profits are higher under monopoly than under duopoly. If this assumption did not hold, the takeover would not take place. | p.7 (A1) |
        | $\\pi^d_S>\\pi^M_I+\\pi^m_I$ | An incumbent has less incentive to innovate (in a new/better product or a more efficient production process) than a potential entrant because the innovation would cannibalise the incumbent’s current profits. (Corresponds to Arrow's replacement effect) | p.7 (A2) |
        | $p\\pi^d_S>K$ | In case of effort it is efficient to develop the prototype, i.e., development has a positive net present value (NPV) for the start-up | p.8 (A3) |
        | $p(W^M-W^m)>K$ | The development of the project is not only privately beneficial for the start-up, but also for society as a whole, whether undertaken by the incumbent or the start-up. | p.8 (A4)|
        | $B-K<0$$B-(p\\pi^d_S-K)<0$ | The first inequality implies that if S shirks the project has negative value; thus, no financial contract could be signed unless the startup makes effort. The second implies that the start-up may be financially constrained, that is, it may hold insufficient assets to fund the development of the prototype even though the project has a positive NPV. | p.8 (A5) |

        Parameters
        ----------
        tolerated_level_of_harm
        development_costs
        startup_assets
        success_probability
        private_benefit
        consumer_surplus_monopoly_without_innovation
        incumbent_profit_without_innovation
        consumer_surplus_duopoly
        incumbent_profit_duopoly
        startup_profit_duopoly
        consumer_surplus_monopoly_with_innovation
        incumbent_profit_with_innovation
        """

        # preconditions given (p.6-8)
        assert tolerated_level_of_harm >= 0, "Level of harm has to be bigger than 0"
        assert incumbent_profit_without_innovation > incumbent_profit_duopoly,\
            "Profit of the incumbent has to be bigger without the innovation than in the duopoly"
        assert incumbent_profit_with_innovation > incumbent_profit_without_innovation,\
            "Profit of the incumbent has to be bigger with the innovation than without the innovation"
        assert consumer_surplus_monopoly_with_innovation >= consumer_surplus_monopoly_without_innovation,\
            "Consumer surplus with the innovation has to weakly bigger than without the innovation"
        assert incumbent_profit_with_innovation > incumbent_profit_duopoly + startup_profit_duopoly, \
            "A1 not satisfied (p.7)"
        assert startup_profit_duopoly > incumbent_profit_with_innovation - incumbent_profit_without_innovation, \
            "A2 not satisfied (p.7)"
        assert 0 < success_probability <= 1, \
            "Success probability of development has to be between 0 and 1"
        assert success_probability * startup_profit_duopoly > development_costs, \
            "A3 not satisfied (p.8)"
        assert private_benefit - development_costs < 0 and \
            0 < private_benefit * (success_probability * startup_profit_duopoly - development_costs), \
            "A5 not satisfied (p.8)"

        self.tolerated_harm = tolerated_level_of_harm
        self.development_costs = development_costs
        self.startup_assets = startup_assets
        self.success_probability = success_probability
        self.private_benefit = private_benefit

        # product market payoffs (p.6ff.)
        # with innovation
        self.incumbent_profit_with_innovation = incumbent_profit_with_innovation
        self.cs_with_innovation = consumer_surplus_monopoly_with_innovation
        self.w_with_innovation = self.cs_with_innovation + self.incumbent_profit_with_innovation
        # without innovation
        self.incumbent_profit_without_innovation = incumbent_profit_without_innovation
        self.cs_without_innovation = consumer_surplus_monopoly_without_innovation
        self.w_without_innovation = self.cs_without_innovation + self.incumbent_profit_without_innovation
        # with duopoly
        self.startup_profit_duopoly = startup_profit_duopoly
        self.incumbent_profit_duopoly = incumbent_profit_duopoly
        self.cs_duopoly = consumer_surplus_duopoly
        self.w_duopoly = self.cs_duopoly + self.startup_profit_duopoly + self.incumbent_profit_duopoly

        # post-condition given (p.6-8)
        assert 0 < startup_assets < development_costs, \
            "Startup has not enough assets for development"
        assert self.w_without_innovation < self.w_with_innovation < self.w_duopoly, \
            "Ranking of total welfare not valid (p.7)"
        assert success_probability * (self.w_with_innovation - self.w_without_innovation) > development_costs, \
            "A4 not satisfied (p.8)"
