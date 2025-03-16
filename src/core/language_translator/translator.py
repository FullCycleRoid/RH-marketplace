from huggingface_hub import snapshot_download
from transformers import MarianTokenizer, MarianMTModel


# TODO google API банит за количество запросов
def translate_text(text: str, from_lang: str = 'ru', to_lang: str = 'en') -> str:
    """
    Переводит русский текст с одного языка на другой mtranslate.

    Аргументы:
        text: Исходный текст на русском.

    Возвращает:
        Переведенный текст на английском.
    """
    from time import sleep

    from mtranslate import translate
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


# def translate_text(text: str, from_lang: str = 'ru', to_lang: str = 'en') -> str:
#
#     model_path = snapshot_download(repo_id=f"Helsinki-NLP/opus-mt-{from_lang}-{to_lang}", cache_dir="./models")
#     tokenizer = MarianTokenizer.from_pretrained(model_path)
#     model = MarianMTModel.from_pretrained(model_path)
#
#     inputs = tokenizer(text, return_tensors="pt", truncation=True)
#     translated = model.generate(**inputs)
#     translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
#
#     return translated_text


def translate_large_text(text: str, from_lang: str = 'ru', to_lang: str = 'en', chunk_size: int = 3000) -> str:
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


# text = "Это текст для перевода мы не превышаем ничего вообще"
# print(translate_text(text))
