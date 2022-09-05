from sqlalchemy import Integer, Column, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship

from .database import Base


class SMGS(Base):
    __tablename__ = 'smgs'

    id = Column(Integer, primary_key=True, nullable=False)
    railway_code = Column(String, nullable=True)
    sender = Column(String, nullable=True)
    departure_station = Column(String, nullable=True)
    sender_statement = Column(String, nullable=True)
    recipient = Column(String, nullable=True)
    destination_station = Column(String, nullable=True)
    border_crossing_stations = Column(String, nullable=True)
    railway_carriage = Column(String, nullable=True)
    shipping_name = Column(String, nullable=True)
    container_owner = Column(String, nullable=True)
    container = Column(String, nullable=True)
    container_type = Column(String, nullable=True)
    container_type_code = Column(String, nullable=True)
    type_of_packaging = Column(String, nullable=True)
    number_of_seats = Column(String, nullable=True)
    net = Column(String, nullable=True)
    tara = Column(String, nullable=True)
    gross = Column(String, nullable=True)
    seals = Column(String, nullable=True)
    seal_quantity = Column(String, nullable=True)
    submerged = Column(String, nullable=True)
    method_of_determining_mass = Column(String, nullable=True)
    payment_of_legal_fees = Column(String, nullable=True)
    carriers = Column(String, nullable=True)
    documents_by_sender = Column(String, nullable=True)
    additional_information = Column(String, nullable=True)
    custom_seal = Column(String, nullable=True)
    inspector_name = Column(String, nullable=True)
    date = Column(String, nullable=True)
    file_draft = Column(String, nullable=True)
    file_original = Column(String, nullable=True)
    train_id = Column(Integer, ForeignKey('trains.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    train = relationship("Train")


class Train(Base):
    __tablename__ = 'trains'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    excel_file = Column(String, nullable=True)
