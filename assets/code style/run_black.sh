printf 'Format Package: ... '
python -m black ./../../Fumagalli_Motta_Tarantino_2020

printf '\n Format Setup.py: ... '
python -m black ./../../setup.py --extend-exclude ./../../Fumagalli_Motta_Tarantino_2020