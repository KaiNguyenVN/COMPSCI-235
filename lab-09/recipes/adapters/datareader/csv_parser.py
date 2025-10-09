# csvdatareader_recipes.py
import os
import csv
import ast
import re
from datetime import datetime

from recipes.domainmodel.recipe import Recipe
from recipes.domainmodel.author import Author
from recipes.domainmodel.category import Category
from recipes.domainmodel.nutrition import Nutrition
from recipes.domainmodel.recipe_image import RecipeImage
from recipes.domainmodel.recipe_ingredient import RecipeIngredient
from recipes.domainmodel.recipe_instruction import RecipeInstruction


def _parse_int(val, default=None):
    s = (val or "").strip()
    if not s or s.upper() == "NA":
        return default
    return int(s)

def _parse_float(val, default=None):
    s = (val or "").strip()
    if not s or s.upper() == "NA":
        return default
    return float(s)

def _parse_list_literal(val):
    s = (val or "").strip()
    if not s:
        return []
    try:
        x = ast.literal_eval(s)
        return [str(v).strip() for v in x if str(v).strip()]
    except (SyntaxError, ValueError):
        return [s]

def _strip_or_none(val):
    s = (val or "").strip()
    return s if s and s.upper() != "NA" else None

def _parse_date_with_ordinals(val):
    s = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', (val or "").strip())
    return datetime.strptime(s, "%d %b %Y")


