import json
from os import PathLike
from pathlib import Path

import argh
import tqdm

from src.core.exceptions import InvalidDelimiterError
from src.data_io import iterate_data_jsonl_file
from src.translate import TranslatorMarianMT

delimiter = ","


@argh.arg(
    "keys_to_translate",
    help=f"delimiter separated list of keys to translate (default '{delimiter}').",
)
def main(
    input_file: PathLike,
    output_file: PathLike,
    keys_to_translate: str,
    delimiter: str = delimiter,
    language_from: str = "en",
    language_to: str = "nl",
):
    """Read a jsonl file and translate the selected entries."""
    input_file = Path(input_file)
    output_file = Path(output_file)
    with open(input_file) as fp_in:
        nr_lines = len([None for line in fp_in])

    if len(delimiter) != 1:
        raise InvalidDelimiterError(
            f"the chosen delimiter '{delimiter}' not a 1 character delimiter."
        )

    keys_to_translate_list = keys_to_translate.split(delimiter)

    translator = TranslatorMarianMT(language_from, language_to)

    with open(output_file, "w") as fp_out:
        for data in tqdm.tqdm(iterate_data_jsonl_file(input_file), total=nr_lines):
            for key in keys_to_translate_list:
                data[key] = translator.translate(data[key])
            fp_out.write(json.dumps(data) + "\n")


if __name__ == "__main__":
    argh.dispatch_command(main)
