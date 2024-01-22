import pytest
from src.translate import Translator, TranslatorMarianMT
from tests.resources import example_text


@pytest.fixture
def marianmt_translator_en_nl():
    return TranslatorMarianMT("en", "nl")


def test_init_Translator_ABC_raises() -> None:
    with pytest.raises(TypeError):
        translator = Translator("en", "nl")


def test_init_marianMT_translator() -> None:
    marianmt_translator = TranslatorMarianMT("en", "nl")
    assert isinstance(marianmt_translator, TranslatorMarianMT)


def test_marianmt_translator_translate(marianmt_translator_en_nl: TranslatorMarianMT) -> None:
    assert marianmt_translator_en_nl.translate("the") == "de"


def test_fits_in_context_length(marianmt_translator_en_nl: TranslatorMarianMT) -> None:
    assert marianmt_translator_en_nl._string_fits_in_context(example_text.long_english_text) is False


def test_translate_text_longer_than_context_length(marianmt_translator_en_nl: TranslatorMarianMT) -> None:
    translation = marianmt_translator_en_nl.translate(example_text.long_english_text)
    print("reached")
    assert isinstance(translation, str)