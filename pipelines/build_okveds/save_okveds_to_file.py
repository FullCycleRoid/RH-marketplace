import os

from pipelines.utils import get_company_okved
import pickle


BATCH_SIZE = 1_000_000

def start_process():
    offset = 0
    company_count = 20_000_000
    unique_okveds = dict()

    while offset <= company_count:
        batch = get_company_okved(offset, BATCH_SIZE)
        for code_set in batch:
            if code_set[0]:
                for code, description in code_set[0].items():
                    if code not in unique_okveds:
                        unique_okveds[code] = description

        filename = "okved_data.pkl"

        # Загружаем существующие данные, если файл существует
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                existing_data = pickle.load(file)
        else:
            existing_data = {}

        # Обновляем данные (добавляем новые элементы)
        existing_data.update(unique_okveds)

        # Сохраняем обновлённые данные обратно в файл
        with open(filename, "wb") as file:
            pickle.dump(existing_data, file)

        offset += BATCH_SIZE
        print("Offset", offset, "Count:", len(unique_okveds))


if __name__ == '__main__':
    start_process()
