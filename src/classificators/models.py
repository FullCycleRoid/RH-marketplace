from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


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
    products = Column(Text)

    # Переводы на английский
    type_en = Column(String)
    name_en = Column(String)
    content_en = Column(Text)
    description_en = Column(Text)
    include_en = Column(Text)
    exclude_en = Column(Text)
    products_en = Column(Text)

    # Связь с товарами
    items = relationship("Product", back_populates="classifier")


class MKTUProduct(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    classifier_id = Column(Integer, ForeignKey('classifiers.id'))

    name_en = Column(String)

    classifier = relationship("Classifier", back_populates="items")