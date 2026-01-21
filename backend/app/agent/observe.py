from app.schemas.agent import AgentRequest


def observe(payload: AgentRequest):
    return {
        "ingredients": payload.ingredients,
        "time_available": payload.time_available,
        "servings": payload.servings,
        "preferences": payload.preferences,
    }