from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    source_url = Column(String, nullable=True)
    cook_time = Column(Integer)  # minutes
    servings = Column(Integer)
    steps = Column(Text)
