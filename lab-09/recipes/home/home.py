from flask import Blueprint, render_template, request
import recipes.adapters.repository as repo

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/')
def home():
    recipe_id = request.args.get('recipe_id', default=38, type=int)

    some_recipe = repo.repo_instance.get_recipe(recipe_id)  # get recipe with recipe_id = 1
    #print(some_recipe)

    # Use Jinja to customize a predefined html page rendering the layout for showing a single recipe.
    return render_template('recipeDetails.html', recipe=some_recipe)

