from fastapi import FastAPI, APIRouter, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse
import os
from src.models.enums.ResponsEnums import ResponseStatus
from src.helpers.config import get_settings, Settings
from src.controllers.BaseController import BaseController
from src.controllers.DataController import DataController
from src.controllers.ProjectController import ProjectController
import aiofiles
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, app_settings: Settings = Depends(get_settings), file: UploadFile = File(...)):
    data_controller = DataController()
    is_valid, message = data_controller.ValidateFile(file=file)
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"signal": "error", "message": message})

    file_location = data_controller.generate_unique_file(orig_filename=file.filename, project_id=project_id)

    try:
        async with aiofiles.open(file_location, 'wb') as out_file:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):  
                await out_file.write(chunk)
    except Exception as e:
        logger.error(f"Error occurred while uploading file: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"signal": ResponseStatus.ERROR.value})

        return JSONResponse(content={"signal": ResponseStatus.SUCCESS.value})  # ← moved outside except

    return JSONResponse(
        content={
        "signal": ResponseStatus.SUCCESS.value,
        "file_name": os.path.basename(file_location),
    })