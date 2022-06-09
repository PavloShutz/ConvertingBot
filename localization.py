from googletrans import Translator  # type: ignore


def translate_to_language(text: str, language: str) -> str:
    return Translator().translate(text, dest=language).text
