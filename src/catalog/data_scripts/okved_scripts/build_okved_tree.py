import json
from pprint import pprint

from sqlalchemy.orm import Session

from src import OkvedNode
from src.core.database.postgres.connectors import psycopg_sync_engine
from src.core.language_translator.google_translator import translate_text


def load_okved_data(session, data, parent=None):
    for item in data:
        name = item["name"]
        translation = translate_text(name, "ru", "en")
        node = OkvedNode(
            code=item["code"], name=name, en_name=translation, parent=parent
        )
        session.add(node)
        session.commit()

        print("Добавлена категория")
        pprint(node)
        if "items" in item:
            load_okved_data(session, item["items"], node)


if __name__ == "__main__":
    with open("оквэд.json", "r", encoding="utf-8") as f:
        okved_data = json.load(f)

    with Session(psycopg_sync_engine) as session:
        load_okved_data(session, okved_data)
