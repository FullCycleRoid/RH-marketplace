from time import sleep

from mtranslate import translate


# TODO google API банит за количество запросов
def translate_text(text: str, from_lang: str = "ru", to_lang: str = "en") -> str:
    retry = 0
    while retry < 5:
        try:
            translation = translate(text, to_lang, from_lang)
            return translation
        except Exception as e:
            print(f"Ошибка перевода: {e} retry: {retry}")
            sleep(7)
            retry += 1

    return ""


def translate_large_text(
    text: str, from_lang: str = "ru", to_lang: str = "en", chunk_size: int = 3000
) -> str:
    chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
    translated_chunks = [translate_text(chunk, from_lang, to_lang) for chunk in chunks]
    return " ".join(translated_chunks)
