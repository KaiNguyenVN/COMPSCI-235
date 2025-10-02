from abc import ABC
from sys import exception
from typing import List, Type

from sqlalchemy import func
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from recipes.adapters.repository import AbstractRepository
from recipes.adapters.utils import search_string
from recipes.domainmodel import recipe
from recipes.domainmodel.recipe import Recipe
from recipes.domainmodel.author import Author
from recipes.domainmodel.category import Category
from recipes.domainmodel.user import User
from recipes.domainmodel.review import Review
from recipes.domainmodel.nutrition import Nutrition
from recipes.domainmodel.favourite import Favourite
from recipes.domainmodel.recipe_image import RecipeImage
from recipes.domainmodel.recipe_ingredient import RecipeIngredient
from recipes.domainmodel.recipe_instruction import RecipeInstruction

# feature 1 test
class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self) -> object:
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # region User_data Methods to manage Users
    def add_user(self, user: User):
        pass

    def get_user(self, username: str) -> User:
        pass

    # endregion

    # region Author_data Methods to manage Authors
    def add_author(self, author: Author):
        pass

    def get_authors(self) -> List[Author]:
        pass

    def get_authors(self, sort_method: str) -> List[Author]:
        pass

    def get_number_of_authors(self) -> int:
        pass

    # TODO: Lab 8 - Task 1
    def add_multiple_authors(self, authors: List[Author]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for author in authors:
                    scm.session.add(author)
            scm.commit()

    # endregion

    # region Category_data Methods to manage Categories
    def add_category(self, category: Category):
        pass

    def get_category_by_name(self, name: str) -> Category:
        pass

    def get_categories(self) -> List[Category]:
        pass

    def get_number_of_categories(self) -> int:
        pass

    def add_multiple_categories(self, categories: List[Category]):
        pass

    # endregion

    # region Recipe_data Methods to manage Recipes

    def add_recipe(self, recipe: Recipe):
        pass

    def add_multiple_recipes(self, recipes: List[Recipe]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for recipe in recipes:
                    scm.session.add(recipe)
            scm.commit()

    def get_recipe(self, recipe_id: int) -> Recipe:
        recipe = None
        try:
            query = self._session_cm.session.query(Recipe).filter(
                Recipe._Recipe__id == recipe_id)
            recipe = query.one()
            # Populate the recipe with related data for consistent domain model interface
            self._populate_recipe_data(recipe)
        except NoResultFound:
            print(f'Recipe {recipe_id} was not found')

        return recipe

    def get_recipes(self, page: int, page_size: int, sort_method: str) -> List[Recipe]:
        # TODO: Task 2 Lab-08
        recipes = []
        try:
            query = self._session_cm.session.query(Recipe)
            recipes = query.offset(page * page_size).limit(page_size).all()
            for rec in recipes:
                self._populate_recipe_data(rec)

        except Exception as e:
            print(f'Error fetching recipes: {e}')

        return recipes


    def get_number_of_recipes(self) -> int:
        # TODO: Task 2 Lab-08
        query = self._session_cm.session.query(Recipe)
        return query.count()


    def get_recipes_by_name(self, page: int, page_size: int, name: str, sort_method: str = 'name') -> List[Recipe]:
        pass

    def get_recipes_by_date(self, page: int, page_size: int, target_date: str, sort_method: str = 'name') -> List[
        Recipe]:
        pass

    def get_recipes_by_author(self, page: int, page_size: int, author: Author, sort_method: str = 'name') -> List[
        Recipe]:
        pass

    def get_recipes_by_category(self, page: int, page_size: int, category: Category, sort_method: str = 'name') -> List[
        Recipe]:
        pass

    def get_recipes_by_rating(self, page: int, page_size: int, rating: float, sort_method: str = 'name') -> List[
        Recipe]:
        pass

    # endregion

    # region Review_data Methods to manage Reviews
    def add_review(self, user: User, review: Review):
        pass

    def get_reviews(self, page: int, page_size: int, sort_method: str) -> List[Review]:
       pass

    def get_user_reviews(self, page: int, page_size: int, user: User, sort_method: str) -> List[Review]:
        pass

    def get_recipe_reviews(self, page: int, page_size: int, recipe: Recipe, sort_method: str) -> List[Review]:
        pass

    def get_recipes_reviewed_by_user(self, page: int, page_size: int, user: User, sort_method: str) -> List[Recipe]:
        pass

    def get_review_by_id(self, review_id: int) -> Review:
        pass

    # endregion

    # region User_favourite_recipes Methods to manage User's favourite Recipes
    def add_favourite_recipe(self, user: User, recipe: Recipe):
        pass

    def remove_favourite_recipe(self, user: User, recipe: Recipe):
        pass

    def get_favourite_recipes(self, page: int, page_size: int, user: User) -> List[Recipe]:
        pass

    # endregion

    # region Nutrition_data Methods to manage Nutrition

    def add_nutrition(self, nutrition: Nutrition):
        pass

    # endregion

    def _populate_recipe_data(self, recipe: Recipe):
        """
        Populate a Recipe object with related data (images, ingredients, instructions)
        to maintain consistent domain model interface between memory and database repositories.
        """
        if recipe is None:
            return

        # Use the same session context
        with self._session_cm as scm:
            self._populate_recipe_data_in_session(recipe, scm.session)

    def _populate_recipe_data_in_session(self, recipe: Recipe, session):
        """
        Populate a Recipe object with related data using the provided session.
        """
        if recipe is None:
            return

        # Load and populate images
        recipe_images = session.query(RecipeImage).filter(
            RecipeImage._RecipeImage__recipe_id == recipe.id
        ).order_by(RecipeImage._RecipeImage__position).all()

        if recipe_images:
            image_urls = [img.url for img in recipe_images]
            recipe._Recipe__images = image_urls
        else:
            print(f"DEBUG: No images found for recipe {recipe.id}")


    # region RecipeImage Methods
    def add_recipe_image(self, recipe_image: RecipeImage):
        pass

    def add_multiple_recipe_images(self, recipe_images: List[RecipeImage]):
        with self._session_cm as scm:
            for recipe_image in recipe_images:
                scm.session.add(recipe_image)
            scm.commit()

    def get_recipe_images(self, recipe_id: int) -> List[RecipeImage]:
        pass

    # endregion

