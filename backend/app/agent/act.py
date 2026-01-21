def act(plan_result):
    return {
        "recipe": plan_result["selected_recipe"],
        "grocery_list": plan_result["missing_ingredients"],
        "steps": [
            "Prep ingredients",
            "Heat pan",
            "Cook chicken",
            "Add vegetables",
            "Serve"
        ],
    }
