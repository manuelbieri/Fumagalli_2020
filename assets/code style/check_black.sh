printf 'Check Package: ... '
python -m black ./../../Fumagalli_Motta_Tarantino_2020 --line-length 120 --diff  --extend-exclude ./../../Notebooks

printf '\n Check Tests: ... '
python -m black ./../../Test_Fumagalli_Motta_Tarantino_2020 --line-length 120 --diff  --extend-exclude ./../../Notebooks

printf '\n Check Setup.py: ... '
python -m black ./../../setup.py --line-length 120 --diff --extend-exclude ./../../Notebooks