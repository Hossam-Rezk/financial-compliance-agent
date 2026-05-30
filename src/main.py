from fastapi import FastAPI
from dotenv import load_dotenv
from src.routes import base
from src.routes import data
from motor.motor_asyncio import AsyncIOMotorClient
from helper.config import Settings, get_settings


load_dotenv(".env")

from src.routes import base

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongodb_connection = AsyncIOMotorClient(settings.MONGO_DB_URL)
    app.db_client = app.mongodb_connection[settings.MONGO_DATABASE]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_connection.close()  

app.include_router(base.base_router)
app.include_router(data.data_router)
