![CI](https://github.com/manuelbieri/Fumagalli_2020/actions/workflows/CI.yml/badge.svg)

### Basic Usage

```python
import Fumagalli_Motta_Tarantino_2020.Model as Model

model: Model.BaseModel = Model.BaseModel()
```

### Dependencies

These packages include all the needed imports for the functionality of this package.

| Package &emsp; | Version &emsp; | Annotation &emsp;                               |
|:---------------|:--------------:|:------------------------------------------------|
| scipy          |     1.8.0      | Always needed                                   |
| numpy          |     1.22.3     | Always needed                                   |
| jupyter        |     1.0.0      | Just for the demonstration in demo.ipynb        |
| IPython        |     8.1.1      | Just for the demonstration in demo.ipynb        |
| pdoc           |     10.0.3     | Only to generate the documentation from scratch |

Install the dependencies with the following command:

```shell
$ pip install -r requirements.txt
```
(Note: Make sure you are operating in the same directory, where the `requirements.txt` is located.)

### Generate Documentation
Generate the documentation with the following command:

```shell
$ pdoc -o docs Fumagalli_Motta_Tarantino_2020 --docformat numpy --math
```

or run the shell-script `docs.sh` in the terminal.
