from fastapi import APIRouter
from app.agent.run import run_agent
from app.schemas.agent import AgentRequest, AgentResponse

router = APIRouter()


@router.post("/run", response_model=AgentResponse)
async def run_meal_agent(payload: AgentRequest):
    """
    Main agent endpoint:
    Observe → Plan → Act → Adapt
    """
    result = await run_agent(payload)
    return result
