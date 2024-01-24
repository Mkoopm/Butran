import pytest

from src.core.exceptions import InvalidJsonlFile
from src.data_io import read_jsonl_file


@pytest.fixture()
def jsonl_test_data_path() -> str:
    return "tests/resources/jsonl_test_data.jsonl"


@pytest.fixture()
def jsonl_test_invalid_data_path() -> str:
    return "tests/resources/jsonl_test_data_invalid.jsonl"


def test_read_jsonl_file(jsonl_test_data_path):
    expected_keys = ["_id", "title", "text", "metadata"]
    data_list = []
    for data in read_jsonl_file(jsonl_test_data_path):
        data_list.append(data)

    assert len(data_list) == 2

    assert list(data_list[0].keys()) == expected_keys


def test_read_jsonl_invalid_file(jsonl_test_invalid_data_path):
    with pytest.raises(InvalidJsonlFile):
        for data in read_jsonl_file(jsonl_test_invalid_data_path):
            pass
