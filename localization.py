from googletrans import Translator  # type: ignore


def translate_to_language(text: str, language: str) -> str:
    """Translating input text to the given language"""
    return Translator().translate(text, dest=language).text
