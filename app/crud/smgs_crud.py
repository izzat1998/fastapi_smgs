from fastapi import Depends
from sqlalchemy.orm import Session

from app import models
from ..database import get_db
from ..utils.convert_excel_to_docx import SMGSDOCX


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
            "container": smgs["container"],
            "railway_code": smgs["railway_code"],
            "sender": smgs["sender"],
            "border_crossing_stations": smgs["border_crossing_stations"],
            "railway_carriage": smgs["railway_carriage"],
            "shipping_name": smgs["shipping_name"],
            "container_owner": smgs["container_owner"],
            "type_of_packaging": smgs["type_of_packaging"],
            "number_of_seats": smgs["number_of_seats"],
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
        smgs_query.delete(synchronize_session=False)
        db.commit()

    @classmethod
    def update_smgs(cls, pk: int, updated_smgs: dict, db: Session = Depends(get_db)):
        smgs_query = db.query(cls.model).filter(cls.model.id == pk)
        smgs_query.update(updated_smgs, synchronize_session=False)
        db.commit()
        return smgs_query.first()
