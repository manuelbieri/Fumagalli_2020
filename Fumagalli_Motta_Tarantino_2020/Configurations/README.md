# Preset Configurations

To make the life of the user easier, here are some predefined configuration of parameters with specific characteristics.

## How to use

```python
from Fumagalli_Motta_Tarantino_2020 import *

params = Config.LoadParameters(config_id=3) # load configuration
model = OptimalMergerPolicy(**params()) # Do not forget the stars in front of the call

# Advanced use
params = Config.LoadParameters(config_id=2)
params.adjust_parameters(development_costs=0.11) # change parameters in the configuration
params.set_merger_policy(Types.MergerPolicies.Laissez_faire) # change merger policy
params.toggle_development_success() # change the development outcome to the opposite
model_with_adjustments = OptimalMergerPolicy(**params())
```

Change the `config_id` argument for a different configuration of parameters.

## Available Configurations

See Fumagalli_Motta_Tarantino_2020.Models.BaseModel for the definition of the thresholds.

|  ID  |     Shelving     | $F(\bar{A}) > \Gamma(\cdot)$ | $F(\bar{A}) > \Phi(\cdot)$ | $F(\bar{A}) > \Phi'(\cdot)$ | $F(\bar{A}^T) > \Phi^T(\cdot)$ | Optimized for  |
|:----:|:----------------:|:----------------------------:|:--------------------------:|:---------------------------:|:------------------------------:|:---------------|
|  1   |       True       |            False             |            True            |            True             |              True              | OptimalMerger  |
|  2   |       True       |            False             |           False            |            False            |             False              | OptimalMerger  |
|  3   |      False       |             True             |           False            |            False            |              True              | OptimalMerger  |
|  4   |      False       |            False             |            True            |            True             |              True              | OptimalMerger  |
|  5   |      False       |            False             |           False            |            False            |              True              | OptimalMerger  |
|  30  |       True       |            False             |            True            |            True             |              True              | ProCompetitive |
|  31  |       True       |            False             |           False            |            False            |             False              | ProCompetitive |
|  32  |       True       |            False             |            True            |            True             |              True              | ProCompetitive |
| *33* |       True       |            False             |            True            |            True             |              True              | ResourceWaste  |
|  34  |       True       |             True             |           False            |            False            |             False              | ResourceWaste  |
