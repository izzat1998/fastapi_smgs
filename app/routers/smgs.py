from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from .. import schemas
from ..crud.smgs_crud import SMGS
from ..crud.train_crud import Train
from ..database import get_db

router = APIRouter(
    prefix='/api/v1/smgs',
    tags=['Smgs']
)


@router.get('/', response_model=List[schemas.SMGSOut])
async def get_smgs_list(limit: int = 100, skip: int = 0, search: Optional[str] = "", db: Session = Depends(get_db)):
    smgs_list = SMGS.get_all_smgs(limit=limit, skip=skip, search=search, db=db)
    return smgs_list


@router.get('/{pk}', response_model=schemas.SMGSOut, status_code=status.HTTP_200_OK)
async def get_smgs(pk: int, db: Session = Depends(get_db)):
    smgs = SMGS.get_one_smgs(pk, db)
    if not smgs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"SMGS {pk} not found"
        )
    return smgs


@router.get('/train/{pk}', response_model=List[schemas.SMGSOut], status_code=status.HTTP_200_OK)
async def get_smgs_by_train(pk: int, db: Session = Depends(get_db)):
    smgs_list = SMGS.get_smgs_list_by_train(pk=pk, db=db)
    return smgs_list


@router.post('/', response_model=schemas.SMGSOut, status_code=status.HTTP_201_CREATED)
async def create_smgs(smgs: schemas.SMGSCreate, db: Session = Depends(get_db)):
    smgs = smgs.copy().dict()
    train_name = smgs.pop('train_name')
    train = Train.get_train_by_name(train_name, db)
    if train is None:
        train = Train.add_train(train_name, db)
    new_smgs = SMGS.add_smgs(train.id, smgs, db)
    return new_smgs


@router.delete('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_smgs(pk: int, db: Session = Depends(get_db)):
    if SMGS.get_one_smgs(pk, db) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"SMGS {pk} not found"
        )
    SMGS.delete_smgs(pk, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete('/train_smgs/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_train_all_smgs(pk: int, db: Session = Depends(get_db)):
    train = Train.get_train(pk=pk, db=db)
    if train is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Train {pk} not found"
        )
    SMGS.delete_train_all_smgs(pk, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{pk}', response_model=schemas.SMGSOut)
async def update_smgs(pk: int, smgs: schemas.SMGSUpdate, db: Session = Depends(get_db)):
    train_id = smgs.dict().get('train_id')
    if Train.get_train(pk=train_id, db=db) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Train {train_id} not found"
        )
    if SMGS.get_one_smgs(pk, db) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"SMGS {pk} not found"
        )
    updated_smgs = SMGS.update_smgs(pk, smgs.dict(), db)
    return updated_smgs
