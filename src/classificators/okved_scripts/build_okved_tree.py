import json

from sqlalchemy.orm import Session

from src import OkvedNode
from src.core.database.postgres.connectors import psycopg_sync_engine


def load_okved_data(session, data, parent=None):
    for item in data:
        node = OkvedNode(
            code=item['code'],
            name=item['name'],
            parent=parent
        )
        session.add(node)
        session.commit()

        if 'items' in item:
            load_okved_data(session, item['items'], node)


if __name__ == "__main__":
    with open('оквэд.json', 'r', encoding='utf-8') as f:
        okved_data = json.load(f)


    with Session(psycopg_sync_engine) as session:
        load_okved_data(session, okved_data)