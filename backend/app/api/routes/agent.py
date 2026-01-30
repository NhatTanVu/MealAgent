from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.agent.run import run_agent
from app.api.deps import get_db
from app.models.recipe import Recipe
from app.schemas.agent import AgentRequest, AgentResponse, PlanCandidate, PlanRequest, PlanResponse

router = APIRouter()


def normalize_unit(unit: str | None) -> str | None:
    if not unit:
        return None
    unit = unit.lower().strip()
    aliases = {
        "grams": "g",
        "gram": "g",
        "kilogram": "kg",
        "kilograms": "kg",
        "tablespoon": "tbsp",
        "tablespoons": "tbsp",
        "teaspoon": "tsp",
        "teaspoons": "tsp",
        "cups": "cup"
    }
    return aliases.get(unit, unit)


@router.post("/plan", response_model=PlanResponse)
async def plan_recipes(payload: PlanRequest, db: Session = Depends(get_db)):
    user_ingredients = {
        i["name"].lower(): {
            "amount": i.get("amount"),
            "unit": normalize_unit(i.get("unit"))
        }
        for i in payload.ingredients
    }
    recipes = db.query(Recipe).all()
    candidates: list[tuple[float, PlanCandidate]] = []
    for recipe in recipes:
        total = len(recipe.ingredients)
        have = 0
        utilization_sum = 0.0
        missing = 0
        invalid = False

        for ing in recipe.ingredients:
            name = ing.name.lower()
            req_amount = ing.amount
            req_unit = normalize_unit(ing.unit)
            user_ing = user_ingredients.get(name)

            if not user_ing:
                missing += 1
                continue

            have += 1

            if req_amount and user_ing["amount"] \
                    and req_unit and user_ing["unit"]:
                if req_unit != user_ing["unit"]:
                    utilization_sum += 0.5
                elif user_ing["amount"] < req_amount:
                    invalid = True
                    break
                else:
                    utilization_sum += min(req_amount /
                                           user_ing["amount"], 1.0)
            else:
                utilization_sum += 0.5

        if invalid or have == 0:
            continue

        coverage_score = have / total
        utilization_score = utilization_sum / have if have else 0

        final_score = (
            coverage_score * 2.0
            + utilization_score
            - missing * 1.5
        )

        candidates.append(
            (
                final_score,
                PlanCandidate(
                    id=recipe.id,
                    title=recipe.title,
                    score_reason=(
                        f"{have}/{total} ingredients available • "
                        f"{missing} missing"
                    )
                )
            )
        )

    candidates.sort(key=lambda x: x[0], reverse=True)

    return PlanResponse(
        candidates=[c for _, c in candidates[:3]]
    )


@router.post("/run", response_model=AgentResponse)
async def run_meal_agent(payload: AgentRequest):
    """
    Main agent endpoint:
    Observe → Plan → Act → Adapt
    """
    result = await run_agent(payload)
    return result
