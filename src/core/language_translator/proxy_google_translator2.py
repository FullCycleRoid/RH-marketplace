import re
import html
import urllib.request
import urllib.parse
import time
import random

agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

proxy_settings = {
    # 'http': 'http://wrnl5p:TRV0Gp5lAw@94.158.190.51:1050',
    'https': 'https://wrnl5p:TRV0Gp5lAw@94.158.190.51:1050'
}

def translate(to_translate, from_language="auto", to_language="auto", proxies=None, retries=3):
    """Улучшенная функция перевода с обработкой ошибок и повторными попытками"""
    base_link = "https://translate.google.com/m?tl=%s&sl=%s&q=%s"

    for attempt in range(retries):
        try:
            # Создаем прокси-хендлер
            proxy_handler = urllib.request.ProxyHandler(proxies or {})
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
            time.sleep(2 ** attempt)


def translate_large_text(
        text: str, from_lang: str = "ru", to_lang: str = "en", chunk_size: int = 4000
) -> str:
    chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
    translated_chunks = [translate(chunk, from_lang, to_lang) for chunk in chunks]
    return " ".join(translated_chunks)


if __name__ == "__main__":
    try:
        result = translate(
            "Hello world",
            to_language="ru",
            from_language="en",
            proxies=proxy_settings
        )
        print("Перевод:", result)
    except Exception as e:
        print("Final error:", str(e))
#
#     def try_proxy():
#         try:
#             proxy_handler = urllib.request.ProxyHandler(proxy_settings)
#             opener = urllib.request.build_opener(proxy_handler)
#             opener.open("http://httpbin.org/ip", timeout=10)
#             print("Proxy working!")
#         except Exception as e:
#             print("Proxy error:", str(e))
#
#     try_proxy()