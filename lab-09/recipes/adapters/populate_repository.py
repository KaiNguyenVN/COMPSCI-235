import os
from pathlib import Path

from recipes.adapters.repository import AbstractRepository
from recipes.adapters.datareader.csv_parser import CSVDataReader


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool, testing: bool):
    # Get the absolute path to the data directory
    dir_name = os.path.abspath(data_path)

    if testing:
        # Different files for the testing mode.
        recipe_filename = os.path.join(dir_name, "recipes-excerpt.csv")
    else:
        recipe_filename = os.path.join(dir_name, "recipes.csv")

    reader = CSVDataReader(recipe_filename)
    reader.read_recipes_csv()

    authors = reader.dataset_of_authors
    recipes = reader.dataset_of_recipes
    categories = reader.dataset_of_categories

    # TODO : Add authors to the repo
    repo.add_multiple_authors(authors)

    # Add recipes to the repo
    repo.add_multiple_recipes(recipes)
    
    # Add additional data using domain models (if using database repository)
    if database_mode:
        # print("Populating additional tables...")

        # Add recipe images
        recipe_images = reader.dataset_of_recipe_images
        if recipe_images:
            repo.add_multiple_recipe_images(recipe_images)