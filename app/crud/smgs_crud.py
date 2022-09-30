import os
import pathlib

from fastapi import Depends
from sqlalchemy.orm import Session

from app import models
from ..database import get_db
from ..utils.utils import SMGSDOCX


def remove_file_from_disk(file_path: str) -> None:
    if os.path.exists(file_path):
        rem_file = pathlib.Path(file_path)
        rem_file.unlink()


class SMGS:
    model = models.SMGS

    @classmethod
    def get_all_smgs(cls, limit, skip, search, db: Session = Depends(get_db)):
        return db.query(cls.model).filter(cls.model.sender.contains(search)).limit(limit).offset(skip).all()

    @classmethod
    def get_one_smgs(cls, pk: int, db: Session = Depends(get_db)):
        return db.query(cls.model).filter(cls.model.id == pk).first()

    @classmethod
    def get_smgs_list_by_train(cls, pk: int, db: Session = Depends(get_db)):
        return db.query(cls.model).filter(cls.model.train_id == pk).all()

    @classmethod
    def add_smgs(cls, train_id: int, smgs: dict, db: Session = Depends(get_db)) -> models.SMGS:
        smgs_docx = {

            "railway_code": smgs["railway_code"],
            "sender": smgs["sender"],
            "departure_station": smgs["departure_station"],
            "sender_statement": smgs["sender_statement"],
            "recipient": smgs["recipient"],
            "destination_station": smgs["destination_station"],
            "border_crossing_stations": smgs["border_crossing_stations"],
            "railway_carriage": smgs["railway_carriage"],
            "shipping_name": smgs["shipping_name"],
            "container_owner": smgs["container_owner"],
            "container": smgs["container"],
            "p": smgs["container_type_code"],
            "type": smgs["container_type"],
            "type_of_packaging": smgs["type_of_packaging"],
            "net": smgs["net"],
            "tara": smgs["tara"],
            "gross": smgs["gross"],
            "seals": smgs["seals"],
            "seal_quantity": smgs["seal_quantity"],
            "submerged": smgs["submerged"],
            "method_of_determining_mass": smgs["method_of_determining_mass"],
            "payment_of_legal_fees": smgs["payment_of_legal_fees"],
            "carriers": smgs["carriers"],
            "documents_by_sender": smgs["documents_by_sender"],
            "additional_information": smgs["additional_information"],
            "custom_seal": smgs["custom_seal"],
            "inspector_name": smgs["inspector_name"],
            "date": smgs["date"],

        }
        path = 'static/documents/'
        train = db.query(models.Train).filter(models.Train.id == train_id).first()
        draft, original = SMGSDOCX.create_docx(smgs_data=smgs_docx,
                                               train_name=train.name,
                                               store_path=path)
        new_smgs = cls.model(train_id=train_id, **smgs)
        new_smgs.file_draft = '/' + draft
        new_smgs.file_original = '/' + original
        db.add(new_smgs)
        db.commit()
        db.refresh(new_smgs)
        return new_smgs

    @classmethod
    def delete_smgs(cls, pk: int, db: Session = Depends(get_db)):
        smgs_query = db.query(cls.model).filter(cls.model.id == pk)
        smgs_query.delete(synchronize_session=False)
        db.commit()

    @classmethod
    def delete_train_all_smgs(cls, pk: int, db: Session = Depends(get_db)):
        smgs_query = db.query(cls.model).filter(cls.model.train_id == pk)
        for smgs in smgs_query.all():
            original_file = os.path.abspath(os.path.join(os.path.basename(__file__), '../' + smgs.file_original))
            draft_file = os.path.abspath(os.path.join(os.path.basename(__file__), '../' + smgs.file_draft))
            remove_file_from_disk(original_file)
            remove_file_from_disk(draft_file)
            smgs_query.delete(synchronize_session=False)
            db.commit()

    @classmethod
    def update_smgs(cls, pk: int, updated_smgs: dict, db: Session = Depends(get_db)):
        smgs_query = db.query(cls.model).filter(cls.model.id == pk)
        smgs_query.update(updated_smgs, synchronize_session=False)
        db.commit()
        return smgs_query.first()
