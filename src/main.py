from fastapi import FastAPI
from dotenv import load_dotenv
from src.routes import base, data
from src.routes import nlp
from motor.motor_asyncio import AsyncIOMotorClient
from src.helpers.config import get_settings
from src.stores.vectordb.QdrantProvider import QdrantProvider
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

load_dotenv(".env")

limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.mongodb_connection = AsyncIOMotorClient(settings.MONGO_DB_URL)
    app.db_client = app.mongodb_connection[settings.MONGO_DATABASE]
    qdrant = QdrantProvider()
    qdrant.init_collection()
    yield
    app.mongodb_connection.close()

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)
