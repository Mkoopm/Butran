import pytest
from src.translate import Translator, TranslatorMarianMT


@pytest.fixture
def marianmt_translator_en_nl():
    return TranslatorMarianMT("en", "nl")


def test_init_Translator_ABC_raises() -> None:
    with pytest.raises(TypeError):
        translator = Translator()


def test_init_marianMT_translator() -> None:
    marianmt_translator = TranslatorMarianMT("en", "nl")
    assert isinstance(marianmt_translator, TranslatorMarianMT)


def test_marianmt_translator_translate(marianmt_translator_en_nl: TranslatorMarianMT) -> None:
    assert marianmt_translator_en_nl.translate(["the"]) == ["de"]