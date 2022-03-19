![CI](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/CI.yml/badge.svg)
[![CodeCov](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/CodeCov.yml/badge.svg)](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/CodeCov.yml)
[![codecov](https://codecov.io/gh/manuelbieri/Fumagalli_2020/branch/master/graph/badge.svg?token=RRZ3PJI9U1)](https://codecov.io/gh/manuelbieri/Fumagalli_2020)
[![CodeQL](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/codeql-analysis.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Basic Usage

```python
import Fumagalli_Motta_Tarantino_2020.Model as Model

# initialize the model (here you can adjust the parameters of the model)
# if the parameters are not valid for the model an assertion-error with a corresponding message will be displayed
model: Model.BaseModel = Model.BaseModel()
```

### Dependencies

These packages include all the needed imports for the functionality of this package.

| Package &emsp; | Version &emsp; | Annotation &emsp;                          |
|:---------------|:--------------:|:-------------------------------------------|
| scipy          |     1.8.0      | Always                                     |
| numpy          |     1.22.3     | Always                                     |
| jupyter        |     1.0.0      | For the demonstration in jupyter Notebooks |
| IPython        |     8.1.1      | For the demonstration in jupyter Notebooks |
| pdoc           |     10.0.3     | To generate the documentation from scratch |

Install the dependencies with the following command:

```shell
$ pip install -r requirements.txt
```
(Note: Make sure you are operating in the same directory, where the `requirements.txt` is located.)

### Generate Documentation
Generate the documentation with the following command:

```shell
$ pdoc -o docs Fumagalli_Motta_Tarantino_2020 --docformat numpy --math
```

or run the shell-script `docs/build.sh` in the terminal.
