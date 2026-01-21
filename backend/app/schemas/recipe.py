from pydantic import BaseModel
from typing import List


class RecipeCreate(BaseModel):
    title: str
    ingredients: List[str]
    steps: List[str]

class RecipeResponse(RecipeCreate):
    id: str