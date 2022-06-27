from typing import AnyStr

from googletrans import Translator  # type: ignore


class Localization:
    """Makes simple and fast localization."""

    @staticmethod
    def translate_to_language(text: str, language: str) -> str:
        """Translating input text to the given language.
        Args:
            text (str): input text to translate.
            language (str): language to translate text to.
        Returns:
            translated text.
        """
        return Translator().translate(text, dest=language).text

    @staticmethod
    def get_language_key(input_dict_of_languages: dict, value: AnyStr) -> str:
        """Getting key from LANGUAGES by value.
        Args:
            input_dict_of_languages (dict):
                    input dict of languages for searching in.
            value (AnyStr): the searched language value.
        Returns:
            language value if language input is valid.
        """
        for key, val in input_dict_of_languages.items():
            if value == val:
                return key
        return "No such a key"
