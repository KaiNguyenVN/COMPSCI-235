from recipes.adapters.repository import AbstractRepository
from recipes.domainmodel.recipe import Recipe


def get_number_of_recipes(repo: AbstractRepository):
    return repo.get_number_of_recipes()


def get_recipes(repo: AbstractRepository):
    recipes = repo.get_recipes(page=1, page_size=10, sort_method="name")
    recipe_dicts = []
    for recipe in recipes:
        recipe_dict = {
            'recipe_id': recipe.id,
            'name': recipe.name,
            'description': recipe.description,
        }
        recipe_dicts.append(recipe_dict)
    return recipe_dicts
