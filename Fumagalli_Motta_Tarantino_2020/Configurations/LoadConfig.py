import csv
import os.path
from typing import Optional

import Fumagalli_Motta_Tarantino_2020.Configurations.StoreConfig as StoreConfig
import Fumagalli_Motta_Tarantino_2020.Configurations.ConfigExceptions as Exceptions
import Fumagalli_Motta_Tarantino_2020.Models.Types as Types


class LoadParameters:
    """
    Loads a specific configuration from a file.
    """

    file_name: str = "params.csv"
    """Filename of the configuration file."""

    def __init__(self, config_id: int, file_path: Optional[str] = None):
        """
        Initializes a valid object with a valid path to the configuration file and a valid id for the configuration.

        Parameters
        ----------
        config_id: int
            ID of the configuration (Fumagalli_Motta_Tarantino_2020.Configurations)
        file_path: str
            Path to configuration file, if not set, then the standard file is used.
        """
        self._id = config_id
        self._file_path = self._set_path(file_path)
        self.params: StoreConfig.ParameterModel = self._select_configuration()

    @staticmethod
    def _set_path(file_path: Optional[str]) -> str:
        return (
            os.path.join(os.path.dirname(__file__), LoadParameters.file_name)
            if file_path is None
            else file_path
        )

    def adjust_parameters(self, **kwargs) -> None:
        """
        Change parameter values of the configuration.

        You can change as many values as you wish with one call.

        Parameters
        ----------
        **kwargs
          Form: {"name_of_parameter": new_value_of_parameter, ...}
        """
        for key, value in kwargs.items():
            self.params.set(key, value)

    def _select_configuration(self) -> StoreConfig.ParameterModel:
        configs = self._parse_file()
        for config in configs:
            if config["id"] == self._id:
                return StoreConfig.ParameterModel(
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
        """
        Changes the value of the development success (if attempted) to the exact opposite.

        - False $\\Rightarrow$ True
        - True $\\Rightarrow$ False
        """
        self.params.set(
            "development_success", not self.params.get("development_success")
        )

    def set_startup_assets(self, value: float):
        """
        Sets the value of the start-up assets.
        """
        self.params.set("startup_assets", value)

    def set_merger_policy(self, value: Types.MergerPolicies):
        """
        Sets the merger policy.
        """
        self.params.merger_policy = value

    @staticmethod
    def _parse_value(value):
        try:
            return int(value)
        except ValueError:
            return float(value)

    def __call__(self, *args, **kwargs) -> dict:
        """
        Returns a dict containing all the parameters and their values.
        """
        return self.params()
