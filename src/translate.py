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

    def _string_fits_in_context(self, text: str):
        tokenized_length = self.tokenizer(text, return_tensors="pt", padding=True)["input_ids"].shape[1]
        print(f"tokenized length: {tokenized_length}, context length: {self.model.config.max_position_embeddings}")
        return tokenized_length < self.model.config.max_position_embeddings


    def _fit_to_context(self, text: str, chunk_lst: list):
        def split_text(text: str):
            print(f"type of text to split: {type(text)}")
            split_idx = text.rfind('. ', 0, int(len(text)/2))
            if split_idx == -1:
                split_idx = text.rfind(' ', 0, int(len(text)/2))
            if split_idx == -1:
                split_idx = int(len(text)/2)
            return text[:split_idx], text[split_idx:]

        if self._string_fits_in_context(text):
            chunk_lst.append(text)
        else:
            sub_text_1, sub_text_2 = split_text(text)
            self._fit_to_context(sub_text_1, chunk_lst)
            self._fit_to_context(sub_text_2, chunk_lst)

    def translate(self, text_input: str) -> str:
        if not isinstance(text_input, str):
            raise TypeError("input must be str.")

        input_chunks = []
        self._fit_to_context(text_input, input_chunks)
        input_chunks = input_chunks

        translated_ids_list = self.model.generate(**self.tokenizer(input_chunks, return_tensors="pt", truncation=True, padding=True))

        output = ""
        for translated_ids in translated_ids_list:

            output += self.tokenizer.decode(list(translated_ids), skip_special_tokens=True)
        return output