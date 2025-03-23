import html
import random
import re
import time
import urllib.parse
import urllib.request
from typing import List

from pipelines.utils import get_random_proxy_obj

agent = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def translate(
    to_translate, from_language="auto", to_language="auto", proxy_obj=None, retries=3
):
    """Улучшенная функция перевода с обработкой ошибок и повторными попытками"""
    base_link = "https://translate.google.com/m?tl=%s&sl=%s&q=%s"

    for attempt in range(retries):
        try:
            # Создаем прокси-хендлер
            proxy_handler = urllib.request.ProxyHandler(proxy_obj or {})
            opener = urllib.request.build_opener(proxy_handler)

            # Кодируем текст и формируем URL
            encoded_text = urllib.parse.quote(to_translate)
            url = base_link % (to_language, from_language, encoded_text)

            # Случайная задержка между запросами
            time.sleep(random.uniform(1.5, 3.5))

            # Выполняем запрос
            request = urllib.request.Request(url, headers=agent)
            with opener.open(request, timeout=10) as response:
                raw_data = response.read()
                data = raw_data.decode("utf-8")

                # Ищем результат перевода
                expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
                re_result = re.findall(expr, data)

                if re_result:
                    return html.unescape(re_result[0])
                return ""

        except Exception as e:
            print(f"Attempt {attempt+1} failed: {str(e)}")
            if attempt == retries - 1:
                raise
            time.sleep(2**attempt)


def translate_large_text(
    text: str,
    from_lang: str = "ru",
    to_lang: str = "en",
    chunk_size: int = 4000,
    proxy_obj=None,
) -> str:
    chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
    translated_chunks = [
        translate(chunk, from_lang, to_lang, proxy_obj) for chunk in chunks
    ]
    return " ".join(translated_chunks)


# if __name__ == "__main__":
#     def load_proxies(file_path: str) -> List[str]:
#         with open(file_path, 'r') as f:
#             lines = f.readlines()
#             return [f"https://{proxy.strip()}" for proxy in lines]
#
#     try:
#         load_proxies = load_proxies("../../../proxylist.txt")
#         pr = get_random_proxy_obj(load_proxies)
#         result = translate(
#             "Hello world",
#             to_language="ru",
#             from_language="en",
#             proxies=pr
#         )
#         print("Перевод:", result)
#     except Exception as e:
#         print("Final error:", str(e))
