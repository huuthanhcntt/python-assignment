from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String, nullable=False)