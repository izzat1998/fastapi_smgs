from datetime import datetime
from typing import Union, List

from pydantic import BaseModel


class TrainBase(BaseModel):
    name: str
    user_id: Union[int, None] = None


class TrainCreate(TrainBase):
    pass


class TrainUpdate(TrainBase):
    pass


class TrainOut(TrainBase):
    id: int
    excel_file: Union[str, None] = None

    class Config:
        orm_mode = True


class TrainMainOut(TrainBase):
    id: int
    smgs_count: int = 0
    excel_file: Union[str, None] = None


    class Config:
        orm_mode = True


class SMGSBase(BaseModel):
    railway_code: Union[str, None] = None
    sender: Union[str, None] = None
    departure_station: Union[str, None] = None
    sender_statement: Union[str, None] = None
    recipient: Union[str, None] = None
    destination_station: Union[str, None] = None
    border_crossing_stations: Union[str, None] = None
    railway_carriage: Union[str, None] = None
    shipping_name: Union[str, None] = None
    container_owner: Union[str, None] = None
    container: Union[str, None] = None
    container_type: Union[str, None] = None
    container_type_code: Union[str, None] = None
    type_of_packaging: Union[str, None] = None
    number_of_seats: Union[str, None] = None
    net: Union[str, None] = None
    tara: Union[str, None] = None
    gross: Union[str, None] = None
    seals: Union[str, None] = None
    seal_quantity: Union[str, None] = None
    submerged: Union[str, None] = None
    method_of_determining_mass: Union[str, None] = None
    payment_of_legal_fees: Union[str, None] = None
    carriers: Union[str, None] = None
    documents_by_sender: Union[str, None] = None
    additional_information: Union[str, None] = None
    custom_seal: Union[str, None] = None
    inspector_name: Union[str, None] = None
    date: Union[str, None] = None


class SMGSOut(SMGSBase):
    id: Union[int, None] = None
    file_draft: Union[str, None] = None
    file_original: Union[str, None] = None
    created_at: Union[datetime, None] = None
    train: TrainOut

    class Config:
        orm_mode = True


class SMGSTrain(SMGSBase):
    id: Union[int, None] = None
    file_draft: Union[str, None] = None
    file_original: Union[str, None] = None
    created_at: Union[datetime, None] = None

    class Config:
        orm_mode = True


class SMGSCreate(SMGSBase):
    train_name: str
    pass


class SMGSUpdate(SMGSBase):
    train_id: int


class TrainWithSMGS(TrainOut):
    smgs_list: List[SMGSTrain] = None
    count: int = None

    class Config:
        orm_mode = True
