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
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://manuelbieri-fmt20web-fmt20-app-hryht2.streamlitapp.com/)

This package implements the models presented in [Fumagalli et al. (2020)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3674889) (note, that the version from 2020 is implemented).
Additionally, extensions from the models are explained in [Extension of Fumagalli et al (2020).pdf](https://github.com/manuelbieri/Fumagalli_2020/blob/master/Extension%20of%20Fumagalli%20et%20al%20(2020).pdf).

## Installation

You can either [install the package](#Package) (functionality only) or [download the whole repository](#Repository) (with documentation and assets).

<h3 id="Package">Package</h3>

Install the latest release from [PyPi](https://pypi.org/project/Fumagalli-Motta-Tarantino-2020/):

```shell
$ pip install Fumagalli-Motta-Tarantino-2020
```
Or install this package directly from source:

```shell
$ pip install git+https://github.com/manuelbieri/Fumagalli_2020.git
```
The necessary dependencies are automatically installed during the setup.

<h3 id="Repository">Repository</h3>

If you would like to get the whole repository, download it [here](https://github.com/manuelbieri/Fumagalli_2020/archive/refs/heads/master.zip)
or clone it with GIT (requires GIT installation):
```shell
$ git clone https://github.com/manuelbieri/Fumagalli_2020.git
```

Install the dependencies for the repository with the following command (Note: Make sure you are operating in the same directory, where the 
`requirements.txt` is located.):

```shell
$ pip install -r requirements.txt
```

Note: This package requires a working latex installation for the plots!

## Basic Usage

```python
import Fumagalli_Motta_Tarantino_2020 as FMT20

# initialize the model (here you can adjust the parameters of the model)
# all other models conform to the interface defined in FMT20.OptimalMergerPolicy
model: FMT20.OptimalMergerPolicy = FMT20.OptimalMergerPolicy()

# print a summary of the outcome
print(model.summary())

# plot a model overview
FMT20.Overview(model).show()

# open the API-documentation
FMT20.docs()

# open the GitHub-repository
FMT20.repo()
```

A tutorial is included with the notebook Tutorial.ipynb. Additionally, find the latest documentation including all the details on [manuelbieri.ch/fumagalli_2020](https://manuelbieri.ch/Fumagalli_2020/).

Note: mybinder.org is currently not supported, since this package needs at least python 3.9.

## Overview

This sections provides a quick overview for this repository.

### Assets

Additional files about the code style (scripts), class diagram and a more detailed project overview (Fumagalli_Motta_Tarantino_2020.Project).

### Docs

Contains the files of the [automatically](#docs) generated API - documentation

### Fumagalli_Motta_Tarantino_2020

Contains the actual code of the package. See Fumagalli_Motta_Tarantino_2020.Models and Fumagalli_Motta_Tarantino_2020.Visualizations for
the available models and visualization options. In Fumagalli_Motta_Tarantino_2020.Notebooks are some jupyter notebooks included 
(e.g., Interactive.ipynb or Tutorial.ipynb).

## Tests

Run the unittests shipped in Fumagalli_Motta_Tarantino_2020.Tests with the following command (pay attention to the current working directory):

```shell
$ python -m unittest discover Fumagalli_Motta_Tarantino_2020.Tests
```

For explanations about the tests, have a look at Fumagalli_Motta_Tarantino_2020.Tests. See [codecov.io](https://app.codecov.io/gh/manuelbieri/Fumagalli_2020) for a detailed report about the test coverage.

## Code style

As the default code style [Black](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) is used and
automatically checked and enforced by GitHub - workflows. To run black in the terminal either run `assets/code style/run_black.sh` or use the following command:
```shell
$ python -m black ./Fumagalli_Motta_Tarantino_2020
```
This command modifies the source code if the preset rules are not met. You can as well just check, whether the rules are met or not with `assets/code style/check_black.sh` or:
```shell
$ python -m black ./../../Fumagalli_Motta_Tarantino_2020 --diff
```

<h2 id="docs">Generate Documentation</h2>
Generate the documentation with the following command (as always be aware of the working directory):

```shell
$ pdoc -o docs Fumagalli_Motta_Tarantino_2020 --docformat numpy --math
```

or run the shell-script `docs/build.sh` in the terminal.