class CSVDataReader:
    """
    Reads recipes from CSV and builds in-memory lists of Recipes, Authors, and Categories.
    Authors and Categories are deduplicated but stored as lists for repo compatibility.
    """
    def __init__(self, recipe_filename: str):
        self.__recipe_filename = recipe_filename
        self.__dataset_of_recipes: list[Recipe] = []
        self.__dataset_of_authors: list[Author] = []
        self.__dataset_of_categories: list[Category] = []
        self.__dataset_of_recipe_images: list[RecipeImage] = []
        self.__dataset_of_recipe_ingredients: list[RecipeIngredient] = []
        self.__dataset_of_recipe_instructions: list[RecipeInstruction] = []

    @property
    def dataset_of_recipes(self) -> list[Recipe]:
        return self.__dataset_of_recipes

    @property
    def dataset_of_authors(self) -> list[Author]:
        return self.__dataset_of_authors

    @property
    def dataset_of_categories(self) -> list[Category]:
        return self.__dataset_of_categories

    @property
    def dataset_of_recipe_images(self) -> list[RecipeImage]:
        return self.__dataset_of_recipe_images

    @property
    def dataset_of_recipe_ingredients(self) -> list[RecipeIngredient]:
        return self.__dataset_of_recipe_ingredients

    @property
    def dataset_of_recipe_instructions(self) -> list[RecipeInstruction]:
        return self.__dataset_of_recipe_instructions

    def read_recipes_csv(self):
        if not os.path.exists(self.__recipe_filename):
            print(f"path {self.__recipe_filename} does not exist!")
            return

        with open(self.__recipe_filename, "r", encoding="utf-8-sig") as f:
            rows = csv.DictReader(f)
            author_count = 1
            category_count = 1

            for row in rows:
                try:
                    recipe_id = _parse_int(row.get("RecipeId"))
                    recipe_name = (row.get("Name") or "").strip()
                    
                    # Skip if recipe name is empty
                    if not recipe_name:
                        continue

                    # ---- Author (unique, list-based) ----
                    author_name = (row.get("AuthorName") or "").strip()
                    author_id = _parse_int(row.get("AuthorId"), default=None)
                    
                    # Use default author if name is empty
                    if not author_name:
                        author_name = "Unknown Author"
                        print(f"DEBUG: Using default author for recipe {recipe_name}")
                        
                    # Check for existing author by name, not by equality
                    existing_author = next((a for a in self.__dataset_of_authors if a.name == author_name), None)
                    if existing_author is None:
                        # Use author_id from CSV if available, otherwise let database auto-generate
                        if author_id is not None:
                            candidate_author = Author(author_id, author_name)
                        else:
                            candidate_author = Author(author_count, author_name)
                            author_count += 1
                        self.__dataset_of_authors.append(candidate_author)
                        author_obj = candidate_author
                    else:
                        author_obj = existing_author

                    # ---- Category (unique, list-based) ----
                    category_name = (row.get("RecipeCategory") or "").strip()
                    # Check for existing category by name, not by equality
                    existing_category = next((c for c in self.__dataset_of_categories if c.name == category_name), None)
                    if existing_category is None:
                        # Don't specify ID - let the database auto-generate it
                        candidate_category = Category(category_name)
                        self.__dataset_of_categories.append(candidate_category)
                        category_obj = candidate_category
                        # print(f"DEBUG: Created new category: {category_name}")
                    else:
                        category_obj = existing_category

                    # ---- Other fields ----
                    cook_time = _parse_int(row.get("CookTime"), default=0)
                    prep_time = _parse_int(row.get("PrepTime"), default=0)
                    date_published = _parse_date_with_ordinals(row.get("DatePublished"))
                    description = (row.get("Description") or "").strip()
                    images = _parse_list_literal(row.get("Images"))
                    ingredient_quantities = _parse_list_literal(row.get("RecipeIngredientQuantities"))
                    ingredients = _parse_list_literal(row.get("RecipeIngredientParts"))
                    instructions = _parse_list_literal(row.get("RecipeInstructions"))

                    # Parse nutrition values with explicit defaults
                    calories_val = _parse_float(row.get("Calories"))
                    calories = 0.0 if calories_val is None else calories_val
                    
                    fat_val = _parse_float(row.get("FatContent"))
                    fat = 0.0 if fat_val is None else fat_val
                    
                    saturated_fat_val = _parse_float(row.get("SaturatedFatContent"))
                    saturated_fat = 0.0 if saturated_fat_val is None else saturated_fat_val
                    
                    cholesterol_val = _parse_float(row.get("CholesterolContent"))
                    cholesterol = 0.0 if cholesterol_val is None else cholesterol_val
                    
                    sodium_val = _parse_float(row.get("SodiumContent"))
                    sodium = 0.0 if sodium_val is None else sodium_val
                    
                    carbohydrates_val = _parse_float(row.get("CarbohydrateContent"))
                    carbohydrates = 0.0 if carbohydrates_val is None else carbohydrates_val
                    
                    fiber_val = _parse_float(row.get("FiberContent"))
                    fiber = 0.0 if fiber_val is None else fiber_val
                    
                    sugar_val = _parse_float(row.get("SugarContent"))
                    sugar = 0.0 if sugar_val is None else sugar_val
                    
                    protein_val = _parse_float(row.get("ProteinContent"))
                    protein = 0.0 if protein_val is None else protein_val
                    
                    nutrition_obj = Nutrition(
                        id=recipe_id,
                        calories=calories,
                        fat=fat,
                        saturated_fat=saturated_fat,
                        cholesterol=cholesterol,
                        sodium=sodium,
                        carbohydrates=carbohydrates,
                        fiber=fiber,
                        sugar=sugar,
                        protein=protein,
                    )

                    servings = _parse_int(row.get("RecipeServings"))
                    recipe_yield = _strip_or_none(row.get("RecipeYield"))

                    recipe = Recipe(
                        id=recipe_id,
                        name=recipe_name,
                        author=author_obj,
                        cook_time=cook_time,
                        preparation_time=prep_time,
                        date=date_published,
                        description=description,
                        images=images,
                        category=category_obj,
                        ingredient_quantities=ingredient_quantities,
                        ingredients=ingredients,
                        rating=None,
                        nutrition=nutrition_obj,
                        servings=servings,
                        recipe_yield=recipe_yield,
                        instructions=instructions,
                    )
                    
                    # Create RecipeImage instances
                    for position, url in enumerate(images, 1):
                        if url and url.strip():
                            recipe_image = RecipeImage(recipe_id, url.strip(), position)
                            self.__dataset_of_recipe_images.append(recipe_image)
                    
                    # Create RecipeIngredient instances
                    for position, (quantity, ingredient) in enumerate(zip(ingredient_quantities, ingredients), 1):
                        if quantity and ingredient and quantity.strip() and ingredient.strip():
                            recipe_ingredient = RecipeIngredient(recipe_id, quantity.strip(), ingredient.strip(), position)
                            self.__dataset_of_recipe_ingredients.append(recipe_ingredient)
                    
                    # Create RecipeInstruction instances
                    for position, step in enumerate(instructions, 1):
                        if step and step.strip():
                            recipe_instruction = RecipeInstruction(recipe_id, step.strip(), position)
                            self.__dataset_of_recipe_instructions.append(recipe_instruction)
                    if hasattr(author_obj, "add_recipe"):
                        author_obj.add_recipe(recipe)
                    if hasattr(category_obj, "add_recipe"):
                        category_obj.add_recipe(recipe)

                    self.__dataset_of_recipes.append(recipe)

                except (ValueError, KeyError) as e:
                    # Skip malformed rows
                    # print(f"Skipping malformed row: {e}")
                    continue
