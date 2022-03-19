import abc
from typing import Tuple, Optional

import numpy.random
import scipy.stats


class AbstractCDF(abc.ABC):
    def __init__(self, lower_threshold: float = 0, upper_threshold: float = 1) -> None:
        self._upper_threshold = upper_threshold
        self._lower_threshold = lower_threshold

    @abc.abstractmethod
    def _get_cdf_value(self, a) -> float:
        pass

    def draw(self, a: Optional[float] = None) -> Tuple[float, float]:
        if a is None:
            a: float = numpy.random.uniform(self._lower_threshold, self._upper_threshold)
        return a, self._get_cdf_value(a)


class NormCDF(AbstractCDF):
    def __init__(self, lower_threshold: float = 0, upper_threshold: float = 1) -> None:
        super(NormCDF, self).__init__(lower_threshold, upper_threshold)

    def _get_cdf_value(self, a) -> float:
        return float(scipy.stats.norm.cdf(a))
