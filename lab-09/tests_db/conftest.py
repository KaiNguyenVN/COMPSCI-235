import pytest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from recipes.adapters import database_repository, populate_repository
from recipes.adapters.orm import mapper_registry, map_model_to_tables


def get_project_root() -> Path:
    return Path(__file__).parent


TEST_DATA_PATH_DATABASE_LIMITED = get_project_root() / "data"

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///recipes-test.db'


@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)

    mapper_registry.metadata.create_all(engine)  # Conditionally create database tables.
    # Remove any data from the tables.
    with engine.begin() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker
    session_factory = sessionmaker(
        autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    populate_repository.populate(
        TEST_DATA_PATH_DATABASE_LIMITED, repo_instance, database_mode=True, testing=True)
    yield engine
    mapper_registry.metadata.drop_all(engine)


# Creates a fresh database session for each test
@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    mapper_registry.metadata.create_all(engine)
    with engine.begin() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(
        autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    populate_repository.populate(
        TEST_DATA_PATH_DATABASE_LIMITED, repo_instance, database_mode=True, testing=True)
    yield session_factory
    mapper_registry.metadata.drop_all(engine)


# A database session with empty tables (no data)
@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    mapper_registry.metadata.create_all(engine)
    with engine.begin() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    mapper_registry.metadata.drop_all(engine)
