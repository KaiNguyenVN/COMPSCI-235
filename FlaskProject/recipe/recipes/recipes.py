from flask import render_template, Blueprint
from recipe import create_recipes

browse_blueprint = Blueprint('browse_bp', __name__)
recipe_detail_blueprint = Blueprint('recipe_detail_bp', __name__)

@browse_blueprint.route('/browse', methods=['GET'])
def browse():
    list_of_recipes = create_recipes()
    return render_template('browse.html', recipes=list_of_recipes)

@recipe_detail_blueprint.route('/recipe/<int:recipe_id>', methods=['GET'])
def recipe(recipe_id):
    list_of_recipes = create_recipes()
    recipe = next(recipe for recipe in list_of_recipes if recipe.id == recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)