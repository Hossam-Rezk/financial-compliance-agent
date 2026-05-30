from fastapi import FastAPI, APIRouter, Depends
import os

from src.helpers.config import get_settings, Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["base"]

)
@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):
    settings = get_settings()
    return {"message": f"Welcome to {settings.APP_NAME} version {settings.APP_VERSION}!"}