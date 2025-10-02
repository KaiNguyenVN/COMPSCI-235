from recipes.adapters.repository import AbstractRepository
from recipes.domainmodel.recipe import Recipe


def get_number_of_recipes(repo: AbstractRepository):
    # TODO: Task 2 Lab-08
    return repo.get_number_of_recipes()

def get_recipes(repo: AbstractRepository, page: int = 1, page_size: int = 10, sort_method: str = "name"):
    # TODO: Task 2 Lab-08
    recipes = []
    recipe = repo.get_recipes(page=page, page_size=page_size, sort_method=sort_method)

    for rec in recipe:
        recipes.append(rec)

    return {'recipes': recipes, 'page': page, 'page_size': page_size}
