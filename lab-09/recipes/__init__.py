from pathlib import Path
from flask import Flask

# imports from SQLAlchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from recipes.domainmodel.recipe import Recipe
from recipes.browse import browse

# local imports
import recipes.adapters.repository as repo
from recipes.adapters.database_repository import SqlAlchemyRepository
from recipes.adapters.populate_repository import populate
from recipes.adapters.orm import mapper_registry, map_model_to_tables


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    database_uri = 'sqlite:///recipes.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_ECHO'] = True  # echo SQL statements - useful for debugging

    # STEP 2: Create a database engine and connect it to the specified database
    database_engine = create_engine(database_uri, connect_args={"check_same_thread": False},
                                    poolclass=NullPool,
                                    echo=False)

    # STEP 3: Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True,
                                   bind=database_engine)

    # STEP 4: Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo.repo_instance = SqlAlchemyRepository(session_factory)
    data_path = Path('recipes') / 'adapters' / 'data'

    # STEP 4: Repopulate the DB.
    if len(inspect(database_engine).get_table_names()) == 0:
        print("REPOPULATING DATABASE...")
        # For testing, or first-time use of the web application, reinitialise the database.
        clear_mappers()
        # Conditionally create database tables.
        mapper_registry.metadata.create_all(database_engine)
        # Remove any data from the tables.
        for table in reversed(mapper_registry.metadata.sorted_tables):
            with database_engine.connect() as conn:
                conn.execute(table.delete())

        # Generate mappings that map domain model classes to the database tables.
        map_model_to_tables()

        populate(data_path, repo.repo_instance, True)
        print("REPOPULATING DATABASE... FINISHED")

    else:
        # Solely generate mappings that map domain model classes to the database tables.
        map_model_to_tables()

    with app.app_context():
        # Register the browse blueprint to the app instance.
        from .home import home
        app.register_blueprint(home.home_blueprint)
        app.register_blueprint(browse.browse_blueprint)

        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, SqlAlchemyRepository):
                repo.repo_instance.close_session()

    return app
