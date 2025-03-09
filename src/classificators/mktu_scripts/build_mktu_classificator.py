import json

from src import MKTUClassifier


def load_data_from_json(file_path):
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
                products=item['products'],

                # Пример переводов на английский (можно заменить на реальные переводы)
                type_en=item['type'],
                name_en=item['name'],
                content_en=item['content'],
                description_en=item['description'],
                include_en=item['include'],
                exclude_en=item['exclude'],
                products_en=item['products']
            )

            session.add(classifier)
            session.commit()

            # Загрузка товаров
            products = item['products'].split('\n')
            for product in products:
                if product.strip():
                    product_item = Product(
                        name=product.strip(),
                        name_en=product.strip(),  # Пример перевода на английский
                        classifier_id=classifier.id
                    )
                    session.add(product_item)

            session.commit()


# Загрузка данных из JSON-файла
load_data_from_json('mktu.json')