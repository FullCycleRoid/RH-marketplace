from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship


from src import Base


class OkvedNode(Base):
    __tablename__ = 'okved_nodes'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    en_name = Column(String, nullable=False)

    parent_id = Column(Integer, ForeignKey('okved_nodes.id'))
    parent = relationship('OkvedNode', remote_side=[id], back_populates='child_nodes')
    child_nodes = relationship('OkvedNode', back_populates='parent')

    def __repr__(self):
        return f"<OkvedNode(code={self.code}, description={self.name})>"


class MKTUClassifier(Base):
    __tablename__ = 'MKTU_classifier'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    name = Column(String)
    content = Column(Text)
    description = Column(Text)
    include = Column(Text)
    exclude = Column(Text)

    # Переводы на английский
    type_en = Column(String)
    name_en = Column(String)
    content_en = Column(Text)
    description_en = Column(Text)
    include_en = Column(Text)
    exclude_en = Column(Text)

    # Связь с товарами
    categories = relationship("MKTUCategories", back_populates="classifier")

    def __repr__(self):
        return f"<MKTUClassifier(type={self.type}, name={self.name})>"


class MKTUCategories(Base):
    __tablename__ = 'MKTU_categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    classifier_id = Column(Integer, ForeignKey('MKTU_classifier.id'))

    name_en = Column(String)

    classifier = relationship("MKTUClassifier", back_populates="categories")


class CatalogCategory(Base):
    __tablename__ = 'catalog_categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Название категории (напр., "Спорт и инвентарь")
    parent_id = Column(Integer, ForeignKey('catalog_categories.id'))
    en_name = Column(String)  # Перевод на английский

    # Иерархия
    parent = relationship('CatalogCategory', remote_side=[id], back_populates='children')
    children = relationship('CatalogCategory', back_populates='parent')

    # Связи с классификаторами
    okved_nodes = relationship("OkvedNode", secondary="catalog_okved_links")
    mktu_classes = relationship("MKTUClassifier", secondary="catalog_mktu_links")

    def __repr__(self):
        return f"<CatalogCategory(name={self.name})>"


# Таблицы для связей многие-ко-многим
class CatalogOkvedLink(Base):
    __tablename__ = 'catalog_okved_links'
    category_id = Column(Integer, ForeignKey('catalog_categories.id'), primary_key=True)
    okved_id = Column(Integer, ForeignKey('okved_nodes.id'), primary_key=True)


class CatalogMKTULink(Base):
    __tablename__ = 'catalog_mktu_links'
    category_id = Column(Integer, ForeignKey('catalog_categories.id'), primary_key=True)
    mktu_id = Column(Integer, ForeignKey('MKTU_classifier.id'), primary_key=True)