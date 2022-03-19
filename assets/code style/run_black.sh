printf 'Format Package: ... '
python -m black ./../../Fumagalli_Motta_Tarantino_2020 --line-length 120 --extend-exclude ./../../Notebooks

printf '\n Format Tests: ... '
python -m black ./../../Test_Fumagalli_Motta_Tarantino_2020 --line-length 120 --extend-exclude ./../../Notebooks

printf '\n Format Setup.py: ... '
python -m black ./../../setup.py --line-length 120 --extend-exclude ./../../Notebooks