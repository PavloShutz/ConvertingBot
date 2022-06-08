from googletrans import Translator


def translate_to_language(text: str, language: str) -> str:
    return Translator().translate(text, dest=language).text
