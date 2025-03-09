from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src import Base


class OkvedNode(Base):
    __tablename__ = 'okved_nodes'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)

    parent_id = Column(Integer, ForeignKey('okved_nodes.id'))
    parent = relationship('OkvedNode', remote_side=[id], back_populates='child_nodes')
    child_nodes = relationship('OkvedNode', back_populates='parent')

    def __repr__(self):
        return f"<OkvedNode(code={self.code}, description={self.name})>"
