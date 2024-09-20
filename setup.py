from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Fumagalli_Motta_Tarantino_2020",
    packages=find_packages(),
    version="1.0.2",  # adjust
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
    download_url="https://github.com/manuelbieri/Fumagalli_2020/archive/refs/tags/v1.0.2.tar.gz",  # adjust
    keywords=["Killer Acquisition", "Competition", "Innovation"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",  # "3 - Alpha" / "4 - Beta" / "5 - Production/Stable"
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=[
        "scipy>=1.14.1",
        "matplotlib>=3.9.2",
        "numpy>=2.1.1",
        "ipython>=8.27.0",
        "jupyter~=1.1.1",
        "mockito~=1.5.1",
        "ipympl==0.9.4",
    ],  # adjust
    extras_require={
        "docs": "pdoc~=14.7.0",
        "style": "SciencePlots>=1.0.9",
        "black": ["black>=24.8.0", "jupyter-black>=0.4.0"],
        "interactive": "ipywidgets>=7.8.4",
    },
    package_data={
        "Fumagalli_Motta_Tarantino_2020.Configurations": ["params.csv"],
        "Fumagalli_Motta_Tarantino_2020.Notebooks": ["*.ipynb"],
    },
    test_suite="Fumagalli_Motta_Tarantino_2020.Tests",
)
