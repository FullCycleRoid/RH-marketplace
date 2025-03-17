import json
from pprint import pprint

from sqlalchemy.orm import Session

from src import MKTUClassifier, MKTUCategories
from src.core.database.postgres.connectors import psycopg_sync_engine
from src.core.language_translator.google_translator import translate_text, translate_large_text


def load_data_from_json(session, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        for item in data:
            classifier = MKTUClassifier(
                type=item['type'],
                name=item['name'],
                content=item['content'],
                description=item['description'],
                include=item['include'],
                exclude=item['exclude'],

                type_en=translate_large_text(item['type'], 'ru', 'en'),
                name_en=translate_large_text(item['name'], 'ru', 'en'),
                content_en=translate_large_text(item['content'], 'ru', 'en'),
                description_en=translate_large_text(item['description'], 'ru', 'en'),
                include_en=translate_large_text(item['include'], 'ru', 'en'),
                exclude_en=translate_large_text(item['exclude'], 'ru', 'en'),
            )

            session.add(classifier)
            session.commit()

            print('Добавлен класс МКТУ')
            pprint(classifier)

            # Загрузка товаров
            categories = item['products'].split(';')
            for category in categories:
                if category.strip():
                    product_item = MKTUCategories(
                        name=category.strip(),
                        name_en=translate_text(category.strip(), 'ru', 'en'),  # Пример перевода на английский
                        classifier_id=classifier.id
                    )
                    session.add(product_item)
                    print(f'Добавлена категория: {category.strip()}')
            session.commit()


# ALTER SEQUENCE public."MKTU_categories_id_seq" RESTART WITH 1;
# ALTER SEQUENCE public."MKTU_classifier_id_seq" RESTART WITH 1;


if __name__ == "__main__":

    with Session(psycopg_sync_engine) as session:
        load_data_from_json(session, 'mktu.json')