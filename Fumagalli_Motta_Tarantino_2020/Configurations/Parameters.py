import csv
import os.path

import Fumagalli_Motta_Tarantino_2020.Types as Types
import Fumagalli_Motta_Tarantino_2020 as FMT20


class LoadParameters:
    file_dir: str = os.path.dirname(__file__)
    file_name: str = "params.csv"
    file_path: str = os.path.join(file_dir, file_name)

    def __init__(self, config_id: int):
        self.id = config_id
        # noinspection PyTypeChecker
        self.params: Parameters = None
        self._parse_config()
        assert self.params is not None, "ID not available"

    def _parse_config(self):
        with open(file=LoadParameters.file_path, newline="") as f:
            configs = [
                {k: self.parse_value(v) for k, v in row.items()}
                for row in csv.DictReader(f, skipinitialspace=True)
            ]

        for config in configs:
            if config["id"] == self.id:
                self.params = Parameters(
                    merger_policy=Types.MergerPolicies.Strict,
                    development_costs=config["K"],
                    startup_assets=config["A"],
                    success_probability=config["p"],
                    development_success=True,
                    private_benefit=config["B"],
                    consumer_surplus_without_innovation=config["CSm"],
                    incumbent_profit_without_innovation=config["PmI"],
                    consumer_surplus_duopoly=config["CSd"],
                    incumbent_profit_duopoly=config["PdI"],
                    startup_profit_duopoly=config["PdS"],
                    consumer_surplus_with_innovation=config["CSM"],
                    incumbent_profit_with_innovation=config["PMI"],
                )

    def toggle_development_success(self) -> None:
        self.params.development_success = not self.params.development_success

    def set_startup_assets(self, value: float):
        self.params.startup_asset = value

    def set_merger_policy(self, value: Types.MergerPolicies):
        self.params.merger_policy = value

    @staticmethod
    def parse_value(value):
        try:
            return int(value)
        except ValueError:
            return float(value)

    def __call__(self, *args, **kwargs) -> dict:
        return self.params()


class Parameters:
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
        self._merger_policy = merger_policy
        self._development_costs = development_costs
        self._startup_assets = startup_assets
        self._success_probability = success_probability
        self._development_success = development_success
        self._private_benefit = private_benefit
        self._incumbent_profit_with_innovation = incumbent_profit_with_innovation
        self._cs_with_innovation = consumer_surplus_with_innovation
        self._incumbent_profit_without_innovation = incumbent_profit_without_innovation
        self._cs_without_innovation = consumer_surplus_without_innovation
        self._startup_profit_duopoly = startup_profit_duopoly
        self._incumbent_profit_duopoly = incumbent_profit_duopoly
        self._cs_duopoly = consumer_surplus_duopoly

    @property
    def development_success(self) -> bool:
        return self._development_success

    @development_success.setter
    def development_success(self, value: bool):
        self._development_success = value

    @property
    def startup_asset(self) -> float:
        return self._startup_assets

    @startup_asset.setter
    def startup_asset(self, value: float):
        self._startup_assets = value

    @property
    def merger_policy(self) -> Types.MergerPolicies:
        return self._merger_policy

    @merger_policy.setter
    def merger_policy(self, value: Types.MergerPolicies):
        self._merger_policy = value

    def get_kwargs(self) -> dict:
        return {
            "merger_policy": self._merger_policy,
            "development_costs": self._development_costs,
            "startup_assets": self._startup_assets,
            "success_probability": self._success_probability,
            "development_success": self._development_success,
            "private_benefit": self._private_benefit,
            "consumer_surplus_without_innovation": self._cs_without_innovation,
            "incumbent_profit_without_innovation": self._incumbent_profit_without_innovation,
            "consumer_surplus_duopoly": self._cs_duopoly,
            "incumbent_profit_duopoly": self._incumbent_profit_duopoly,
            "startup_profit_duopoly": self._startup_profit_duopoly,
            "consumer_surplus_with_innovation": self._cs_with_innovation,
            "incumbent_profit_with_innovation": self._incumbent_profit_with_innovation,
        }

    def __call__(self, *args, **kwargs) -> dict:
        return self.get_kwargs()


if __name__ == "__main__":
    p = LoadParameters(config_id=101)
    m = FMT20.OptimalMergerPolicy(**p())
    print("(1)", m.is_incumbent_expected_to_shelve())
    print("(2)", m.asset_threshold_cdf > m.asset_distribution_threshold_strict)
    print("(3)", m.asset_threshold_cdf > m.asset_distribution_threshold)
    print("(4)", m.asset_threshold_cdf > m.asset_distribution_threshold_intermediate)
    print(
        "(5)",
        m.asset_threshold_late_takeover_cdf
        > m.asset_distribution_threshold_laissez_faire,
    )
