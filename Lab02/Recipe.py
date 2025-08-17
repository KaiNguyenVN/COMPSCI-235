from datetime import datetime, timedelta
from Category import Category
from tkinter import image_types
from turtledemo.sorting_animate import instructions1


class Recipe:
    def __init__(self, name: str, image: str, ingredients: str, author: str, date: datetime, ingredient_quantities: str, preparation_time: str, instructions: str, category: Category, id: int, cook_time: timedelta, recipe_yield: str, servings: str, description: str):
        self.__name = name
        self.__image = image
        self.__ingredients = ingredients
        self.__author = author
        self.__date = date
        self.__rating = []
        self.__ingredient_quantities = ingredient_quantities
        self.__preparation_time = preparation_time
        self.__instructions = instructions
        self.__category = category
        self.__id = id
        self.__cook_time = cook_time
        self.__recipe_yield = recipe_yield
        self.__servings = servings
        self.__description = description
        self.__reviews = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty")
        self.__name = value

    @property
    def image(self):
        return self.__image

    @property
    def ingredients(self):
        return self.__ingredients

    @ingredients.setter
    def ingredients(self, value: str):
        if not value:
            raise ValueError("Ingredients cannot be empty")
        self.__ingredients = value

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value: str):
        if not value:
            raise ValueError("Author cannot be empty")
        self.__author = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value: str):
        self.__date = datetime.strptime(value, '%Y-%m-%d').date()

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value: int):
        if not value:
            raise ValueError("Rating cannot be empty")
        self.__rating = value


    @property
    def ingredient_quantities(self):
        return self.__ingredient_quantities

    @ingredient_quantities.setter
    def ingredient_quantities(self, value: str):
        if not value:
            raise ValueError("Ingredient quantities cannot be empty")
        self.__ingredient_quantities = value

    @property
    def preparation_time(self):
        return self.__preparation_time

    @preparation_time.setter
    def preparation_time(self, value: str):
        if not value:
            raise ValueError("Preparation time cannot be empty")
        self.__preparation_time = value

    @property
    def instructions(self):
        return self.__instructions

    @instructions.setter
    def instructions(self, value: str):
        if not value:
            raise ValueError("Instructions cannot be empty")
        self.__instructions = value

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value: str):
        if not value:
            raise ValueError("Category cannot be empty")
        self.__category = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: int):
        if not value:
            raise ValueError("Id cannot be empty")
        self.__id = value

    @property
    def cook_time(self):
        return self.__cook_time

    @cook_time.setter
    def cook_time(self, value: str):
        if not value:
            raise ValueError("Cook time cannot be empty")
        self.__cook_time = value

    @property
    def recipe_yield(self):
        return self.__recipe_yield

    @recipe_yield.setter
    def recipe_yield(self, value: str):
        if not value:
            raise ValueError("Recipe yield cannot be empty")
        self.__recipe_yield = value

    @property
    def servings(self):
        return self.__servings

    @servings.setter
    def servings(self, value: str):
        if not value:
            raise ValueError("Servings cannot be empty")
        self.__servings = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value: str):
        if not value:
            raise ValueError("Description cannot be empty")
        self.__description = value

    @property
    def reviews(self):
        return self.__reviews

    @reviews.setter
    def reviews(self, value: str):
        if not value:
            raise ValueError("Reviews cannot be empty")
        self.__reviews = value

    def add_rating(self, rating: "Recipe"):
        self.__rating.append(rating)

    def add_reviews(self, reviews: "Recipe"):
        self.__rating.extend(reviews)



