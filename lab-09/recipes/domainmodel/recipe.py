from datetime import datetime

from recipes.domainmodel.review import Review
# from recipes.domainmodel.author import "Author"  # import here to avoid circular imports if needed
# from recipes.domainmodel.category import Category
# from recipes.domainmodel.nutrition import Nutrition

class Recipe:
    def __init__(self, id: int, name: str, author: "Author", cook_time: int,
                 preparation_time: int, date: datetime, description: str,
                 images: list[str], category: "Category",
                 ingredient_quantities: list[str],
                 ingredients: list[str], rating: float | None, nutrition: "Nutrition",
                 servings: str | None, recipe_yield: str | None, instructions: list[str]) -> object:
        self.__id = id
        self.__name = name
        self.__author = author
        self.__cook_time = cook_time
        self.__preparation_time = preparation_time
        self.__date = date
        self.__description = description
        self.__images = images
        self.__category = category
        self.__ingredient_quantities = ingredient_quantities
        self.__ingredients = ingredients
        self.__rating = rating
        self.__nutrition = nutrition
        self.__servings = servings if servings is not None else "Not specified"
        self.__recipe_yield = recipe_yield if recipe_yield is not None else "Not specified"
        self.__instructions = instructions
        self.__reviews = []

    def __repr__(self) -> str:
        return (f"<Recipe {self.__name} with id: {self.id} was created by {self.__author.name} "
            f"on {self.__date}>")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Recipe):
            return False
        return self.id == other.id

    def __lt__(self, other) -> bool:
        if not isinstance(other, Recipe):
            raise TypeError("Comparison must be between Recipe instances")
        return self.id < other.id

    def __hash__(self) -> int:
        return hash(self.__id)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def author(self) -> "Author":
        return self.__author

    @author.setter
    def author(self, author: "Author"):
        self.__author = author

    @property
    def cook_time(self) -> int:
        return self.__cook_time

    @property
    def preparation_time(self) -> int:
        return self.__preparation_time

    @property
    def date(self) -> datetime:
        return self.__date

    @property
    def description(self) -> str:
        return self.__description

    @property
    def images(self) -> list[str]:
        return self.__images

    @property
    def category(self) -> "Category":
        return self.__category

    @property
    def ingredient_quantities(self) -> list[str]:
        return self.__ingredient_quantities

    @property
    def ingredients(self) -> list[str]:
        return self.__ingredients

    @property
    def rating(self) -> float | None:
        return self.__rating

    @property
    def nutrition(self) -> "Nutrition":
        return self.__nutrition

    @property
    def servings(self) -> str:
        return self.__servings

    @property
    def recipe_yield(self) -> str:
        return self.__recipe_yield

    @property
    def instructions(self) -> list[str]:
        return self.__instructions

    @property
    def reviews(self) -> list[Review]:
        return self.__reviews

    def add_review(self, review: Review) -> None:
        if isinstance(review, Review):
            self.__reviews.append(review)
            self.__update_rating()
        else:
            raise TypeError("Expected a Review instance")

    def remove_review(self, review: Review) -> None:
        if review in self.__reviews:
            self.__reviews.remove(review)
            self.__update_rating()
        else:
            raise ValueError("Review not found in recipe's reviews")

    def __update_rating(self) -> None:
        if self.__reviews:
            ratings = [r.rating for r in self.__reviews if
                       hasattr(r, "rating") and r.rating is not None]
            if ratings:
                average_rating = sum(ratings) / len(ratings)
                self.__rating = round(average_rating, 1)
            else:
                self.__rating = None
        else:
            self.__rating = None

    def set_author(self, author: "Author") -> None:
        from recipes.domainmodel.author import Author  # lazy import

        if not isinstance(author, Author):
            raise TypeError(f"Expected Author instance, got {type(author).__name__}")
        self.__author = author