This submodule provides the implementations for the visualization of the models in Fumagalli_Motta_Tarantino_2020.Models.

## Basic Usage
```python
import Fumagalli_Motta_Tarantino_2020 as FMT20


model = FMT20.OptimalMergerPolicy()

# see list below for available visualizations
visualizer = FMT20.Overview(model)

# show the plot in a canvas
visualizer.show()

# exceptional use for Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.PerfectInformation
model = FMT20.PerfectInformation()

# for the outcome for different merger policies over a range of assets
visualizer_perfect_information = FMT20.MergerPoliciesAssetRangePerfectInformation(model)
visualizer_perfect_information.show()
```

## Available Visualizations
The following models are available:
- Fumagalli_Motta_Tarantino_2020.Visualizations.Visualize.IVisualize
  - Interface for all visualizations
  - Do not try to initialize this class, it will fail for sure sooner or later
- Fumagalli_Motta_Tarantino_2020.Visualizations.Visualize.Timeline ($\Rightarrow$ inherits from Visualize.IVisualize)
  - Timeline of events for a specific model
- Fumagalli_Motta_Tarantino_2020.Visualizations.Visualize.Payoffs ($\Rightarrow$ inherits from Visualize.IVisualize)
  - Payoffs for different market configurations and stakeholders in a specific model
- Fumagalli_Motta_Tarantino_2020.Visualizations.VisualizeRanges.AssetRange ($\Rightarrow$ inherits from Visualize.IVisualize)
  - Outcomes for the set merger policy over a range of assets
- Fumagalli_Motta_Tarantino_2020.Visualizations.VisualizeRanges.MergerPoliciesAssetRange ($\Rightarrow$ inherits from VisualizeRanges.AssetRange)
  - Outcomes for the all available merger policies over a range of assets
- Fumagalli_Motta_Tarantino_2020.Visualizations.VisualizeRanges.MergerPoliciesAssetRangePerfectInformation ($\Rightarrow$ inherits from VisualizeRanges.MergerPoliciesAssetRange)
  - Outcomes for the set merger policy over a range of assets for Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.PerfectInformation
- Fumagalli_Motta_Tarantino_2020.Visualizations.VisualizeRanges.Overview ($\Rightarrow$ inherits from Visualize.IVisualize)
  - Combines Timeline, Payoffs and MergerPoliciesAssetRange for a specific model in one plot