from abc import ABCMeta, abstractmethod


class Translator(metaclass=ABCMeta):
    """Abstract class that defines the interface of a 'translator'. 
    
    A translator should be initiated with an input and output language and
    be able to translate a list of strings from the input to output language.
    """
    @abstractmethod
    def __init__(self, language_from: str, language_to: str) -> None:
        pass

    @abstractmethod
    def translate(self, text_input: str) -> str:
        pass


class TranslatorMarianMT(Translator):
    def __init__(self, language_from: str, language_to: str) -> None:
        from transformers import MarianMTModel, MarianTokenizer

        model_name = f"Helsinki-NLP/opus-mt-{language_from}-{language_to}"
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)

    def translate(self, text_input: list[str]) -> list[str]:
        translated = self.model.generate(**self.tokenizer(text_input, return_tensors="pt", padding=True))
        return [self.tokenizer.decode(t, skip_special_tokens=True) for t in translated]
