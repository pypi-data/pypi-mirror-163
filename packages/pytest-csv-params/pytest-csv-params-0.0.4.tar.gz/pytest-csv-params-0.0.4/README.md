# pytest-csv-params

A pytest plugin to parametrize tests by CSV files.

## Requirements
 
- Python 3.8, 3.9 or 3.10
- pytest >= 7.1

There's no operating system dependend code in this plugin, so it should run anywhere where pytest runs.

## Installation

Simply install it with pip...

```bash
pip install pytest-csv-params
```

... or poetry ...

```bash
poetry add --dev pytest-csv-params
```

## Usage

Simply decorate your test method with `@csv_params` and the following parameters:

| Parameter    | Type                     | Description                                               | Example                             |
|--------------|--------------------------|-----------------------------------------------------------|-------------------------------------|
| `data_file`  | `str`                    | The CSV file to use, relative or absolute path            | `/var/testdata/test1.csv`           |
| `base_dir`   | `str` (optional)         | Directory to look up relative CSV files (see `data_file`) | `join(dirname(__file__), "assets")` |
| `id_col`     | `str` (optional)         | Column name of the CSV that contains test case IDs        | `ID#`                               |
| `dialect`    | `csv.Dialect` (optional) | CSV Dialect definition (see [1])                          | `csv.excel_tab`                     |
| `data_casts` | `dict` (optional)        | Cast Methods for the CSV Data (see "Data Casting" below)  | `{ "a": int, "b": float }`          |

[1] [Python CSV Documentation](https://docs.python.org/3/library/csv.html#dialects-and-formatting-parameters)

### Data Casting

When data is read from CSV, they are always parsed as `str`. If you need them in other formats, you can set a method that should be called with the value.

These methods can also be lambdas, and are also good for further transformations.

#### Data Casting Example

```python
from pytest_csv_params.decorator import csv_params

def normalize(x: str) -> str:
    return x.strip().upper()

@csv_params(
    data_file="/test/data.csv",
    data_casts={
        "col_x": normalize,
        "col_y": float,
    },
)
def test_something(col_x, col_y):
    # Test something...
    ...
```

### CSV Format

The default CSV format is:

- `\r\n` as line ending
- All non-numeric fields are surrounded by `"`
- If you need a `"` in the value, use `""` (double quote)
- Fields are separated by comma (`,`)

#### Example CSV

```text
"ID#", "part_a", "part_b", "expected_result"
"first", 1, 2, 3
"second", 3, 4, 7
"third", 10, 11, 21
```

### Usage Example

This example uses the CSV example from above.

```python
from pytest_csv_params.decorator import csv_params

@csv_params(
    data_file="/data/test-lib/cases/addition.csv",
    id_col="ID#",
    data_casts={
        "part_a": int,
        "part_b": int,
        "expected_result": int,
    },
)
def test_addition(part_a, part_b, expected_result):
    assert part_a + part_b == expected_result
```

## Contributing

### Build and test

You need [Poetry](https://python-poetry.org/) in order to build this project.

Tests are implemented with `pytest`, and `tox` is used to orchestrate them for the supported python versions. 

- Checkout this repo
- Run `poetry install`
- Run `poetry run tox` (for all supported python versions) or `poetry run pytest` (for your current version)

### Bugs etc.

Please send your issues to `csv-params_issues` (at) `jued.de`. Please include the following:

- Plugin Version used
- Pytest version
- Python version with operating system

It would be great if you could include example code that clarifies your issue.

### Pull Requests

Pull requests are always welcome. Since this Gitea instance is not open to public, just send an e-mail to discuss options.

## License

Code is under MIT license. See `LICENSE.txt` for details.
