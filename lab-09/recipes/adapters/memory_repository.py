from datetime import datetime
from typing import Any
from typing import List, Type

from recipes.adapters.repository import AbstractRepository
from recipes.domainmodel.author import Author
from recipes.domainmodel.category import Category
from recipes.domainmodel.nutrition import Nutrition
from recipes.domainmodel.recipe import Recipe
from recipes.domainmodel.review import Review
from recipes.domainmodel.user import User
from recipes.domainmodel.tag import Tag

SORT_METHOD_AUTHOR = 'author'
SORT_METHOD_DATE = 'date'
SORT_METHOD_NAME = 'name'
SORT_METHOD_RATING = 'rating'
SORT_METHOD_RECIPE = 'recipe'
SORT_METHOD_RECIPES_COUNT = 'recipes_count'
SORT_METHOD_USER = 'user'


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__authors = list()
        self.__categories = list()
        self.__recipes = list()
        self.__reviews = list()
        self.__users = list()
        self.__tags = list()
        self._next_user_id = 1
        self._next_category_id = 1
        self._next_tag_id = 1

    #region Author_data
    def add_author(self, author: Author):
        self._validate_author(author)
        self.__authors.append(author)

    def get_authors(self) -> list[Author]:
        return self.__authors

    def get_authors(self, sort_method: str) -> list[Author]:
        """
        Returns a list of all Authors in the repository, sorted by sort_method.
        The sort_method can be: name or recipes_count.
        """
        if sort_method == SORT_METHOD_NAME:
            return sorted(self.__authors, key=lambda a: a.name)
        elif sort_method == SORT_METHOD_RECIPES_COUNT:
            return sorted(self.__authors, key=lambda a: len(a.recipes),
                          reverse=True)
        else:
            raise ValueError(f"Invalid sort method: {sort_method}")

    def get_number_of_authors(self) -> int:
        return len(self.__authors)

    def add_multiple_authors(self, authors: List[Author]):
        for author in authors:
            self.add_author(author)

    #endregion

    #region Category_data Methods to manage Categories
    def add_category(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance")
        if category.id is None:
            category._Category__id = self._next_category_id
            self._next_category_id += 1
        self._validate_category(category)
        self.__categories.append(category)

    def get_category_by_name(self, name: str) -> Category | None:
        """
        Returns the Category with the specified name from the repository.
        If there is no Category with the given name, this method returns None.
        """
        if not isinstance(name, str):
            raise TypeError("Expected name to be a string")
        for category in self.__categories:
            if category.name.lower() == name.lower():
                return category
        return None

    def get_categories(self) -> List[Category]:
        """
        Returns a list of all Categories in the repository.
        """
        return self.__categories

    def get_number_of_categories(self) -> int:
        return len(self.__categories)

    def add_multiple_categories(self, categories: List[Category]):
        for category in categories:
            self.add_category(category)

    #endregion

    #region Recipe_data Methods to manage Recipes
    def add_recipe(self, recipe: Recipe):
        if not isinstance(recipe, Recipe):
            raise TypeError("Expected a Recipe instance")
        self._validate_recipe(recipe)
        self.__recipes.append(recipe)
    
    def add_multiple_recipes(self, recipes: List[Recipe]):
        """
        Adds multiple Recipes to the repository after validating them.
        """
        for recipe in recipes:
            if not isinstance(recipe, Recipe):
                raise TypeError("Expected a Recipe instance")
            self._validate_recipe(recipe)
            self.__recipes.append(recipe)

    def get_recipe(self, recipe_id: int) -> Recipe | None:
        """
        Returns Recipe with recipe_id from the repository.
        If there is no Recipe with the given recipe_id, this method returns None.
        """
        for recipe in self.__recipes:
            if recipe.id == recipe_id:
                return recipe
        return None

    def get_recipes(self, page: int, page_size: int, sort_method: str) -> List[
        Recipe]:
        """
        Returns a list of all Recipes in the repository, sorted by sort_method.
        The sort_method can be: name, date, or rating.
        Pagination is applied using page and page_size.
        """
        if sort_method == SORT_METHOD_NAME:
            sorted_recipes = sorted(self.__recipes, key=lambda r: r.name)
        elif sort_method == SORT_METHOD_DATE:
            sorted_recipes = sorted(self.__recipes, key=lambda r: r.date)
        elif sort_method == SORT_METHOD_RATING:
            sorted_recipes = sorted(self.__recipes, key=lambda r: r.rating if r.rating is not None else float('-inf'),
                                    reverse=True)
        else:
            raise ValueError(f"Invalid sort method: {sort_method}")

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return sorted_recipes[start_index:end_index]
    
    def get_all_recipes(self, sort_method: str = 'name') -> List[Recipe]:
        """
        Returns all recipes in the repository, sorted by sort_method.
        This method is optimized for getting all recipes without pagination.
        The sort_method can be: name, date, or rating.
        """
        if sort_method == SORT_METHOD_NAME:
            return sorted(self.__recipes, key=lambda r: r.name)
        elif sort_method == SORT_METHOD_DATE:
            return sorted(self.__recipes, key=lambda r: r.date)
        elif sort_method == SORT_METHOD_RATING:
            return sorted(self.__recipes, key=lambda r: r.rating if r.rating is not None else float('-inf'),
                         reverse=True)
        else:
            raise ValueError(f"Invalid sort method: {sort_method}")
    
    def get_recipes_with_category_filter(self, page: int, page_size: int, sort_method: str, category_name: str = None) -> tuple[List[Recipe], int]:
        """
        Returns recipes with optional category filtering, sorted by sort_method.
        This method is optimized for browse functionality with in-memory filtering.
        
        Args:
            page: Current page number
            page_size: Number of recipes per page
            sort_method: Method to sort recipes by
            category_name: Optional category name to filter by
            
        Returns:
            tuple: (recipes_list, total_count)
        """
        # Start with all recipes
        filtered_recipes = self.__recipes.copy()
        
        # Apply category filter if specified
        if category_name:
            filtered_recipes = [
                recipe for recipe in filtered_recipes
                if recipe.category.name.lower() == category_name.lower()
            ]
        
        # Apply sorting
        if sort_method == SORT_METHOD_NAME:
            filtered_recipes = sorted(filtered_recipes, key=lambda r: r.name)
        elif sort_method == SORT_METHOD_DATE:
            filtered_recipes = sorted(filtered_recipes, key=lambda r: r.date)
        elif sort_method == SORT_METHOD_RATING:
            filtered_recipes = sorted(filtered_recipes, key=lambda r: r.rating if r.rating is not None else float('-inf'),
                                    reverse=True)
        else:
            raise ValueError(f"Invalid sort method: {sort_method}")
        
        # Get total count
        total_count = len(filtered_recipes)
        
        # Apply pagination
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        recipes = filtered_recipes[start_index:end_index]
        
        return recipes, total_count
    
    def search_recipes(self, search_type: str, search_term: str, page: int, page_size: int, sort_method: str, category_name: str = None) -> tuple[List[Recipe], int]:
        """
        Search recipes with in-memory filtering.
        
        Args:
            search_type: Type of search (name, author, category, date, rating)
            search_term: Search term
            page: Current page number
            page_size: Number of recipes per page
            sort_method: Method to sort recipes by
            category_name: Optional category name to filter by
            
        Returns:
            tuple: (recipes_list, total_count)
        """
        from datetime import datetime
        
        # Start with all recipes
        filtered_recipes = self.__recipes.copy()
        
        # Apply search filter based on search_type
        if search_type == 'name':
            filtered_recipes = [r for r in filtered_recipes if search_term.lower() in r.name.lower()]
        elif search_type == 'author':
            filtered_recipes = [r for r in filtered_recipes if r.author and search_term.lower() in r.author.name.lower()]
        elif search_type == 'category':
            filtered_recipes = [r for r in filtered_recipes if r.category and search_term.lower() in r.category.name.lower()]
        elif search_type == 'date':
            try:
                date_obj = datetime.strptime(search_term, "%Y-%m-%d").date()
                filtered_recipes = [r for r in filtered_recipes if r.date.date() == date_obj]
            except ValueError:
                return [], 0
        elif search_type == 'rating':
            try:
                rating = float(search_term)
                filtered_recipes = [r for r in filtered_recipes if r.rating == rating]
            except ValueError:
                return [], 0
        
        # Apply additional category filter if specified
        if category_name:
            filtered_recipes = [r for r in filtered_recipes if r.category.name.lower() == category_name.lower()]
        
        # Apply sorting
        if sort_method == SORT_METHOD_NAME:
            filtered_recipes = sorted(filtered_recipes, key=lambda r: r.name)
        elif sort_method == SORT_METHOD_DATE:
            filtered_recipes = sorted(filtered_recipes, key=lambda r: r.date)
        elif sort_method == SORT_METHOD_RATING:
            filtered_recipes = sorted(filtered_recipes, key=lambda r: r.rating if r.rating is not None else float('-inf'),
                                    reverse=True)
        else:
            raise ValueError(f"Invalid sort method: {sort_method}")
        
        # Get total count
        total_count = len(filtered_recipes)
        
        # Apply pagination
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        recipes = filtered_recipes[start_index:end_index]
        
        return recipes, total_count
    
    def get_number_of_recipes(self) -> int:
        return len(self.__recipes)

    def get_recipes_by_name(self, page: int, page_size: int,
                            name: str, sort_method: str = 'name') -> List[Recipe]:
        """
        Returns a list of Recipes that match the given name, sorted by sort_method.
        The sort_method can be: name, date, or rating.
        If there are no Recipes with the given name, this method returns an empty list.
        Pagination is applied using page and page_size.
        """
        if not isinstance(name, str):
            raise TypeError("Expected name to be a string")
        matching_recipes = [recipe for recipe in self.__recipes if
                            name.lower() in recipe.name.lower()]

        # Apply sorting based on sort_method
        if sort_method == 'name':
            sorted_recipes = sorted(matching_recipes, key=lambda r: r.name)
        elif sort_method == 'date':
            sorted_recipes = sorted(matching_recipes, key=lambda r: r.date)
        elif sort_method == 'rating':
            sorted_recipes = sorted(matching_recipes, key=lambda r: r.rating if r.rating is not None else float('-inf'),
                                    reverse=True)
        else:
            raise ValueError(f"Invalid sort method: {sort_method}")

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return sorted_recipes[start_index:end_index]

    def get_recipes_by_date(self, page: int, page_size: int,
                            target_date: str, sort_method: str = SORT_METHOD_NAME) -> List[Recipe]:
        """
        Returns a list of Recipes that were published on target_date, sorted by sort_method.
        The sort_method can be: name, date, or rating.
        If there are no Recipes on the given date, this method returns an empty list.
        Pagination is applied using page and page_size.
        """
        if not isinstance(target_date, str):
            raise TypeError("Expected target_date to be a string")
        try:
            date = datetime.strptime(target_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

        matching_recipes = [recipe for recipe in self.__recipes if
                            recipe.date.date() == date.date()]

        if sort_method == SORT_METHOD_NAME:
            sorted_recipes = sorted(matching_recipes, key=lambda r: r.name)
        elif sort_method == SORT_METHOD_DATE:
            sorted_recipes = sorted(matching_recipes, key=lambda r: r.date)
        elif sort_method == SORT_METHOD_RATING:
            sorted_recipes = sorted(matching_recipes, key=lambda r: r.rating if r.rating is not None else float('-inf'),
                                    reverse=True)
        else:
            raise ValueError(f"Invalid sort method: {sort_method}")

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return sorted_recipes[start_index:end_index]

    def get_recipes_by_author(self, page: int, page_size: int, author: Author,
                              sort_method: str = 'name') -> List[Recipe]:
        """
        Returns a list of Recipes by the specified Author, sorted by sort_method.
        The sort_method can be: name, date, or rating.
        If there are no Recipes by the given Author, this method returns an empty list.
        """
        if not isinstance(author, Author):
            raise TypeError("Expected author to be an Author instance")
        matching_recipes = [recipe for recipe in self.__recipes if
                            recipe.author == author]
        if not matching_recipes:
            return []
        if sort_method == 'name':
            sorted_recipes = sorted(matching_recipes, key=lambda r: r.name)
        elif sort_method == 'date':
            sorted_recipes = sorted(matching_recipes, key=lambda r: r.date)
        elif sort_method == 'rating':
            sorted_recipes = sorted(matching_recipes, key=lambda r: r.rating if r.rating is not None else float('-inf'),
                                    reverse=True)
        else:
            raise ValueError(f"Invalid sort method: {sort_method}")
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return sorted_recipes[start_index:end_index]

    def get_recipes_by_category(self, page: int, page_size: int,
                                category: Category, sort_method: str = 'name') -> List[Recipe]:
        """
        Returns a list of Recipes in the specified Category, sorted by sort_method.
        The sort_method can be: name, date, or rating.
        If there are no Recipes in the given Category, this method returns an empty list.
        Pagination is applied using page and page_size.
        """
        if not isinstance(category, Category):
            raise TypeError("Expected category to be a Category instance")
        matching_recipes = [recipe for recipe in self.__recipes if
                            recipe.category == category]

        if sort_method == 'name':
            sorted_recipes = sorted(matching_recipes, key=lambda r: r.name)
        elif sort_method == 'date':
            sorted_recipes = sorted(matching_recipes, key=lambda r: r.date)
        elif sort_method == 'rating':
            sorted_recipes = sorted(matching_recipes, key=lambda r: r.rating if r.rating is not None else float('-inf'),
                                    reverse=True)
        else:
            raise ValueError(f"Invalid sort method: {sort_method}")

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return sorted_recipes[start_index:end_index]

    def get_recipes_by_rating(self, page: int, page_size: int,
                              rating: float, sort_method: str = 'name') -> List[Recipe]:
        """
        Returns a list of Recipes that are rated at the given rating, sorted by sort_method.
        The sort_method can be: name, date, or rating.
        If there are no Recipes rated at the given rating, this method returns an empty list.
        Pagination is applied using page and page_size.
        """
        if not isinstance(rating, (float, int)):
            raise TypeError("Expected rating to be a float or int")
        matching_recipes = [recipe for recipe in self.__recipes if
                            recipe.rating is not None and recipe.rating == rating]

        if sort_method == 'name':
            sorted_recipes = sorted(matching_recipes, key=lambda r: r.name)
        elif sort_method == 'date':
            sorted_recipes = sorted(matching_recipes, key=lambda r: r.date)
        elif sort_method == 'rating':
            sorted_recipes = sorted(matching_recipes, key=lambda r: r.rating if r.rating is not None else float('-inf'),
                                    reverse=True)
        else:
            raise ValueError(f"Invalid sort method: {sort_method}")

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return sorted_recipes[start_index:end_index]

    def get_number_of_recipes(self) -> int:
        """
        Returns the total number of Recipes in the repository.
        """
        return len(self.__recipes)

    #endregion

    #region Review_data Methods to manage Reviews
    def add_review(self, user: User, review: Review):
        """
        Adds a Review to the repository after validating it.
        The user must be an instance of User, and the review must be an instance of Review.
        """
        if not isinstance(user, User):
            raise TypeError("Expected a User instance")
        if not isinstance(review, Review):
            raise TypeError("Expected a Review instance")
        self._validate_review(review)
        self.__reviews.append(review)
        user.add_review(review)

    def get_reviews(self, page: int, page_size: int, sort_method: str) -> list[
        Review]:
        """
        Returns a list of all Reviews in the repository, sorted by sort_method.
        The sort_method can be: date, rating, or user.
        Pagination is applied using page and page_size.
        """
        if sort_method == SORT_METHOD_DATE:
            sorted_reviews = sorted(self.__reviews, key=lambda r: r.date)
        elif sort_method == SORT_METHOD_RATING:
            sorted_reviews = sorted(self.__reviews, key=lambda r: r.rating if r.rating is not None else float('-inf'),
                                    reverse=True)
        elif sort_method == SORT_METHOD_USER:
            sorted_reviews = sorted(self.__reviews,
                                    key=lambda r: r.user.username)
        else:
            raise ValueError(f"Invalid sort method: {sort_method}")

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return sorted_reviews[start_index:end_index]

    def get_user_reviews(self, page: int, page_size: int, user: User,
                         sort_method: str) -> list[Review]:
        """
        Returns a list of Reviews submitted by the specified User, sorted by sort_method.
        The sort_method can be: date, rating, or recipe.
        Pagination is applied using page and page_size.
        """
        if not isinstance(user, User):
            raise TypeError("Expected a User instance")
        user_reviews = [review for review in self.__reviews if
                        review.user == user]
        if sort_method == SORT_METHOD_DATE:
            return sorted(user_reviews, key=lambda r: r.date)
        elif sort_method == SORT_METHOD_RATING:
            return sorted(user_reviews, key=lambda r: r.rating if r.rating is not None else float('-inf'), reverse=True)
        elif sort_method == SORT_METHOD_RECIPE:
            return sorted(user_reviews, key=lambda r: r.recipe.name)
        else:
            raise ValueError(f"Invalid sort method: {sort_method}")

    def get_recipe_reviews(self, page: int, page_size: int, recipe: Recipe,
                           sort_method: str) -> list[Review]:
        """
        Returns a list of Reviews for the specified Recipe, sorted by sort_method.
        The sort_method can be: date, rating, or user.
        Pagination is applied using page and page_size.
        """
        if not isinstance(recipe, Recipe):
            raise TypeError("Expected a Recipe instance")
        recipe_reviews = recipe.reviews
        if sort_method == SORT_METHOD_DATE:
            sorted_reviews = sorted(recipe_reviews, key=lambda r: r.date)
        elif sort_method == SORT_METHOD_RATING:
            sorted_reviews = sorted(recipe_reviews, key=lambda r: r.rating if r.rating is not None else float('-inf'),
                                    reverse=True)
        elif sort_method == SORT_METHOD_USER:
            sorted_reviews = sorted(recipe_reviews,
                                    key=lambda r: r.user.username)
        else:
            raise ValueError(f"Invalid sort method: {sort_method}")

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return sorted_reviews[start_index:end_index]

    def get_recipes_reviewed_by_user(self, page: int, page_size: int,
                                     user: User, sort_method: str) -> \
            list[Recipe]:
        """
        Returns a list of Recipes reviewed by the specified User, sorted by sort_method.
        The sort_method can be: date, name, or author.
        Pagination is applied using page and page_size.
        """
        if not isinstance(user, User):
            raise TypeError("Expected a User instance")
        user_reviews = user.reviews
        reviewed_recipes = [review.recipe for review in user_reviews]
        if sort_method == SORT_METHOD_DATE:
            sorted_recipes = sorted(reviewed_recipes, key=lambda r: r.date)
        elif sort_method == SORT_METHOD_NAME:
            sorted_recipes = sorted(reviewed_recipes, key=lambda r: r.name)
        elif sort_method == SORT_METHOD_AUTHOR:
            sorted_recipes = sorted(reviewed_recipes,
                                    key=lambda r: r.author.name)
        else:
            raise ValueError(f"Invalid sort method: {sort_method}")
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return sorted_recipes[start_index:end_index]

    def get_review_by_id(self, review_id: int) -> Review | None:
        """
        Returns the Review with the specified review_id from the repository.
        If there is no Review with the given review_id, this method returns None.
        """
        for review in self.__reviews:
            if review.id == review_id:
                return review
        return None

    #endregion

    #region User_data Methods to manage Users
    def add_user(self, user: User):
        if not isinstance(user, User):
            raise TypeError("Expected a User instance")
        if user.id is None:
            user._User__id = self._next_user_id
            self._next_user_id += 1
        self._validate_user(user)
        self.__users.append(user)

    def get_user(self, username: str) -> User | None:
        for user in self.__users:
            if user.username == username:
                return user
        return None

    #endregion

    #region User_favourite_recipes Methods to manage User's favourite Recipes
    def add_favourite_recipe(self, user: User, recipe: Recipe):
        """
        Adds a Recipe to the user's list of favourite recipes.
        The user must be an instance of User, and the recipe must be an instance of Recipe.
        """
        if not isinstance(user, User):
            raise TypeError("Expected a User instance")
        if not isinstance(recipe, Recipe):
            raise TypeError("Expected a Recipe instance")
        if recipe not in user.favourite_recipes:
            user.favourite_recipes.append(recipe)

    def remove_favourite_recipe(self, user: User, recipe: Recipe):
        """
        Removes a Recipe from the user's list of favourite recipes.
        The user must be an instance of User, and the recipe must be an instance of Recipe.
        """
        if not isinstance(user, User):
            raise TypeError("Expected a User instance")
        if not isinstance(recipe, Recipe):
            raise TypeError("Expected a Recipe instance")
        if recipe in user.favourite_recipes:
            user.favourite_recipes.remove(recipe)

    def get_favourite_recipes(self, page: int, page_size: int, user: User) -> \
    list[Recipe]:
        """
        Returns a list of the user's favourite Recipes, sorted by name.
        Pagination is applied using page and page_size.
        """
        if not isinstance(user, User):
            raise TypeError("Expected a User instance")
        favourite_recipes = user.favourite_recipes
        sorted_recipes = sorted(favourite_recipes, key=lambda r: r.name)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return sorted_recipes[start_index:end_index]

    #endregion

    #region Nutrition_data Methods to manage Nutrition
    def add_nutrition(self, nutrition: Nutrition):
        self.__nutritions.append(nutrition)

    #endregion

    #region Recipe Images, Ingredients, and Instructions Methods
    def get_recipe_images(self, recipe_id: int) -> List:
        """
        Returns a list of RecipeImage objects for the specified recipe.
        For memory repository, this returns an empty list since images are stored directly in Recipe.images.
        """
        return []

    def get_recipe_ingredients(self, recipe_id: int) -> List:
        """
        Returns a list of RecipeIngredient objects for the specified recipe.
        For memory repository, this returns an empty list since ingredients are stored directly in Recipe.ingredients.
        """
        return []

    def get_recipe_instructions(self, recipe_id: int) -> List:
        """
        Returns a list of RecipeInstruction objects for the specified recipe.
        For memory repository, this returns an empty list since instructions are stored directly in Recipe.instructions.
        """
        return []

    def add_multiple_recipe_images(self, recipe_images: List):
        """
        Adds multiple RecipeImage objects to the repository.
        For memory repository, this is a no-op since images are stored directly in Recipe.images.
        """
        pass

    def add_multiple_recipe_ingredients(self, recipe_ingredients: List):
        """
        Adds multiple RecipeIngredient objects to the repository.
        For memory repository, this is a no-op since ingredients are stored directly in Recipe.ingredients.
        """
        pass

    def add_multiple_recipe_instructions(self, recipe_instructions: List):
        """
        Adds multiple RecipeInstruction objects to the repository.
        For memory repository, this is a no-op since instructions are stored directly in Recipe.instructions.
        """
        pass
    #endregion

    def _validate_author(self, author: Author):
        if not isinstance(author, Author):
            raise TypeError("Expected an Author instance")
        if author in self.__authors:
            raise FileExistsError(
                f"Author {author.name} already exists in repository")
        if not author.name:
            raise ValueError("Author name cannot be empty")
        if not isinstance(author.name, str):
            raise TypeError("Author name must be a string")
        if author.id < 0:
            raise ValueError("Author ID must be a non-negative integer")
        if not isinstance(author.recipes, list) or not all(
                isinstance(recipe, Recipe) for recipe in author.recipes):
            raise TypeError(
                "Author recipes must be a list of Recipe instances")
        return

    def _validate_category(self, category: Category):
        if category in self.__categories:
            raise FileExistsError(
                f"Category {category.name} already exists in repository")
        if not category.name:
            raise ValueError("Category name cannot be empty")
        if not isinstance(category.name, str):
            raise TypeError("Category name must be a string")
        return

    def _validate_recipe(self, recipe: Recipe):
        if not isinstance(recipe, Recipe):
            raise TypeError("Expected a Recipe instance")
        if recipe.author not in self.__authors:
            raise ValueError(
                f"Author {recipe.author.name} not found in repository")
        if recipe.category not in self.__categories:
            raise ValueError(
                f"Category {recipe.category.name} not found in repository")
        if any(r.id == recipe.id for r in self.__recipes):
            raise FileExistsError(
                f"Recipe with ID {recipe.id} already exists in repository")
        if recipe.rating is not None:
            if not (0 <= recipe.rating <= 5):
                raise ValueError("Rating must be between 0 and 5")
        if not isinstance(recipe.date, datetime):
            raise TypeError("Expected a datetime instance for date")
        if recipe in self.__recipes:
            raise FileExistsError("Recipe already exists in the repository")
        if recipe.id < 0:
            raise ValueError("Recipe ID must be a non-negative integer")
        if not isinstance(recipe.name, str) or not recipe.name:
            raise ValueError("Recipe name must be a non-empty string")
        if not isinstance(recipe.author, Author):
            raise TypeError("Expected an Author instance for author")
        if not isinstance(recipe.category, Category):
            raise TypeError("Expected a Category instance for category")
        if not isinstance(recipe.images, list) or not all(
                isinstance(img, str) for img in recipe.images):
            raise TypeError("Expected a list of strings for images")
        if not isinstance(recipe.ingredients, list) or not all(
                isinstance(ing, str) for ing in recipe.ingredients):
            raise TypeError("Expected a list of strings for ingredients")
        if not isinstance(recipe.ingredient_quantities, list) or not all(
                isinstance(qty, str) for qty in recipe.ingredient_quantities):
            raise TypeError(
                "Expected a list of strings for ingredient quantities")
        if not isinstance(recipe.description, str) or not recipe.description:
            raise ValueError("Recipe description must be a non-empty string")
        if not (isinstance(recipe.rating, float) or recipe.rating is None):
            print(recipe.rating)
            print(type(recipe.rating))
            raise ValueError("Recipe rating must be an float or None")
        return

    def _validate_review(self, review: Review):
        if not isinstance(review, Review):
            raise TypeError("Expected a Review instance")
        if review.user not in self.__users:
            raise ValueError(
                f"User {review.user.username} not found in repository")
        if review.recipe not in self.__recipes:
            raise ValueError(
                f"Recipe {review.recipe.name} not found in repository")
        if not (0 <= review.rating <= 5):
            raise ValueError("Rating must be between 0 and 5")
        if not isinstance(review.date, datetime):
            raise TypeError("Expected a datetime instance for date")
        return

    def _validate_user(self, user):
        if user in self.__users:
            raise FileExistsError(
                f"User {user.username} already exists in repository")
        if user.username in [u.username for u in self.__users]:
            raise FileExistsError(
                f"Username {user.username} already exists in repository")
        if not user.username:
            raise ValueError("Username cannot be empty")
        if not isinstance(user.username, str):
            raise TypeError("Username must be a string")
        if not user.password:
            raise ValueError("Password cannot be empty")
        if not isinstance(user.password, str):
            raise TypeError("Password must be a string")
        return

    #region Tag_data Methods to manage Tags
    def add_tag(self, tag: Tag):
        if not isinstance(tag, Tag):
            raise TypeError("Expected a Tag instance")
        if tag.id is None:
            tag._Tag__id = self._next_tag_id
            self._next_tag_id += 1
        
        # Check if tag already exists (by name since tags should be unique by name)
        existing_tag = self.get_tag_by_name(tag.name)
        if existing_tag:
            raise FileExistsError(f"Tag '{tag.name}' already exists")
        
        self.__tags.append(tag)

    def get_tag_by_name(self, name: str) -> Tag | None:
        normalized_name = name.lower().strip()
        for tag in self.__tags:
            if tag.name == normalized_name:
                return tag
        return None

    def get_tags(self) -> List[Tag]:
        return sorted(self.__tags, key=lambda tag: tag.name)

    def get_recipes_by_tag(self, page: int, page_size: int, tag: Tag) -> List[Recipe]:
        recipes_with_tag = [recipe for recipe in self.__recipes if recipe.has_tag(tag)]
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return recipes_with_tag[start_index:end_index]

    def get_recipes_by_tag_names(self, page: int, page_size: int, tag_names: List[str]) -> List[Recipe]:
        normalized_names = [name.lower().strip() for name in tag_names]
        recipes_with_tags = []
        
        for recipe in self.__recipes:
            recipe_tag_names = recipe.tag_names
            if any(tag_name in recipe_tag_names for tag_name in normalized_names):
                recipes_with_tags.append(recipe)
        
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return recipes_with_tags[start_index:end_index]
    #endregion

    def _sort_recipes(self, recipes: List[Recipe], sort_method: str) -> List[Recipe]:
        if sort_method == SORT_METHOD_NAME:
            sorted_recipes = sorted(recipes, key=lambda r: r.name)
        elif sort_method == SORT_METHOD_DATE:
            sorted_recipes = sorted(recipes, key=lambda r: r.date)
        elif sort_method == SORT_METHOD_RATING:
            sorted_recipes = sorted(recipes, key=lambda r: r.rating if r.rating is not None else float('-inf'),
                                    reverse=True)
        else:
            raise ValueError(f"Invalid sort method: {sort_method}")
        return sorted_recipes
