import abc
from typing import Tuple, Optional

import numpy.random
import scipy.stats


class AbstractCDF(abc.ABC):
    @abc.abstractmethod
    def __init__(self, lower_threshold: float = 0, upper_threshold: float = 1) -> None:
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold

    @abc.abstractmethod
    def draw(self, a: Optional[float] = None) -> Tuple[float, float]:
        pass


class NormCDF(AbstractCDF):
    def __init__(self, lower_threshold: float = 0, upper_threshold: float = 1) -> None:
        super(NormCDF, self).__init__(lower_threshold, upper_threshold)

    def draw(self, a: Optional[float] = None) -> Tuple[float, float]:
        if a is None:
            a: float = numpy.random.uniform(self.lower_threshold, self.upper_threshold)
        return a, float(scipy.stats.norm.cdf(a))
