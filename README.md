[![CI](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/CodeCov.yml/badge.svg)](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/CodeCov.yml)
[![codecov](https://codecov.io/gh/manuelbieri/Fumagalli_2020/branch/master/graph/badge.svg?token=RRZ3PJI9U1)](https://codecov.io/gh/manuelbieri/Fumagalli_2020)
[![CodeQL](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/codeql-analysis.yml)
[![Code Style Check](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/Black.yml/badge.svg)](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/Black.yml)
[![CodeFactor](https://www.codefactor.io/repository/github/manuelbieri/fumagalli_2020/badge)](https://www.codefactor.io/repository/github/manuelbieri/fumagalli_2020)
[![GitHub repo size](https://img.shields.io/github/repo-size/manuelbieri/Fumagalli_2020)](https://github.com/manuelbieri/Fumagalli_2020)
[![GitHub license](https://img.shields.io/github/license/manuelbieri/Fumagalli_2020)](https://github.com/manuelbieri/Fumagalli_2020/blob/master/LICENSE)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/manuelbieri/Fumagalli_2020)](https://github.com/manuelbieri/Fumagalli_2020/releases)
![PyPI - Status](https://img.shields.io/pypi/status/Fumagalli-Motta-Tarantino-2020)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Fumagalli-Motta-Tarantino-2020)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/manuelbieri/Fumagalli_2020/HEAD)

### Installation

Install the latest release from [PyPi](https://pypi.org/project/Fumagalli-Motta-Tarantino-2020/):

```shell
$ pip install Fumagalli-Motta-Tarantino-2020
```

Or alternatively, install the package directly from source:

```shell
$ pip install pip install git+https://github.com/manuelbieri/Fumagalli_2020.git
```


### Basic Usage

```python
import Fumagalli_Motta_Tarantino_2020.Models as Model

# initialize the model (here you can adjust the parameters of the model)
model: Model.OptimalMergerPolicy = Model.OptimalMergerPolicy()

# print a summary of the outcome
print(model.summary())
```

A tutorial is included with the notebook tutorial.ipynb.

Find the latest documentation on [manuelbieri.ch/fumagalli_2020](https://manuelbieri.ch/Fumagalli_2020/).

### Dependencies

These packages include all the needed imports for the functionality of this package. The declared version should ensure 
compatibility with [mybinder.org](https://mybinder.org/v2/gh/manuelbieri/Fumagalli_2020/HEAD)

| Package &emsp; | Version &emsp; | Annotation &emsp;                          |
|:---------------|:--------------:|:-------------------------------------------|
| scipy          |     1.7.3      | Always                                     |
| numpy          |     1.21.6     | Always                                     |
| matplotlib     |     3.5.1      | Always                                     |
| black          |     22.1.0     | For consistent code formatting             |
| jupyter        |     1.0.0      | For the demonstration in jupyter Notebooks |
| IPython        |     7.32.0     | For the demonstration in jupyter Notebooks |
| pdoc           |     11.0.0     | To generate the documentation from scratch |

Install the dependencies with the following command (Note: Make sure you are operating in the same directory, where the `requirements.txt` is located.):

```shell
$ pip install -r requirements.txt
```

### Tests

Run the unittests shipped in Fumagalli_Motta_Tarantino_2020.tests with the following command (pay attention to the current working directory):

```shell
$ python -m unittest discover Fumagalli_Motta_Tarantino_2020/tests
```

For explanations about the tests, have a look at [TestCases.md](Fumagalli_Motta_Tarantino_2020/tests/TestCases.md) . See [codecov.io](https://app.codecov.io/gh/manuelbieri/Fumagalli_2020) for a detailed report about the test coverage.

### Generate Documentation
Generate the documentation with the following command:

```shell
$ pdoc -o docs Fumagalli_Motta_Tarantino_2020 --docformat numpy --math
```

or run the shell-script `docs/build.sh` in the terminal.
