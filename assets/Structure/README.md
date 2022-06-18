## Project Structure

Build the folder structure with the following command (or execute `assets/Structure/tree.sh`):

```bash
git config --global alias.tree '! git ls-tree --full-name --name-only -t -r HEAD | sed -e "s/[^-][^\/]*\//   |/g" -e "s/|\([^ ]\)/|-- \1/"'
git tree
```

This command just works for Git - repositories and not for folder structures in general.


This is the annotated folder structure:
```
.github
   |-- workflows
   |   |-- Black.yml  # Checks the code style on errors
   |   |-- CodeCov.yml  # Pushes the newest CI results to codecov.io
   |   |-- PyPI.yml  # Publishes releases automatically on PyPI
   |   |-- codeql-analysis.yml  # Checks for weaknesses in code
Fumagalli_Motta_Tarantino_2020  # Package as published on PyPI
   |-- Configurations  # Package to load preset configurations
   |-- Notebooks
   |   |-- Analysis.ipynb  # Contains a narrative analysis of the models
   |   |-- Configurations.ipynb  # Plots all preset configurations
   |   |-- Figures.ipynb  # Generates all figures used in thesis
   |   |-- Tutorial.ipynb  # Contains a tutorial for the package
   |   |-- __init__.py
   |-- tests  # Test package, which tests all classes in the main package
   |-- AdditionalModels.py  # Models: CournotCompetition, EquityContract and PerfectInformation
   |-- Distributions.py  # Provides a uniform and normal distribution (respective their cumulative function and inverse)
   |-- Exceptions.py  # Provides useful custom exceptions
   |-- ExtensionModels.py  # Models: ProCompetitive and ResourceWaste
   |-- Models.py  # Provides the implementation of the base model
   |-- Project.py  # Contains information about the project
   |-- Types.py  # Provides Enum (merger policies and bidding types) and dataclasses
   |-- Visualize.py  # Provides visualization interface and Timeline and payoff plots
   |-- VisualizeRanges.py  # Provides plots for ranges and an overview plot
   |-- __init__.py
assets  # Additional ressources regarding the code
   |-- Structure  # Contains informations about the project and code structure
   |   |-- README.md  # This file
   |   |-- class_diagram.drawio  # UML class diagram
   |   |-- tree.sh  # Generates this tree of the project structure
   |-- code style  # Bash scripts for automatic check and enforcement of code style
   |   |-- check_black.sh
   |   |-- run_black.sh
   |-- visual  # Contains graphics
   |   |-- class_diagram.svg
   |   |-- logo.svg
docs  # Contains the files for the documentation page (automatically generated with pdoc)
   |-- build.sh  # Bash script for automatic build of documentation
CITATION.cff  # Citation of the repository
Fumagalli et al (2020) - Shelving or developing The Aquisition of potential competitors under financial constraints.pdf
LICENSE  # MIT
README.md  # Introduction to the repository
requirements.txt  # Dependcies for the repository
setup.py  # Setup script for publication on PyPI
```

## Class diagram

![Class diagram](../visual/class_diagram.svg) (If the class diagram is not shown, follow this [link](https://github.com/manuelbieri/Fumagalli_2020/blob/master/assets/visual/class_diagram.svg))


## Code style

As default code style [Black](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) is used and
automatically checked and enforced by GitHub - workflows.
