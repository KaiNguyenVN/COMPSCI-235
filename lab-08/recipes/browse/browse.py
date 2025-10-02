from flask import Blueprint, request
from flask import render_template

import recipes.adapters.repository as repo
import recipes.browse.services as services
from recipes.adapters.repository import AbstractRepository

# Configure Blueprint.
browse_blueprint = Blueprint(
    'recipes_bp', __name__)

@browse_blueprint.route('/browse', methods=['GET'])
def browse_recipes():
    # TODO: Complete for Task 2 Lab-08

    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    sort_method = request.args.get('sort_method', 'name')

    number_of_recipes = services.get_number_of_recipes(repo.repo_instance)
    recipes = services.get_recipes(repo.repo_instance, page, page_size, sort_method)

    return render_template(
        'browse.html',
        # Custom page title
        title=f'Browse Recipes | CS235 Recipe Library',
        # Page heading
        heading='Browse Recipes',
        number_of_recipes=number_of_recipes,
        recipes=recipes['recipes'],
        page=page,
        page_size=page_size,
    )
