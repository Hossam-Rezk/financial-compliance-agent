from fastapi import FastAPI
from dotenv import load_dotenv
from src.routes import base, data
from src.routes import nlp
from motor.motor_asyncio import AsyncIOMotorClient
from src.helpers.config import get_settings
from src.stores.vectordb.QdrantProvider import QdrantProvider

load_dotenv(".env")

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongodb_connection = AsyncIOMotorClient(settings.MONGO_DB_URL)
    app.db_client = app.mongodb_connection[settings.MONGO_DATABASE]
    qdrant = QdrantProvider()
    qdrant.init_collection()

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_connection.close()

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)
