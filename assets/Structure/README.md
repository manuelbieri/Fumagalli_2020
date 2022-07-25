## Project Structure

```
.github
   |-- workflows
   |   |-- Black.yml  # Checks the code style for errors
   |   |-- CodeCov.yml  # Pushes the latest CI results to codecov.io
   |   |-- PyPI.yml  # Publishes releases automatically on PyPI
   |   |-- codeql-analysis.yml  # Checks the code for weaknesses
Fumagalli_Motta_Tarantino_2020  # Package as published on PyPI
   |-- Configurations  # Package to load preset configurations
   |-- Models
   |   |-- Base.py  # Provides the implementation of the base model
   |   |-- BaseExtended.py  # CournotCompetition, EquityContract and PerfectInformation
   |   |-- Distributions.py  # Provides a uniform and normal distribution
   |   |-- Exceptions.py  # Provides useful custom exceptions
   |   |-- Extension.py  # ProCompetitive and ResourceWaste
   |   |-- README.md
   |   |-- Types.py  # Provides Enum (merger policies and bidding types) and dataclasses
   |   |-- __init__.py
   |-- Notebooks
   |   |-- Analysis.ipynb  # Contains an analysis of the models
   |   |-- Configurations.ipynb  # Plots all available configurations
   |   |-- Figures.ipynb  # Generates all figures used in thesis
   |   |-- Interactive.ipynb  # Interactive use of visualizations
   |   |-- NotebookUtilities.py  # Functions used in Notebooks
   |   |-- README.md
   |   |-- Tutorial.ipynb  # Contains a tutorial for the package
   |   |-- __init__.py
   |-- Project.py  # Contains information about the project
   |-- Tests  # Test package, which tests all classes in the main package
   |-- Visualizations
   |   |-- README.md
   |   |-- Visualize.py  # Provides visualization interface and Timeline and payoff plots
   |   |-- VisualizeRanges.py  # Provides plots for ranges and an overview plot
   |   |-- __init__.py
   |-- __init__.py
assets  # Additional ressources regarding the code
   |-- Structure  # Contains informations about the project and code structure
   |   |-- README.md
   |   |-- class_diagram.drawio  # UML class diagram
   |   |-- tree.sh  # Generates this tree of the project structure
   |-- code style  # Scripts for automatic check and enforcement of code style
   |   |-- check_black.sh
   |   |-- run_black.sh
   |-- visual  # Contains graphics
   |   |-- class_diagram.svg
   |   |-- logo.svg
docs  # Automatically generated documentation page with pdoc
   |-- build.sh
CITATION.cff  # Citation of the repository
Extension of Fumagalli et al (2020).pdf
Fumagalli et al (2020) - Shelving or developing.pdf
LICENSE  # MIT
README.md  # Introduction to the repository
requirements.txt  # Dependcies for the repository
setup.py  # Setup script for publication on PyPI
```

Build the folder structure with the following command (or execute `assets/Structure/tree.sh`):

```bash
git config --global alias.tree '! git ls-tree --full-name --name-only -t -r HEAD | sed -e "s/[^-][^\/]*\//   |/g" -e "s/|\([^ ]\)/|-- \1/"'
git tree
```

This command just works for Git - repositories and not for folder structures in general.

## Class diagram

![Class diagram](../visual/class_diagram.svg) (If the class diagram is not shown, follow this [link](https://github.com/manuelbieri/Fumagalli_2020/blob/master/assets/visual/class_diagram.svg))
