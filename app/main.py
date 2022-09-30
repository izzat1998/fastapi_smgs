import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from .routers import smgs, train

app = FastAPI(
    title='SMGS', openapi_url="/api/v1/smgs/openapi.json",
    docs_url="/api/v1/smgs/docs")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/smgs/static", StaticFiles(directory="static"), name="static")
app.include_router(smgs.router, prefix="/api/v1/smgs/smgs")
app.include_router(train.router, prefix="/api/v1/smgs/train")
