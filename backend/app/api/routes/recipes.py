from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeResponse

router = APIRouter()


@router.post("/", response_model=RecipeResponse)
async def ingest_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    """
    Ingest a recipe from URL / video / image
    """
    db_recipe = Recipe(
        title=recipe.title,
        cook_time=30,
        servings=2,
        steps="\n".join(recipe.steps)
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    return RecipeResponse(
        title=recipe.title,
        ingredients=recipe.ingredients,
        steps=recipe.steps,
        id="demo-recipe-id"
    )
