from sqlalchemy import select, inspect
from recipes.adapters.orm import mapper_registry


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    tables = inspector.get_table_names()

    # Check all required tables are there
    assert 'recipes' in tables
    assert 'authors' in tables
    assert 'nutrition' in tables
    assert 'recipe_images' in tables


    assert inspector.get_table_names(
    ) == ['authors',
          'nutrition',
          'recipe_images',
          'recipes']


def test_database_populate_all_recipes(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    # recipes table is at index 6 alphabetically
    recipes_table_name = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table recipes
        select_statement = select(mapper_registry.metadata.tables[recipes_table_name])
        result = connection.execute(select_statement)

        recipes = []
        for row in result:
            recipes.append((row[0], row[1]))

        nr_recipes = len(recipes)
        assert nr_recipes == 13

        # First row is recipe 'D-Hour Radio Network' with recipe_id 1.
        assert recipes[0] == (38, 'Low-Fat Berry Blue Frozen Dessert')


def test_database_populate_all_nutrients(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    # nutrition table is at index 1 alphabetically
    nutrients_table_name = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table nutrition
        select_statement = select(mapper_registry.metadata.tables[nutrients_table_name])
        result = connection.execute(select_statement)

        nutrients = []
        for row in result:
            nutrients.append((row[0], row[1], row[2], row[3], row[4], row[5]))

        nr_nutrients = len(nutrients)
        # There are total 13 nutrients in the test dataset, same as the number of recipes.
        assert nr_nutrients == 13

        # Check the first row, few columns of the table nutrition
        assert nutrients[0] == (38, 170.9, 2.5, 1.3, 8.0, 29.8)


# TODO: Verify the data loading process for Authors.
def test_database_populate_all_authors(database_engine):
    inspector = inspect(database_engine)
    authors_table_name = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[authors_table_name])
        result = connection.execute(select_statement)

        authors = []
        for row in result:
            authors.append((row[0], row[1]))

        nr_authors = len(authors)
        assert nr_authors == 11

        assert authors[0] == (1533, 'Dancer')