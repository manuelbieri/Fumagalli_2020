import scipy.stats


class NormalDistributionFunction:
    @staticmethod
    def cumulative(x: float, **kwargs) -> float:
        return scipy.stats.norm.cdf(x, **kwargs)

    @staticmethod
    def inverse_cumulative(q: float, **kwargs) -> float:
        return scipy.stats.norm.ppf(q, **kwargs)
