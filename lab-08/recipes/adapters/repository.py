import abc
from typing import List

from recipes.domainmodel.author import Author
from recipes.domainmodel.category import Category
from recipes.domainmodel.nutrition import Nutrition
from recipes.domainmodel.recipe import Recipe
from recipes.domainmodel.review import Review
from recipes.domainmodel.user import User

repo_instance = None


class RepositoryException(Exception):
    """
    An exception class for repository errors.
    """

    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):
    """AbstractRepository is an abstract base class that defines the
    interface for a repository to interact with the recipe library.
    """

    #region Author_data Methods to manage Authors
    # Methods to manage Authors

    @abc.abstractmethod
    def add_author(self, author: Author):
        """Adds an Author to the repository."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_authors(self) -> list[Author]:
        """Returns a list of all Authors in the repository."""

        raise NotImplementedError

    @abc.abstractmethod
    def get_authors(self, sort_method: str) -> list[Author]:
        """Returns a list of all Authors in the repository, sorted by sort_method.

        sort_method can be: name or recipes_count.
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_number_of_authors(self) -> int:
        """Returns the number of Authors in the repository."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_multiple_authors(self, authors: List[Author]):
        """Adds multiple Authors to the repository."""
        raise NotImplementedError
    
    #endregion

    #region Category_data Methods to manage Categories
    # Methods to manage Categories

    @abc.abstractmethod
    def add_category(self, category: Category):
        """Adds a Category to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_category_by_name(self, name: str) -> Category | None:
        """
        Returns the Category with the specified name from the repository.
        If there is no Category with the given name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_categories(self) -> List[Category]:
        """Returns a list of all Categories in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_categories(self) -> int:
        """Returns the number of Categories in the repository."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_multiple_categories(self, categories: List[Category]):
        """Adds multiple Categories to the repository."""
        raise NotImplementedError

    #endregion

    #region Recipe_data Methods to manage Recipes   
    # Methods to manage Recipes

    @abc.abstractmethod
    def add_recipe(self, recipe: Recipe):
        """Adds a Recipe to the repository."""
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_multiple_recipes(self, recipe: List[Recipe]):
        """Adds multiple Recipes to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe(self, recipe_id: int) -> Recipe | None:
        """
        Returns Recipe with recipe_id from the repository.
        If there is no Recipe with the given recipe_id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes(self, page: int, page_size: int, sort_method: str) -> List[Recipe]:
        """
        Returns a list of all Recipes in the repository, sorted by sort_method.
        sort_method can be: author, date, name, or rating.
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_number_of_recipes(self) -> int:
        """Returns the number of Recipes in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes_by_name(self, page: int, page_size: int, name: str, sort_method: str = 'name') -> List[Recipe]:
        """
        Returns a list of Recipes that match the given name, sorted by sort_method.
        The sort_method can be: name, date, or rating.
        If there are no Recipes with the given name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes_by_date(self, page: int, page_size: int, target_date: str, sort_method: str = 'name') -> List[Recipe]:
        """
        Returns a list of Recipes that were published on target_date, sorted by sort_method.
        The sort_method can be: name, date, or rating.
        If there are no Recipes on the given date, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes_by_author(self, page: int, page_size: int, author: Author, sort_method: str = 'name') -> List[Recipe]:
        """
        Returns a list of Recipes by the specified Author, sorted by sort_method.
        sort_method can be: name, date, or rating.
        If there are no Recipes by the given Author, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes_by_category(self, page: int, page_size: int, category: Category, sort_method: str = 'name') -> List[Recipe]:
        """
        Returns a list of Recipes in the specified Category, sorted by sort_method.
        The sort_method can be: name, date, or rating.
        If there are no Recipes in the given Category, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes_by_rating(self, page: int, page_size: int, rating: float, sort_method: str = 'name') -> List[Recipe]:
        """
        Returns a list of Recipes that are rated at the given rating, sorted by sort_method.
        The sort_method can be: name, date, or rating.
        If there are no Recipes rated at the given rating, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_recipes(self) -> int:
        """Returns the number of Recipes in the repository."""
        raise NotImplementedError

    #endregion

    #region Review_data Methods to manage Reviews
    # Methods to manage Reviews

    @abc.abstractmethod
    def add_review(self, user: User, review: Review):
        """Adds a Review to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self, page: int, page_size: int, sort_method: str) -> list[Review]:
        """
        Returns a list of all Reviews in the repository, sorted by sort_method.
        sort_method can be: date, rating, or user.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_reviews(self, page: int, page_size: int, user: User, sort_method: str) -> list[Review]:
        """
        Returns a list of Reviews submitted by the specified User, sorted by sort_method.
        sort_method can be: date, rating, or recipe.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_reviews(self, page: int, page_size: int, recipe: Recipe, sort_method: str) -> list[
        Review]:
        """
        Returns a list of Reviews for the specified Recipe, sorted by sort_method.
        sort_method can be: date, rating, or user.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipes_reviewed_by_user(self, page: int, page_size: int, user: User, sort_method: str) -> \
            list[Recipe]:
        """
        Returns a list of Recipes reviewed by the specified User, sorted by sort_method.
        sort_method can be: date, name, or author.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_review_by_id(self, review_id: int) -> Review | None:
        """
        Returns the Review with the specified review_id from the repository.
        If there is no Review with the given review_id, this method returns None.
        """
        raise NotImplementedError
    
    #endregion

    #region User_data Methods to manage Users

    # Methods to manage Users

    @abc.abstractmethod
    def add_user(self, user: User):
        """Adds a User to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username: str) -> User | None:
        """
        Returns the User with the provided username from the repository.
        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    #endregion

    #region User_favourite_recipes Methods to manage User's favourite Recipes

    @abc.abstractmethod
    def add_favourite_recipe(self, user: User, recipe: Recipe):
        """Adds a Recipe to the User's list of favourite Recipes."""
        raise NotImplementedError

    @abc.abstractmethod
    def remove_favourite_recipe(self, user: User, recipe: Recipe):
        """Removes a Recipe from the User's list of favourite Recipes."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_favourite_recipes(self, page: int, page_size: int, user: User) -> list[Recipe]:
        """Returns a list of the User's favourite Recipes."""
        raise NotImplementedError
    
    #endregion

    #region Nutrition_data Methods to manage Nutrition

    @abc.abstractmethod
    def add_nutrition(self, nutrition: Nutrition):
        """Adds a Nutrition to the repository."""
        raise NotImplementedError

    #endregion