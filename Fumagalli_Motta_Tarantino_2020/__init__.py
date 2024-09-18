"""
.. include:: ../README.md
"""

from Fumagalli_Motta_Tarantino_2020.Models import *

from Fumagalli_Motta_Tarantino_2020.Configurations import *
from Fumagalli_Motta_Tarantino_2020.Visualizations import *
from Fumagalli_Motta_Tarantino_2020.Project import *

import Fumagalli_Motta_Tarantino_2020.Models.Exceptions as Exceptions
import Fumagalli_Motta_Tarantino_2020.Models.Distributions as Distributions
import Fumagalli_Motta_Tarantino_2020.Notebooks.NotebookUtilities as NotebookUtilities
import webbrowser


def docs() -> bool:
    """
    Opens the API documentation in the browser.
    """
    return webbrowser.open("https://manuelbieri.ch/Fumagalli_2020")


def repo() -> bool:
    """
    Opens the Git - repository in the browser.
    """
    return webbrowser.open("https://github.com/manuelbieri/Fumagalli_2020")
