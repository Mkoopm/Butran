import json
from os import PathLike
from pathlib import Path
from typing import Iterator

from src.core.exceptions import InvalidJsonlFile


# add generator for jsonl files
def read_jsonl_file(file_path: PathLike) -> Iterator[dict]:
    file_path = Path(file_path)
    with open(file_path, "r") as f:
        for line in f:
            try:
                json_data = json.loads(line)
                yield json_data
            except json.JSONDecodeError as e:
                raise InvalidJsonlFile(
                    f"The file {file_path} does not contain valid jsonl content."
                ) from e
