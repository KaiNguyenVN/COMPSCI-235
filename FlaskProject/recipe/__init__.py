from flask import Flask
from recipe.domainmodel.author import Author
from recipe.domainmodel.recipe import Recipe

def create_recipes() -> list[Recipe]:
    author1 = Author(12491, 'Christine')
    recipe1 = Recipe(10268, 'Dressed Three Bean Salad', author1,
                     description="Make and share this Dressed Three Bean Salad recipe from Food.com.",
                     ingredients=["beans", "kidney bean", "green pepper", "sugar", "salt", "vinegar", "pepper"],
                     instructions=["Combine all beans, onions and green pepper.", "Heat all dressing ingredients until dissolved and pour over vegetables.", "Let stand 24 hours.", "Stir occasionally."],
                     images=["https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/10/26/8/40u9WTbxTYGS2baVyiCy_IMG_3518.JPG", "https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/10/26/8/picaHnRpl.jpg"])

    author2 = Author(10431, 'Robert Clickner')
    recipe2 = Recipe(10327, 'World\'s Best Potato Salad', author2,
                     description="This is a zesty potato salad that you enjoy at the meal, and you find yourself picking at it in between meals.",
                     ingredients=["white potatoes", "celery", "dill pickle", "pitted black olives", "medium cheddar", "swiss cheese", "parmesan cheese", "red onion", "garlic", "white pepper", "ground black pepper", "dry mustard", "cayenne pepper", "mayonnaise"],
                     instructions=["Peel and wash potatoes; cook in boiling water until just fork tender (do not over cook).", "Cool and dice approximately 1/2 x 1/2-inch; combine with all other diced items (onions, pickles, pepperoni, cheeses, celery and black olives).  Fold all of these ingredients gently with 1/2 cup of mayonnaise until mixed.", "Refrigerate for at least a couple of hours, overnight is even better (this is important).", "Add all spices and the rest of mayonnaise and minced garlic; gently fold until mixed.  Refrigerate 30 minutes to 1 hour before serving."],
                     images=["https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/10/32/7/picafqf0F.jpg"]
    )

    author3 = Author(10404, 'Diana Adams')
    recipe3 = Recipe(9446, 'Ham and Cheese Pie', author3,
                     description="This pie doubles as a formal dinner or picnic dish. It is our favorite savory pie. I don't know where the original came from-somewhere down south but I have added more onion, pepper, nutmeg, cayenne and cheese. Also the original called for regular deli ham-holy salt-it just about killed us! So here you go and by the way I like it best cold.",
                     ingredients=["baking potato", "onion", "butter", "milk", "egg", "dry mustard", "ground cloves", "low-salt ham", "cheddar cheese", "butter", "flour", "white pepper", "ground nutmeg", "cayenne pepper", "milk", "cheddar cheese"],
                     instructions=['Preheat oven to 450 degrees Boil potato-meanwhile cook onion in butter until soft and light brown.', 'In a large bowl beat potato.', 'Add to this the onion, beaten egg, mustard and cloves.', 'Mix well.', 'Fold in ham, 1/2 of the cheese and cheese sauce.', "At this point taste to see if you need a bit of salt-most likely you won't.", 'Turn into deep pastry lined pie plate.', 'Top with remaining crust, crimp and seal.', 'Bake on the lowest rack at 450 for 10 minutes.', 'Reduce heat to 350 degrees and bake for 30 min.', 'Top crust with remaining cheese and cook for about 15 min more.', 'Remove and let stand for 20 minutes or chill and serve cold.', 'Cheese Sauce Directions Melt butter in a medium saucepan.', 'Stir in flour and spices and cook until bubbly.', 'Remove from heat and gradually stir in milk.', 'Return to heat and cook until thick and bubbly.', 'Stir in cheese and cook until melted.'],
                     images=["https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/94/46/w159XplaSiO5N8GPpmhn-158.JPG"]
    )

    return [recipe1, recipe2, recipe3]


def create_app():
    app = Flask(__name__)

    # register blueprints
    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .recipes import recipes
        app.register_blueprint(recipes.browse_blueprint)
        app.register_blueprint(recipes.recipe_detail_blueprint)

    return app