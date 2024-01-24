import json
from os import PathLike
from pathlib import Path
from typing import Iterator

from src.core.exceptions import InvalidJsonlFile


def iterate_data_jsonl_file(file_path: PathLike) -> Iterator[dict]:
    """Iterator loop over a jsonl file line by line."""
    file_path = Path(file_path)
    with open(file_path, "r") as f:
        for line in f:
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                raise InvalidJsonlFile(
                    f"The file {file_path} does not contain valid jsonl content."
                ) from e
