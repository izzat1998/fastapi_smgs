import pytest as pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app import models
from app.config import settings
from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URI = f'postgresql://{settings.database_username}:{settings.database_password}' \
                          f'@{settings.database_hostname}' \
                          f':{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URI)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_trains(session):
    train_data = [
        {"name": "Train 1"},
        {"name": "Train 2"},
        {"name": "Train 3"},
        {"name": "Train 4"},
    ]

    def create_train_model(post):
        return models.Train(**post)

    trains = list(map(create_train_model, train_data))
    session.add_all(trains)
    session.commit()
    trains = session.query(models.Train).all()
    return trains