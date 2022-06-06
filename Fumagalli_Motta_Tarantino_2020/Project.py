"""
.. include:: ../assets/Structure/README.md
"""
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
