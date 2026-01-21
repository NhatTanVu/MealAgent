from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base


class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    scheduled_for = Column(String)  # ISO datetime string
