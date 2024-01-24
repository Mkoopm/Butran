import warnings
from os import PathLike

import argh

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
    keys_to_translate: str,
    delimiter: str = delimiter,
    language_from: str = "en",
    language_to: str = "nl",
):
    """Read a jsonl file and translate the selected entries."""
    if len(delimiter) != 1:
        raise InvalidDelimiterError(
            f"the chosen delimiter '{delimiter}' not a 1 character delimiter."
        )

    keys_to_translate_list = keys_to_translate.split(delimiter)

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        translator = TranslatorMarianMT(language_from, language_to)

    for data in iterate_data_jsonl_file(input_file):
        for key in keys_to_translate_list:
            data[key] = translator.translate(data[key])
        print(data)


if __name__ == "__main__":
    argh.dispatch_command(main)
