from fastapi import FastAPI
from dotenv import load_dotenv
from src.routes import base
from src.routes import data

load_dotenv(".env")

from src.routes import base

app = FastAPI()
app.include_router(base.base_router)
app.include_router(data.data_router)
