import os
import zipfile
from io import BytesIO
from typing import List, Optional


from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response, StreamingResponse

from .. import schemas, models

from ..crud.train_crud import Train
from ..database import get_db


router = APIRouter(
    prefix='/api/v1/train',
    tags=['Train']
)


@router.get('/', response_model=List[schemas.TrainOut])
async def get_train_list(limit: int = 100, skip: int = 0, search: Optional[str] = "", db: Session = Depends(get_db)):
    train_list = Train.get_all(limit=limit, skip=skip, search=search, db=db)
    return train_list


@router.get('/smgs_list', response_model=List[schemas.TrainWithSMGS])
async def get_train_smgs_list(db: Session = Depends(get_db)):
    train_list = db.query(models.Train).all()
    for train in train_list:
        smgs_list = db.query(models.SMGS).filter(models.SMGS.train_id == train.id).all()
        train.smgs_list = smgs_list
        train.count = len(smgs_list)
    return train_list


@router.post('/', response_model=schemas.TrainOut)
async def create_train(train: schemas.TrainCreate, db: Session = Depends(get_db)):
    if Train.get_train_by_name(train.dict().get('name'), db=db) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Already exists train with {train.dict().get('name')}"
        )
    new_train = Train.add_train(train.dict().get('name'), db=db)
    return new_train


@router.get('/{pk}', response_model=schemas.TrainOut)
async def get_train(pk: int, db: Session = Depends(get_db)):
    train = Train.get_train(pk=pk, db=db)
    if train is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Train does not exist with id {pk}"
        )
    return train


@router.put('/{pk}', response_model=schemas.TrainOut)
async def get_update(pk: int, train: schemas.TrainUpdate, db: Session = Depends(get_db)):
    if Train.get_train(pk=pk, db=db) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Train does not exist with id {pk}"
        )
    updated_train = Train.update_train(pk=pk, updated_train=train.dict(), db=db)
    return updated_train


@router.delete('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_train(pk: int, db: Session = Depends(get_db)):
    train = Train.get_train(pk=pk, db=db)
    if train is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Train with {pk} does not exist')
    Train.delete_train(pk=pk, db=db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('zip/{pk}', status_code=status.HTTP_201_CREATED)
async def create_zip(pk: int, smgs_type: Optional[str] = "", db: Session = Depends(get_db)):
    train = Train.get_train(pk=pk, db=db)
    if train is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Train with {pk} does not exist')

    smgs_query = db.query(models.SMGS).filter(models.SMGS.train_id == pk)

    io = BytesIO()
    zip_sub_dir = train.name
    zip_filename = "%s.zip" % zip_sub_dir
    with zipfile.ZipFile(io, mode='w', compression=zipfile.ZIP_DEFLATED) as zip:
        for smgs in smgs_query.all():
            if smgs_type == 'draft':
                draft_file = os.path.abspath(os.path.join(os.path.basename(__file__), '../' + smgs.file_draft))
                zip.write(draft_file)
            elif smgs_type == 'original':
                original_file = os.path.abspath(os.path.join(os.path.basename(__file__), '../' + smgs.file_original))
                zip.write(original_file)
            else:
                draft_file = os.path.abspath(os.path.join(os.path.basename(__file__), '../' + smgs.file_draft))
                original_file = os.path.abspath(os.path.join(os.path.basename(__file__), '../' + smgs.file_original))
                zip.write(draft_file)
                zip.write(original_file)
        zip.close()
    return StreamingResponse(
        iter([io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment;filename=%s" % zip_filename}
    )
