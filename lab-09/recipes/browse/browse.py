from flask import Blueprint
from flask import render_template

import recipes.adapters.repository as repo
import recipes.browse.services as services

# Configure Blueprint.
browse_blueprint = Blueprint(
    'recipes_bp', __name__)


@browse_blueprint.route('/browse', methods=['GET'])
def browse_recipes():
    num_recipes = services.get_number_of_recipes(repo.repo_instance)
    all_recipes = services.get_recipes(repo.repo_instance)
    return render_template(
        'browse.html',
        # Custom page title
        title=f'Browse Recipes | CS235 Recipe Library',
        # Page heading
        heading='Browse Recipes',
        recipes=all_recipes,
        num_recipes=num_recipes,
    )