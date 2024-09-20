import matplotlib.pyplot as plt
import Fumagalli_Motta_Tarantino_2020 as FMT20


def configure_two_axes(
    main="",
    sub1="",
    sub2="",
    m1: FMT20.OptimalMergerPolicy = None,
    m2: FMT20.OptimalMergerPolicy = None,
    c1: int = 1,
    c2: int = 2,
    v1=FMT20.MergerPoliciesAssetRange,
    v2=FMT20.MergerPoliciesAssetRange,
    figsize=(11, 5),
    **kwargs,
) -> (plt.Figure, plt.Axes, plt.Axes):
    """
    Creates a figure with two subplots in a row.
    """
    fig = plt.figure(layout="constrained", figsize=figsize)
    axes = fig.subplot_mosaic("""AB""")
    fig.suptitle(main, fontweight="bold", fontsize="x-large")
    fig.supylabel(kwargs.get("sub_y_label", "Merger Policy"))
    m1, m2 = _get_model(m1, m2, c1, c2, **kwargs)
    v1(model=m1, ax=axes["A"]).plot(**get_plot_kwargs(title=sub1, **kwargs))
    v2(model=m2, ax=axes["B"]).plot(**get_plot_kwargs(title=sub2, **kwargs))
    return fig, axes


def get_plot_kwargs(title: str, **kwargs):
    """
    Returns a standardized set of kwargs for the plots.
    """
    return {
        "title": title,
        "legend": kwargs.get("legend", False),
        "optimal_policy": True,
        "y_label": kwargs.get("y_label", ""),
        "parameters": False,
        "thresholds": True,
        "y_offset": -27,
    }


def get_model_by_id(
    c: int, preferred_type=FMT20.OptimalMergerPolicy, **kwargs
) -> FMT20.OptimalMergerPolicy:
    """
    Returns a valid model from a preset configuration, which is identified by an integer id.
    """
    p = FMT20.LoadParameters(config_id=c)
    p.set_merger_policy(kwargs.get("policy", FMT20.MergerPolicies.Strict))
    try:
        return _get_model_by_type(preferred_type, **p(), **kwargs)
    except AssertionError:
        try:
            return _get_model_by_type(FMT20.ProCompetitive, **p(), **kwargs)
        except AssertionError:
            return _get_model_by_type(
                FMT20.ResourceWaste,
                distribution=kwargs.get(
                    "distribution", FMT20.Distributions.NormalDistribution
                ),
                **p(),
                **kwargs,
            )


def _get_model_by_type(model_type, **kwargs) -> FMT20.OptimalMergerPolicy:
    return model_type(
        asset_distribution=kwargs.get(
            "distribution", FMT20.Distributions.UniformDistribution
        ),
        **kwargs,
    )


def _get_model(
    m1, m2, c1, c2, **kwargs
) -> (FMT20.OptimalMergerPolicy, FMT20.OptimalMergerPolicy):
    if (m1 is not None) and (m2 is not None):
        return m1, m2
    if ((m1 is not None) and (m2 is None)) or ((m1 is None) and (m2 is not None)):
        raise NotImplementedError("Too less or too much None to survive")
    return get_model_by_id(
        c1, policy=kwargs.get("policy1", FMT20.MergerPolicies.Strict), **kwargs
    ), get_model_by_id(
        c2, policy=kwargs.get("policy2", FMT20.MergerPolicies.Strict), **kwargs
    )


def get_distribution_labels(
    distribution: type(FMT20.Distributions.NormalDistribution), long_label=False
) -> str:
    """
    Returns labels for the available distributions.
    """
    if distribution == FMT20.Distributions.NormalDistribution:
        return "Normal" + (" Distribution" if long_label else "")
    if distribution == FMT20.Distributions.UniformDistribution:
        return "Uniform" + (" Distribution" if long_label else "")


def get_configurations() -> list[str]:
    """
    Returns a list with all available configurations and their labels.
    """
    output = []
    for i in range(0, 60):
        try:
            m = get_model_by_id(i)
            output.append(f"{i} - {FMT20.IVisualize.get_model_label(type(m))}")
        except FMT20.IDNotAvailableError:
            pass
    return output
