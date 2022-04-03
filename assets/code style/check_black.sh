printf 'Check Package: ... '
python -m black ./../../Fumagalli_Motta_Tarantino_2020 --diff  --extend-exclude ./../../Notebooks

printf '\n Check Setup.py: ... '
python -m black ./../../setup.py --diff --extend-exclude ./../../Notebooks