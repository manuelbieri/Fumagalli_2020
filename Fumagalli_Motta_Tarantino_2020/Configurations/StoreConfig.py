import Fumagalli_Motta_Tarantino_2020.Models.Types as Types


class ParameterModel:
    """
    Holds all parameters (excluding the asset distribution) for a
    Fumagalli_Motta_Tarantino_2020.Models.OptimalMergerPolicy  model and all child classes using the same parameters.
    """

    def __init__(
        self,
        merger_policy: Types.MergerPolicies,
        development_costs: float,
        startup_assets: float,
        success_probability: float,
        development_success: bool,
        private_benefit: float,
        consumer_surplus_without_innovation: float,
        incumbent_profit_without_innovation: float,
        consumer_surplus_duopoly: float,
        incumbent_profit_duopoly: float,
        startup_profit_duopoly: float,
        consumer_surplus_with_innovation: float,
        incumbent_profit_with_innovation: float,
    ):
        self.params = {
            "merger_policy": merger_policy,
            "development_costs": development_costs,
            "startup_assets": startup_assets,
            "success_probability": success_probability,
            "development_success": development_success,
            "private_benefit": private_benefit,
            "consumer_surplus_without_innovation": consumer_surplus_without_innovation,
            "incumbent_profit_without_innovation": incumbent_profit_without_innovation,
            "consumer_surplus_duopoly": consumer_surplus_duopoly,
            "incumbent_profit_duopoly": incumbent_profit_duopoly,
            "startup_profit_duopoly": startup_profit_duopoly,
            "consumer_surplus_with_innovation": consumer_surplus_with_innovation,
            "incumbent_profit_with_innovation": incumbent_profit_with_innovation,
        }

    def get(self, key: str):
        """
        Returns the value for a specific parameter value
        """
        assert key in self.params.keys()
        return self.params[key]

    def set(self, key: str, value: float):
        """
        Sets the value of a specific parameter value.

        For the merger policy use the designated setter
        (Fumagalli_Motta_Tarantino_2020.Configurations.LoadConfig.merger_policy).
        """
        assert key in self.params.keys()
        self.params[key] = value
        assert self.params[key] == value

    @property
    def merger_policy(self) -> Types.MergerPolicies:
        return self.params["merger_policy"]

    @merger_policy.setter
    def merger_policy(self, value: Types.MergerPolicies):
        assert type(value) is Types.MergerPolicies
        self.params["merger_policy"] = value

    def __call__(self, *args, **kwargs) -> dict:
        """
        Returns a dict containing all the parameters and their values.
        """
        return self.params
