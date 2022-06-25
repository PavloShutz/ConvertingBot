from typing import AnyStr

from googletrans import Translator  # type: ignore


class Localization:

    def translate_to_language(self, text: str, language: str) -> str:
        """Translating input text to the given language"""
        return Translator().translate(text, dest=language).text


    def get_language_key(self, input_dict: dict, value: AnyStr) -> str:
        """Getting key from LANGUAGES by value"""
        for key, val in input_dict.items():
            if value == val:
                return key
        return "No such a key"
