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
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/manuelbieri/fmt20web/fmt20_app.py)

### Installation

Install the latest release from [PyPi](https://pypi.org/project/Fumagalli-Motta-Tarantino-2020/):

```shell
$ pip install Fumagalli-Motta-Tarantino-2020
```
Or alternatively, install this package directly from source:

```shell
$ pip install git+https://github.com/manuelbieri/Fumagalli_2020.git
```


### Basic Usage

```python
import Fumagalli_Motta_Tarantino_2020 as FMT20

# initialize the model (here you can adjust the parameters of the model)
# all other models conform to the interface defined in FMT20.OptimalMergerPolicy
model: FMT20.OptimalMergerPolicy = FMT20.OptimalMergerPolicy()

# print a summary of the outcome
print(model.summary())

# plot a model overview
FMT20.Overview(model).show()

# open API-documentation
FMT20.docs()

# open GitHub-repository
FMT20.repo()
```

A tutorial is included with the notebook Tutorial.ipynb. Additionally, find the latest documentation including all the details on [manuelbieri.ch/fumagalli_2020](https://manuelbieri.ch/Fumagalli_2020/).

Note: mybinder.org is currently not supported, since this package needs at least python 3.9.

### Dependencies

Install the dependencies with the following command (Note: Make sure you are operating in the same directory, where the 
`requirements.txt` is located.):

```shell
$ pip install -r requirements.txt
```

### Tests

Run the unittests shipped in Fumagalli_Motta_Tarantino_2020.Tests with the following command (pay attention to the current working directory):

```shell
$ python -m unittest discover Fumagalli_Motta_Tarantino_2020.Tests
```

For explanations about the tests, have a look at Fumagalli_Motta_Tarantino_2020.Tests. See [codecov.io](https://app.codecov.io/gh/manuelbieri/Fumagalli_2020) for a detailed report about the test coverage.

### Generate Documentation
Generate the documentation with the following command:

```shell
$ pdoc -o docs Fumagalli_Motta_Tarantino_2020 --docformat numpy --math
```

or run the shell-script `docs/build.sh` in the terminal.
