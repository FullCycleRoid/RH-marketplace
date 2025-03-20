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


text = """
Современный мир стремительно развивается, и технологии играют ключевую роль в этом процессе. Каждый день мы сталкиваемся с новыми изобретениями, которые делают нашу жизнь проще и удобнее. Одним из самых значимых достижений последних лет является искусственный интеллект. Он используется в различных сферах: от медицины до финансов, от образования до развлечений. ИИ помогает врачам ставить точные диагнозы, банкам — выявлять мошенничество, а обычным пользователям — находить нужную информацию за считанные секунды.

Однако развитие технологий также вызывает и определенные опасения. Многие люди боятся, что роботы и автоматизация лишат их рабочих мест. Действительно, некоторые профессии могут исчезнуть, но на их место придут новые, требующие других навыков. Важно адаптироваться к изменениям и постоянно учиться, чтобы оставаться востребованным специалистом.

Еще одной важной темой является экология. Технологический прогресс часто сопровождается увеличением потребления ресурсов и загрязнением окружающей среды. Однако и здесь технологии могут стать решением. Например, солнечные батареи и ветряные электростанции помогают сократить выбросы углекислого газа, а умные системы управления энергией позволяют оптимизировать ее использование.

В заключение можно сказать, что технологии — это мощный инструмент, который может как улучшить нашу жизнь, так и создать новые вызовы. Главное — использовать их с умом и заботиться о будущем нашей планеты.
"""
# concurrent_requests = 30  # Можно изменить на 20 или 100
#
# # Счетчик попыток
# tries = 0
#
# # Функция для выполнения запросов
# def make_request():
#     global tries
#     res = translate_text(text)
#     tries += 1
#     print(f"Try {tries}: {res[:50]}")
#
# import concurrent.futures
# with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
#     # Запускаем задачи
#     futures = [executor.submit(make_request) for _ in range(100000)]  # 100 запросов
#
#     # Ожидаем завершения всех задач
#     for future in concurrent.futures.as_completed(futures):
#         future.result()