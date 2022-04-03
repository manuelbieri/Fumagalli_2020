![CI](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/CI.yml/badge.svg)
[![CodeCov](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/CodeCov.yml/badge.svg)](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/CodeCov.yml)
[![codecov](https://codecov.io/gh/manuelbieri/Fumagalli_2020/branch/master/graph/badge.svg?token=RRZ3PJI9U1)](https://codecov.io/gh/manuelbieri/Fumagalli_2020)
[![CodeQL](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/codeql-analysis.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Code Style Check](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/Black.yml/badge.svg)](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/Black.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/manuelbieri/fumagalli_2020/badge)](https://www.codefactor.io/repository/github/manuelbieri/fumagalli_2020)
[![GitHub repo size](https://img.shields.io/github/repo-size/manuelbieri/Fumagalli_2020)](https://github.com/manuelbieri/Fumagalli_2020)
![GitHub license](https://img.shields.io/github/license/manuelbieri/Fumagalli_2020)
![GitHub last commit](https://img.shields.io/github/last-commit/manuelbieri/Fumagalli_2020)
![GitHub Release Date](https://img.shields.io/github/release-date/manuelbieri/Fumagalli_2020)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/manuelbieri/Fumagalli_2020)](https://pypi.org/project/Fumagalli-Motta-Tarantino-2020/)


### Basic Usage

```python
import Fumagalli_Motta_Tarantino_2020.Model as Model

# initialize the model (here you can adjust the parameters of the model)
model: Model.MergerPolicyModel = Model.MergerPolicyModel()

# print a summary of the outcome
print(model.summary())
```

### Dependencies

These packages include all the needed imports for the functionality of this package.

| Package &emsp; | Version &emsp; | Annotation &emsp;                          |
|:---------------|:--------------:|:-------------------------------------------|
| scipy          |     1.8.0      | Always                                     |
| numpy          |     1.22.3     | Always                                     |
| black          |     22.1.0     | For consistent code formatting             |
| jupyter        |     1.0.0      | For the demonstration in jupyter Notebooks |
| IPython        |     8.2.0      | For the demonstration in jupyter Notebooks |
| pdoc           |     10.0.4     | To generate the documentation from scratch |

Install the dependencies with the following command:

```shell
$ pip install -r requirements.txt
```
(Note: Make sure you are operating in the same directory, where the `requirements.txt` is located.)

### Tests

Run the unittests with the following command (pay attention to the current working directory):

```shell
python -m unittest discover Fumagalli_Motta_Tarantino_2020/tests "Test_*.py"
```

See [codecov.io](https://app.codecov.io/gh/manuelbieri/Fumagalli_2020) for a detailed report about the test coverage.

### Generate Documentation
Generate the documentation with the following command:

```shell
$ pdoc -o docs Fumagalli_Motta_Tarantino_2020 --docformat numpy --math
```

or run the shell-script `docs/build.sh` in the terminal.
