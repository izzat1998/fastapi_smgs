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

    def create_train_model(train):
        return models.Train(**train)

    trains = list(map(create_train_model, train_data))
    session.add_all(trains)
    session.commit()
    trains = session.query(models.Train).all()
    return trains


@pytest.fixture
def test_smgs(session,test_trains):
    smgs_data = [
        {
            "railway_code": "12346",
            "sender": "sender",
            "departure_station": "departure_station",
            "sender_statement": "sender_statement",
            "recipient": "recipient",
            "destination_station": "destination_station",
            "border_crossing_stations": "border_crossing_stations",
            "railway_carriage": "railway_carriage",
            "shipping_name": "shipping_name",
            "container_owner": "container_owner",
            "container": "WSCU19982132",
            "type_of_packaging": "type_of_packaging",
            "number_of_seats": "number_of_seats",
            "net": "net",
            "tara": "tara",
            "gross": "gross",
            "seals": "seals",
            "seal_quantity": "seal_quantity",
            "submerged": "submerged",
            "method_of_determining_mass": "method_of_determining_mass",
            "payment_of_legal_fees": "payment_of_legal_fees",
            "carriers": "carriers",
            "documents_by_sender": "documents_by_sender",
            "additional_information": "additional_information",
            "custom_seal": "custom_seal",
            "inspector_name": "inspector_name",
            "date": "2022/16/8"
        }, {
            "railway_code": "12346",
            "sender": "sender",
            "departure_station": "departure_station",
            "sender_statement": "sender_statement",
            "recipient": "recipient",
            "destination_station": "destination_station",
            "border_crossing_stations": "border_crossing_stations",
            "railway_carriage": "railway_carriage",
            "shipping_name": "shipping_name",
            "container_owner": "container_owner",
            "container": "TGHU19980228",
            "type_of_packaging": "type_of_packaging",
            "number_of_seats": "number_of_seats",
            "net": "net",
            "tara": "tara",
            "gross": "gross",
            "seals": "seals",
            "seal_quantity": "seal_quantity",
            "submerged": "submerged",
            "method_of_determining_mass": "method_of_determining_mass",
            "payment_of_legal_fees": "payment_of_legal_fees",
            "carriers": "carriers",
            "documents_by_sender": "documents_by_sender",
            "additional_information": "additional_information",
            "custom_seal": "custom_seal",
            "inspector_name": "inspector_name",
            "date": "2022/16/8"
        }, {
            "railway_code": "12346",
            "sender": "sender",
            "departure_station": "departure_station",
            "sender_statement": "sender_statement",
            "recipient": "recipient",
            "destination_station": "destination_station",
            "border_crossing_stations": "border_crossing_stations",
            "railway_carriage": "railway_carriage",
            "shipping_name": "shipping_name",
            "container_owner": "container_owner",
            "container": "CLMU12021120",
            "type_of_packaging": "type_of_packaging",
            "number_of_seats": "number_of_seats",
            "net": "net",
            "tara": "tara",
            "gross": "gross",
            "seals": "seals",
            "seal_quantity": "seal_quantity",
            "submerged": "submerged",
            "method_of_determining_mass": "method_of_determining_mass",
            "payment_of_legal_fees": "payment_of_legal_fees",
            "carriers": "carriers",
            "documents_by_sender": "documents_by_sender",
            "additional_information": "additional_information",
            "custom_seal": "custom_seal",
            "inspector_name": "inspector_name",
            "date": "2022/16/8"
        }, {
            "railway_code": "12346",
            "sender": "sender",
            "departure_station": "departure_station",
            "sender_statement": "sender_statement",
            "recipient": "recipient",
            "destination_station": "destination_station",
            "border_crossing_stations": "border_crossing_stations",
            "railway_carriage": "railway_carriage",
            "shipping_name": "shipping_name",
            "container_owner": "container_owner",
            "container": "WSCU34231245",
            "type_of_packaging": "type_of_packaging",
            "number_of_seats": "number_of_seats",
            "net": "net",
            "tara": "tara",
            "gross": "gross",
            "seals": "seals",
            "seal_quantity": "seal_quantity",
            "submerged": "submerged",
            "method_of_determining_mass": "method_of_determining_mass",
            "payment_of_legal_fees": "payment_of_legal_fees",
            "carriers": "carriers:",
            "documents_by_sender": "documents_by_sender",
            "additional_information": "additional_information",
            "custom_seal": "custom_seal",
            "inspector_name": "inspector_name",
            "date": "2022/16/8"
        }
    ]

    def create_smgs_model(smgs):
        return models.SMGS(train_id=test_trains[0].id,**smgs)

    smgs_list = list(map(create_smgs_model, smgs_data))
    session.add_all(smgs_list)
    session.commit()
    smgs_list = session.query(models.SMGS).all()
    return smgs_list
