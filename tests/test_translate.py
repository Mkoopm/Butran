import pytest

from src.translate import TranslatorMarianMT
from tests.resources import example_text


@pytest.fixture
def marianmt_translator_en_nl():
    return TranslatorMarianMT("en", "nl")


def test_init_marianMT_translator() -> None:
    marianmt_translator = TranslatorMarianMT("en", "nl")
    assert isinstance(marianmt_translator, TranslatorMarianMT)


def test_marianmt_translator_translate(
    marianmt_translator_en_nl: TranslatorMarianMT,
) -> None:
    assert marianmt_translator_en_nl.translate("the") == "de"


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (example_text.long_english_text, False),
        ("Example text.", True),
    ],
)
def test_long_text_fits_in_context_length(
    marianmt_translator_en_nl: TranslatorMarianMT,
    input_text: str,
    expected_output: bool,
) -> None:
    assert (
        marianmt_translator_en_nl._string_fits_in_context(input_text) is expected_output
    )


@pytest.mark.parametrize("input_text", [example_text.difficult_case_1])
def test_to_list_of_context_fitting_strings(
    marianmt_translator_en_nl: TranslatorMarianMT,
    input_text: str,
) -> None:
    output_list: list = []
    output_list = marianmt_translator_en_nl._to_list_of_context_fitting_strings(
        input_text
    )
    fit_of_sub_result = [
        marianmt_translator_en_nl._string_fits_in_context(text_part)
        for text_part in output_list
    ]

    assert len(fit_of_sub_result) > 0
    assert all(fit_of_sub_result)


@pytest.mark.parametrize(
    "input_text", (example_text.long_english_text, example_text.difficult_case_1)
)
def test_translate_text(
    marianmt_translator_en_nl: TranslatorMarianMT,
    input_text: str,
) -> None:
    translation = marianmt_translator_en_nl.translate(input_text)

    assert isinstance(translation, str)
