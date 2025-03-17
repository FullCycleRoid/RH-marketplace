import pandas as pd

class OkvedMapper:
    def __init__(self, mapping_file_path):
        """
        Инициализация маппера с загрузкой таблицы соответствий
        :param mapping_file_path: путь к файлу соответствий (Excel или CSV)
        """
        # Загрузка данных
        if mapping_file_path.endswith('.xlsx'):
            self.mapping_df = pd.read_excel(mapping_file_path)
        elif mapping_file_path.endswith('.csv'):
            self.mapping_df = pd.read_csv(mapping_file_path)
        else:
            raise ValueError("Формат файла не поддерживается. Используйте XLSX или CSV")


    def get_new_code(self, old_code):
        """
        Получить значение new_code по old_code
        :param old_code: код ОКВЭД-1 (строка)
        :return: значение new_code (строка или None, если код не найден)
        """
        # Ищем строку, где old_code совпадает с переданным значением
        result = self.mapping_df[self.mapping_df['old_code'] == old_code]

        # Если найдено хотя бы одно совпадение
        if not result.empty:
            # Возвращаем первое значение new_code
            return result.iloc[0]['new_code']
        else:
            # Если код не найден, возвращаем None
            return None

# Пример использования
if __name__ == "__main__":
    # Инициализация маппера (укажите правильный путь к вашему файлу)
    mapper = OkvedMapper('okved.csv')

    # Пример преобразования кода
    old_okved = '02.01.5'  # Ваш код ОКВЭД-1
    new_codes = mapper.get_new_code(old_okved)

    print(f"Код ОКВЭД-1: {old_okved}")
    print(f"Соответствующие коды ОКВЭД-2: {new_codes}")