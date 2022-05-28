# Preset Configurations


# How to use

```python
from Fumagalli_Motta_Tarantino_2020 import *

params = Config.LoadParameters(config_id=111) # load configuration
model = OptimalMergerPolicy(**params()) # Do not forget the stars in front of the call
```



# Available Configurations

| ID    | I. Shelving expected | II. $F(\bar{A}) > \Gamma(\cdot)$ | III. $F(\bar{A}) > \Phi(\cdot)$ | IV. $F(\bar{A}) > \Phi'(\cdot)$ | V. $F(\bar{A}^T) > \Phi^T(\cdot)$ |
|:------|:--------------------:|:--------------------------------:|:-------------------------------:|:-------------------------------:|:---------------------------------:|
| *100* |         True         |                X                 |                X                |              True               |                 X                 |
| *101* |         True         |                X                 |                X                |              False              |                 X                 |
| *110* |        False         |               True               |              False              |                X                |                 X                 |
| *111* |        False         |               True               |              True               |                X                |                 X                 |
| *112* |        False         |              False               |              False              |                X                |                 X                 |




