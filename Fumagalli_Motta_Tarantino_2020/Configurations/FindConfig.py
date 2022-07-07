import random
from numpy import arange
from typing import Callable

import Fumagalli_Motta_Tarantino_2020.Configurations.StoreConfig as StoreConfig
import Fumagalli_Motta_Tarantino_2020.Models.Base as Base
import Fumagalli_Motta_Tarantino_2020.Models.Types as Types
import Fumagalli_Motta_Tarantino_2020.Models.Distributions as Distributions


class ParameterModelGenerator:
    """
    Generates a random set of parameters for Fumagalli_Motta_Tarantino_2020.Models.Base.CoreModel.
    """

    def __init__(
        self,
        lower=0.01,
        upper=0.99,
        step=0.01,
    ):
        """
        Sets the list of choices to draw the set of parameters from.

        Parameters
        ----------
        lower: float
            Lower thresholds of the range of choices.
        upper: float
            Upper thresholds of the range of choices.
        step: float
            Step between to choices in the range.
        """
        self.lower = lower
        self.upper = upper
        self.step = step

    def get_parameter_model(self, **kwargs) -> StoreConfig.ParameterModel:
        """
        Draws a random set of parameters.

        Parameters
        ----------
        **kwargs
            Constant inputs for the parameter model.

        Returns
        -------
        StoreConfig.ParameterModel
            ParameterModel containing the set of parameters.
        """
        choices = list(arange(self.lower, self.upper, self.step))
        choice = random.choices(choices, k=11)
        choice = [round(i, ndigits=2) for i in choice]
        return StoreConfig.ParameterModel(
            merger_policy=kwargs.get("merger_policy", Types.MergerPolicies.Strict),
            development_costs=kwargs.get("development_costs", choice[0]),
            startup_assets=kwargs.get("startup_assets", choice[1]),
            success_probability=kwargs.get("success_probability", choice[2]),
            development_success=kwargs.get("development_success", True),
            private_benefit=kwargs.get("private_benefit", choice[3]),
            consumer_surplus_without_innovation=kwargs.get(
                "consumer_surplus_without_innovation", choice[4]
            ),
            incumbent_profit_without_innovation=kwargs.get(
                "incumbent_profit_without_innovation", choice[5]
            ),
            consumer_surplus_duopoly=kwargs.get("consumer_surplus_duopoly", choice[6]),
            incumbent_profit_duopoly=kwargs.get("incumbent_profit_duopoly", choice[7]),
            startup_profit_duopoly=kwargs.get("startup_profit_duopoly", choice[8]),
            consumer_surplus_with_innovation=kwargs.get(
                "consumer_surplus_with_innovation", choice[9]
            ),
            incumbent_profit_with_innovation=kwargs.get(
                "incumbent_profit_with_innovation", choice[10]
            ),
        )


class RandomConfig:
    """
    Finds a random configuration satisfying specific requirements.

    Example
    --------
    ```
    import Fumagalli_Motta_Tarantino_2020 as FMT20

    # search for a random configuration -> this can take a while
    config = FMT20.RandomConfig(laissez_faire_optimal=True).find_config()
    model = FMT20.OptimalMergerPolicy(**config())
    print(model.is_laissez_faire_optimal())
    ```
    """

    def __init__(
        self,
        parameter_generator=ParameterModelGenerator(),
        model_type: Callable = Base.OptimalMergerPolicy,
        callable_condition: Callable = None,
        strict_optimal=None,
        intermediate_optimal=None,
        laissez_faire_optimal=None,
        is_killer_acquisition=None,
        **kwargs
    ):
        """
        Specify the requirements to satisfy in the model to find.

        Parameters
        ----------
        parameter_generator: ParameterModelGenerator
            Generator for random sets of parameters
        model_type: Callable
            Type of the model to find the parameters for (conforms to Base.OptimalMergerPolicy).
        callable_condition: Callable
            Lambda with model as input and boolean as output (True equals satisfied requirement).
        strict_optimal: Optional[bool]
            If True, the model has a strict policy as optimal policy.
        intermediate_optimal: Optional[bool]
            If True, the model has an intermediate policy as optimal policy.
        laissez_faire_optimal: Optional[bool]
            If True, the model has a laissez-faire policy as optimal policy.
        is_killer_acquisition: Optional[bool]
            If True, the model facilitates a killer acquisition.
        **kwargs
            Constant inputs for the parameter model.
        """
        self.parameter_generator = parameter_generator
        self._model_type = model_type
        self.strict_optimal = strict_optimal
        self.intermediate_optimal = intermediate_optimal
        self.laissez_faire_optimal = laissez_faire_optimal
        self.is_killer_acquisition = is_killer_acquisition
        self.callable_condition = callable_condition
        self._kwargs = kwargs

    def _check_conditions(self, model: Base.OptimalMergerPolicy) -> bool:
        if not self._check_condition(model.is_strict_optimal(), self.strict_optimal):
            return False
        if not self._check_condition(
            model.is_intermediate_optimal(), self.intermediate_optimal
        ):
            return False
        if not self._check_condition(
            model.is_laissez_faire_optimal(), self.laissez_faire_optimal
        ):
            return False
        if not self._check_condition(
            model.is_killer_acquisition(), self.is_killer_acquisition
        ):
            return False
        if not self._check_callable_condition(self.callable_condition, model):
            return False
        return True

    @staticmethod
    def _check_callable_condition(condition: Callable, model: Base.OptimalMergerPolicy):
        if condition is not None:
            return condition(model)
        return True

    @staticmethod
    def _check_condition(value: bool, check: bool) -> bool:
        if check is not None:
            if value == check:
                return True
            else:
                return False
        return True

    def find_config(self) -> StoreConfig.ParameterModel:
        """
        Triggers the process of finding a set of parameters satisfying the requirements.

        Note: This can take a while, depending on the given conditions (or sometimes it is not possible to find a set
        of parameters).

        Returns
        -------
        StoreConfig.ParameterModel
            ParameterModel containing the set of parameters.
        """
        while True:
            try:
                parameter_model: StoreConfig.ParameterModel = (
                    self.parameter_generator.get_parameter_model(**self._kwargs)
                )
                model = self._get_model(parameter_model)
                if self._check_conditions(model):
                    return parameter_model
                else:
                    pass
            except AssertionError:
                pass

    def _get_model(self, parameter_model):
        model = self._model_type(
            **parameter_model(),
            asset_distribution=self._kwargs.get(
                "asset_distribution", Distributions.UniformDistribution
            ),
        )
        return model
