This submodule provides the implementations of the models presented in Fumagalli et al. (2020) as well as extension of 
these models by Manuel Bieri.

## Basic Usage
```python
import Fumagalli_Motta_Tarantino_2020 as FMT20

# see list below for the available models
model = FMT20.OptimalMergerPolicy()

# print summary
print(model)

# get summary as dict
summary = model.summary()

# check whether a killer acquisition occurred
print(model.is_killer_acquisition())

# get the optimal merger policy
print(model.get_optimal_merger_policy())
```

## Available Models
The following models are available:
- Fumagalli_Motta_Tarantino_2020.Models.Base.BaseModel
  - Validates input parameters according to section 2 of Fumagalli et al. (2020)
  - Use always Fumagalli_Motta_Tarantino_2020.Models.Base.OptimalMergerPolicy instead
- Fumagalli_Motta_Tarantino_2020.Models.Base.MergerPolicy ($\Rightarrow$ inherits from Base.BaseModel)
  - Implements the logic of merger policies presented in sections 3-5 of Fumagalli et al. (2020)
  - Use always Fumagalli_Motta_Tarantino_2020.Models.Base.OptimalMergerPolicy instead
- Fumagalli_Motta_Tarantino_2020.Models.Base.OptimalMergerPolicy ($\Rightarrow$ inherits from Base.MergerPolicy)
  - Implements the logic of optimal merger policies presented in section 6 of Fumagalli et al. (2020)
  - Used as standard model, since it implements all the logic from the basic model
- Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.CournotCompetition ($\Rightarrow$ inherits from Base.OptimalMergerPolicy)
  - Implements the logic of the model presented in section 7 of Fumagalli et al. (2020)
- Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.EquityContract ($\Rightarrow$ inherits from Base.OptimalMergerPolicy)
  - Implements the logic of the model presented in section 8.4 of Fumagalli et al. (2020)
- Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.PerfectInformation ($\Rightarrow$ inherits from Base.OptimalMergerPolicy)
  - Implements the logic of the model presented in section 8.5 of Fumagalli et al. (2020)
- Fumagalli_Motta_Tarantino_2020.Models.Extension.ProCompetitive ($\Rightarrow$ inherits from Base.OptimalMergerPolicy)
  - Implements the logic of the model presented in section A.3 of "Extension of Fumagalli et al (2020).pdf"
- Fumagalli_Motta_Tarantino_2020.Models.Extension.ResourceWaste ($\Rightarrow$ inherits from Extension.ProCompetitive)
  - Implements the logic of the model presented in section A.4 of "Extension of Fumagalli et al (2020).pdf"

