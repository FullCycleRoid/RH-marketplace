from sqlalchemy.orm import sessionmaker

from src import CatalogCategory
from src.core.language_translator.google_translator import translate_large_text

Session = sessionmaker(bind=engine)
session = Session()

# Создание категорий каталога
for cluster_id, name in cluster_names.items():
    parent = (
        session.query(CatalogCategory)
        .filter_by(cluster_id=df["parent_cluster"])
        .first()
    )
    category = CatalogCategory(
        name=name.capitalize(),
        en_name=translate_large_text(name),  # Функция перевода
        parent=parent,
    )
    session.add(category)

session.commit()
