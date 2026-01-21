from pydantic import BaseModel
from typing import List, Optional


class AgentRequest(BaseModel):
    ingredients: List[str]
    time_available: int  # minutes
    servings: int
    preferences: Optional[List[str]] = []


class AgentResponse(BaseModel):
    message: str
    recipe: str
    grocery_list: List[str]
    steps: List[str]
