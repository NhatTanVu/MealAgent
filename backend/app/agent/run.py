from app.schemas.agent import AgentRequest, AgentResponse
from app.agent.observe import observe
from app.agent.plan import plan
from app.agent.act import act
from app.agent.adapt import adapt


async def run_agent(payload: AgentRequest):
    context = observe(payload)
    plan_result = plan(context)
    action_result = act(plan_result)
    adapt(payload, action_result)

    return AgentResponse(
        message="Finished running agent",
        recipe=action_result["recipe"],
        grocery_list=action_result["grocery_list"],
        steps=action_result["steps"],
    )
