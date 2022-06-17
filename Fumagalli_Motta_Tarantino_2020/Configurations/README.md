# Preset Configurations

To make the life of the user easier, here are some predefined configuration of parameters with specific characteristics.

## How to use

```python
import Fumagalli_Motta_Tarantino_2020 as FMT20

params = FMT20.LoadParameters(config_id=3) # load configuration
model = FMT20.OptimalMergerPolicy(**params()) # Do not forget the stars in front of the call

# Advanced use
params = FMT20.LoadParameters(config_id=2)
params.adjust_parameters(development_costs=0.11) # change parameters in the configuration
params.set_merger_policy(FMT20.MergerPolicies.Laissez_faire) # change merger policy
params.toggle_development_success() # change the development outcome to the opposite
model_with_adjustments = FMT20.OptimalMergerPolicy(**params())
```

Change the `config_id` argument for a different configuration of parameters.

## Available Configurations

See Fumagalli_Motta_Tarantino_2020.Models.BaseModel for the definition of the thresholds.

| ID  |     Shelving     | $F(\bar{A}) > \Gamma(\cdot)$ | $F(\bar{A}) > \Phi(\cdot)$ | $F(\bar{A}) > \Phi'(\cdot)$ | $F(\bar{A}^T) > \Phi^T(\cdot)$ | Optimized for  |
|:---:|:----------------:|:----------------------------:|:--------------------------:|:---------------------------:|:------------------------------:|:---------------|
|  1  |       True       |            False             |            True            |            True             |              True              | OptimalMerger  |
|  2  |       True       |            False             |           False            |            False            |             False              | OptimalMerger  |
|  3  |      False       |             True             |           False            |            False            |              True              | OptimalMerger  |
|  4  |      False       |            False             |            True            |            True             |              True              | OptimalMerger  |
|  5  |      False       |            False             |           False            |            False            |              True              | OptimalMerger  |
| 30  |       True       |            False             |            True            |            True             |              True              | ProCompetitive |
| 31  |       True       |            False             |           False            |            False            |             False              | ProCompetitive |
| 32  |       True       |            False             |            True            |            True             |              True              | ProCompetitive |
| 40  |       True       |            False             |            True            |            True             |              True              | ResourceWaste  |
| 41  |       True       |             True             |           False            |            False            |             False              | ResourceWaste  |
| 42  |       True       |             True             |            True            |            False            |              True              | ResourceWaste  |

Further ranges of configurations are:
- 1-5: Standard configurations for Fumagalli_Motta_Tarantino_2020.Models.OptimalMergerPolicy
- 10-19: Configurations for Fumagalli_Motta_Tarantino_2020.Models.OptimalMergerPolicy used in Figures.ipynb
- 30-39: Configurations for Fumagalli_Motta_Tarantino_2020.ExtensionModels.ProCompetitive used in Figures.ipynb and tests 
- 40-49: Configurations for Fumagalli_Motta_Tarantino_2020.ExtensionModels.ResourceWaste used in Figures.ipynb and tests
- 50-59: Configurations for Fumagalli_Motta_Tarantino_2020.AdditionalModels.PerfectInformation used in Figures.ipynb and tests

Find the full set of configurations and their visualization in Notebooks/Configurations.ipynb.
