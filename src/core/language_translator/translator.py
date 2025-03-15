from mtranslate import translate


def translate_text(text: str, from_lang: str = 'ru', to_lang: str = 'en') -> str:
    """
    Переводит русский текст с одного языка на другой mtranslate.

    Аргументы:
        text: Исходный текст на русском.

    Возвращает:
        Переведенный текст на английском.
    """
    try:
        translation = translate(text, to_lang, from_lang)
        return translation
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return ""


def translate_large_text(text: str, from_lang: str = 'ru', to_lang: str = 'en', chunk_size: int = 1000) -> str:
    """
    Переводит большой текст, разбивая его на части.

    Аргументы:
        text: Исходный текст.
        from_lang: Исходный язык (по умолчанию 'ru').
        to_lang: Целевой язык (по умолчанию 'en').
        chunk_size: Максимальный размер части текста (по умолчанию 1000 символов).

    Возвращает:
        Переведенный текст.
    """
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    translated_chunks = [translate_text(chunk, from_lang, to_lang) for chunk in chunks]
    return " ".join(translated_chunks)