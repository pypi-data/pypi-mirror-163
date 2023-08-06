"""
Parametrize a test function by CSV file
"""
import csv
from pathlib import Path
from typing import List, Optional, TypedDict

import pytest

from _ptcsvp.plugin import BASE_DIR_KEY, Plugin
from pytest_csv_params.dialect import CsvParamsDefaultDialect
from pytest_csv_params.exception import (
    CsvParamsDataFileInaccessible,
    CsvParamsDataFileInvalid,
    CsvParamsDataFileNotFound,
)
from pytest_csv_params.types import BaseDir, CsvDialect, DataCastDict, DataFile, IdColName


class TestCaseParameters(TypedDict):
    """
    Type for Test Case
    """

    test_id: Optional[str]
    data: List


def read_csv(base_dir: BaseDir, data_file: DataFile, dialect: CsvDialect):
    """
    Get Data from CSV
    """

    if data_file is None:
        raise CsvParamsDataFileInvalid("Data file is None") from None
    csv_file = Path(data_file)
    if not csv_file.is_absolute():
        if base_dir is not None:
            csv_file = Path(base_dir) / csv_file
    if not csv_file.exists() or not csv_file.is_file():
        raise CsvParamsDataFileNotFound(f"Cannot find file: {str(csv_file)}") from None
    csv_lines = []
    try:
        with open(csv_file, newline="", encoding="utf-8") as csv_file_handle:
            csv_reader = csv.reader(csv_file_handle, dialect=dialect)
            for row in csv_reader:
                csv_lines.append(row)
    except IOError as err:  # pragma: no cover
        raise CsvParamsDataFileInaccessible(f"Unable to read file: {str(csv_file)}") from err
    except csv.Error as err:
        raise CsvParamsDataFileInvalid("Invalid data") from err
    return csv_lines


def add_parametrization(
    base_dir: BaseDir = None,
    data_file: DataFile = None,
    id_col: IdColName = None,
    data_casts: DataCastDict = None,
    dialect: CsvDialect = CsvParamsDefaultDialect,
):
    """
    Get data from the files and add things to the tests
    """
    if base_dir is None:
        base_dir = getattr(Plugin, BASE_DIR_KEY, None)
    csv_lines = read_csv(base_dir, data_file, dialect)
    if len(csv_lines) < 2:
        raise CsvParamsDataFileInvalid("File does not contain a single data row") from None
    id_index = -1
    headers = csv_lines.pop(0)
    if id_col is not None:
        try:
            id_index = headers.index(id_col)
            del headers[id_index]
        except ValueError as err:
            raise CsvParamsDataFileInvalid(f"Cannot find ID column '{id_col}'") from err
    if len(headers) == 0:
        raise CsvParamsDataFileInvalid("File seems only to have IDs") from None
    data: List[TestCaseParameters] = []
    for data_line in csv_lines:
        line = list(map(str, data_line))
        if len(line) == 0:
            continue
        test_id = None
        if id_index >= 0:
            test_id = line.pop(id_index)
        if len(headers) != len(line):
            raise CsvParamsDataFileInvalid("Header and Data length mismatch") from None
        if data_casts is not None:
            for index, header in enumerate(headers):
                caster = data_casts.get(header, None)
                if caster is not None:
                    line[index] = caster(str(line[index]))
        data.append(
            {
                "test_id": test_id,
                "data": line,
            }
        )
    id_data = None
    if id_col is not None:
        id_data = [tc_data["test_id"] for tc_data in data]
    return pytest.mark.parametrize(headers, [tc_data["data"] for tc_data in data], ids=id_data)
