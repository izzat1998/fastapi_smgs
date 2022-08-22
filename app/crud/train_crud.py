from typing import Optional, List

from fastapi import Depends
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db


class Train:
    model = models.Train

    @classmethod
    def add_train(cls, train_name: str, db: Session = Depends(get_db)) -> schemas.TrainOut:
        new_train = cls.model(name=train_name)
        db.add(new_train)
        db.commit()
        db.refresh(new_train)
        return new_train

    @classmethod
    def get_all(cls, limit, skip, search, db: Session = Depends(get_db)) -> List[schemas.TrainOut]:
        return db.query(cls.model).filter(cls.model.name.contains(search)).limit(limit).offset(skip).all()

    @classmethod
    def get_train(cls, pk: int, db: Session = Depends(get_db)) -> Optional[models.Train]:
        train = db.query(cls.model).filter(cls.model.id == pk).first()
        return train

    @classmethod
    def get_train_by_name(cls, name: str, db: Session = Depends(get_db)) -> Optional[models.Train]:
        train = db.query(cls.model).filter(cls.model.name == name).first()
        return train

    @classmethod
    def update_train(cls, pk: int, updated_train: dict, db: Session = Depends(get_db)):
        train_query = db.query(cls.model).filter(cls.model.id == pk)
        train_query.update(updated_train, synchronize_session=False)
        db.commit()
        return train_query.first()

    @classmethod
    def delete_train(cls, pk: int, db: Session = Depends(get_db)):
        train_query = db.query(cls.model).filter(cls.model.id == pk)
        train_query.delete(synchronize_session=False)
        db.commit()