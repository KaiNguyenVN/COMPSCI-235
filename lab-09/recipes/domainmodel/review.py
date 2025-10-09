from recipes.domainmodel.user import User
from datetime import datetime

class Review:
    def __init__(self, id: int, user: User, date: datetime, recipe: "Recipe", rating: float, comment: str):
        self.__id = id
        self.__user = user
        self.__date = date
        self.__recipe = recipe
        if not (0 <= rating <= 5):
            raise ValueError("Rating must be between 0 and 5")
        else:
            self.__rating = rating
        self.__comment = comment

    def __repr__(self) -> str:
        return f"<Review: User: {self.user}, Recipe: {self.recipe}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Review):
            return False
        return self.id == other.id

    def __lt__(self, other) -> bool:
        if not isinstance(other, Review):
            raise TypeError("Comparison must be between Review instances")
        if self.__rating is None:
            return False
        if other.__rating is None:
            return True
        return self.__rating < other.__rating

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def user(self) -> User:
        return self.__user

    @property
    def date(self) -> datetime:
        return self.__date

    @property
    def recipe(self) -> "Recipe":
        return self.__recipe

    @property
    def rating(self) -> float:
        return self.__rating

    @property
    def comment(self) -> str:
        return self.__comment

    def update_rating(self, new_rating: float) -> None:
        if not (0 <= new_rating <= 5):
            raise ValueError("Rating must be between 0 and 5")
        self.__rating = new_rating

    def update_comment(self, new_comment: str) -> None:
        self.__comment = new_comment
