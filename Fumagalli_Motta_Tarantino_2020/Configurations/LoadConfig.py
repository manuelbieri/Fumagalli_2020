import csv
import os.path
from typing import Optional

import Fumagalli_Motta_Tarantino_2020.Configurations.ConfigExceptions as Exceptions
import Fumagalli_Motta_Tarantino_2020.Types as Types


class _ParameterModel:
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
        assert key in self.params.keys()
        return self.params[key]

    def set(self, key: str, value: float):
        assert key in self.params.keys()
        self.params[key] = value
        assert self.params[key] == value

    @property
    def merger_policy(self) -> Types.MergerPolicies:
        return self.params["merger_policy"]

    @merger_policy.setter
    def merger_policy(self, value: Types.MergerPolicies):
        self.params["merger_policy"] = value

    def __call__(self, *args, **kwargs) -> dict:
        return self.params


class LoadParameters:
    file_name: str = "params.csv"

    def __init__(self, config_id: int, file_path: Optional[str] = None):
        self._id = config_id
        self._file_path = self._set_path(file_path)
        self.params: _ParameterModel = self._select_configuration()

    @staticmethod
    def _set_path(file_path: Optional[str]) -> str:
        return (
            os.path.join(os.path.dirname(__file__), LoadParameters.file_name)
            if file_path is None
            else file_path
        )

    def adjust_parameters(self, **kwargs) -> None:
        for (key, value) in kwargs.items():
            self.params.set(key, value)

    def _select_configuration(self) -> _ParameterModel:
        configs = self._parse_file()
        for config in configs:
            if config["id"] == self._id:
                return _ParameterModel(
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
        raise Exceptions.IDNotAvailableError("No configuration with this ID found.")

    def _parse_file(self):
        with open(file=self._file_path, newline="") as f:
            configs = []
            for row in csv.DictReader(f, skipinitialspace=True):
                if not self._is_comment_row(row):
                    tmp = {}
                    for k, v in row.items():
                        tmp.update({k: self._parse_value(v)})
                    configs.append(tmp)
        return configs

    @staticmethod
    def _is_comment_row(row: dict[str, str]) -> bool:
        if row["id"].strip() == "#":
            return True
        return False

    def toggle_development_success(self) -> None:
        self.params.set(
            "development_success", not self.params.get("development_success")
        )

    def set_startup_assets(self, value: float):
        self.params.set("startup_assets", value)

    def set_merger_policy(self, value: Types.MergerPolicies):
        self.params.merger_policy = value

    @staticmethod
    def _parse_value(value):
        try:
            return int(value)
        except ValueError:
            return float(value)

    def __call__(self, *args, **kwargs) -> dict:
        return self.params()
