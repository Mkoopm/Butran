import warnings
from abc import ABCMeta, abstractmethod

import torch

torch.set_grad_enabled(False)


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
    def __init__(
        self, language_from: str, language_to: str, max_context_frac: float = 1.0
    ) -> None:
        from transformers import MarianMTModel, MarianTokenizer  # type: ignore

        model_name = f"Helsinki-NLP/opus-mt-{language_from}-{language_to}"
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            self.model = MarianMTModel.from_pretrained(model_name)
        self.max_input_length = int(
            max_context_frac * self.model.config.max_position_embeddings
        )

    def _string_fits_in_context(self, text: str):
        text_tokenized = self.tokenizer(
            text,
            return_tensors="pt",
            padding="max_length",
            max_length=self.max_input_length,
            return_overflowing_tokens=True,
            return_length=True,
        )
        return bool(text_tokenized["length"] <= self.max_input_length)

    def _to_list_of_context_fitting_strings(self, text: str) -> list[str]:
        tokenized = self.tokenizer.tokenize(text)

        # one token gets added during processing
        target_length = self.max_input_length - 1

        result_list = []
        if len(tokenized) <= target_length:
            string_form = self.tokenizer.convert_tokens_to_string(tokenized)
            result_list.append(string_form)

        while len(tokenized) > target_length:
            tokens_fit, tokens_remainder = (
                tokenized[:target_length],
                tokenized[target_length:],
            )

            string_to_split = self.tokenizer.convert_tokens_to_string(tokens_fit)

            sub_str_to_find = ". "
            split_idx = text.rfind(sub_str_to_find)
            if split_idx == -1:
                sub_str_to_find = ", "
                split_idx = text.rfind(sub_str_to_find)
            if split_idx == -1:
                sub_str_to_find = " "
                split_idx = text.rfind(sub_str_to_find)
            if split_idx == -1:
                result_list.append(string_to_split)
            else:
                result_list.append(string_to_split[: split_idx + len(sub_str_to_find)])
            tokenized = self.tokenizer.tokenize(
                string_to_split[split_idx + len(sub_str_to_find) :]
                + self.tokenizer.convert_tokens_to_string(tokens_remainder)
            )
        return result_list

    def translate(self, text_input: str) -> str:
        if not isinstance(text_input, str):
            raise TypeError("input must be str.")

        input_chunks = self._to_list_of_context_fitting_strings(text_input)

        translated_ids_list = self.model.generate(
            **self.tokenizer(
                input_chunks,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=self.model.config.max_position_embeddings,
            )
        )

        output = ""
        for translated_ids in translated_ids_list:

            output += self.tokenizer.decode(
                list(translated_ids), skip_special_tokens=True
            )
        return output
