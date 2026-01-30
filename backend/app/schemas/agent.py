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


class PlanRequest(BaseModel):
    ingredients: List[dict]
    timeAvailable: int
    servings: int


class PlanCandidate(BaseModel):
    id: int
    title: str
    score_reason: str


class PlanResponse(BaseModel):
    candidates: List[PlanCandidate]
