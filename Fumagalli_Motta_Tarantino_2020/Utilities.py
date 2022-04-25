import scipy.stats


class NormalDistributionFunction:
    """
    Represents a normal distribution function.
    """

    @staticmethod
    def cumulative(x: float, **kwargs) -> float:
        """
        Returns the value of the cumulative distribution function.

        Parameters
        ----------
        x: float
            Value to get the corresponding value of the cumulative distribution function.
        kwargs
            Parameters for the normal distribution (loc and scale)

        Returns
        -------
        float
            Value of the cumulative distribution function.
        """
        return scipy.stats.norm.cdf(x, **kwargs)

    @staticmethod
    def inverse_cumulative(q: float, **kwargs) -> float:
        """
        Returns the value of the inverse cumulative distribution function (percent point function).

        Parameters
        ----------
        q: float
            Value to get the corresponding value of the inverse cumulative distribution function.
        kwargs
            Parameters for the normal distribution (loc and scale)

        Returns
        -------
        float
            Value of the inverse cumulative distribution function.
        """
        return scipy.stats.norm.ppf(q, **kwargs)
