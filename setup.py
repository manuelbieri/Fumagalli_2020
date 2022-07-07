from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Fumagalli_Motta_Tarantino_2020",
    packages=find_packages(),
    version="0.5.1",  # change with new version
    license="MIT",
    description="Implements the models presented in Fumagalli et al. (2020)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Manuel Bieri",
    author_email="mail@manuelbieri.ch",
    url="https://github.com/manuelbieri/Fumagalli_2020#readme",
    project_urls={
        "Documentation": "https://manuelbieri.ch/Fumagalli_2020/",
        "Download": "https://github.com/manuelbieri/Fumagalli_2020/releases",
        "Source": "https://github.com/manuelbieri/Fumagalli_2020",
    },
    download_url="https://github.com/manuelbieri/Fumagalli_2020/archive/refs/tags/v0.5.1.tar.gz",  # change with new version
    keywords=["Killer Acquisition", "Competition", "Innovation"],
    classifiers=[
        "Development Status :: 4 - Beta",  # "3 - Alpha" / "4 - Beta" / "5 - Production/Stable"
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=[
        "scipy>=1.8.1",
        "matplotlib>=3.5.2",
        "numpy>=1.22.4",
        "ipython>=7.31.0",
        "jupyter~=1.0.0",
    ],  # change with new version
    extras_require={
        "docs": "pdoc~=12.0.2",
        "style": "SciencePlots>=1.0.9",
        "black": ["black>=22.6.0", "jupyter-black>=0.3.1"],
        "interactive": "ipywidgets>=7.7.1",
    },
    package_data={
        "Fumagalli_Motta_Tarantino_2020.Configurations": ["params.csv"],
        "Fumagalli_Motta_Tarantino_2020.Notebooks": ["*.ipynb"],
    },
    test_suite="Fumagalli_Motta_Tarantino_2020.Tests",
)
