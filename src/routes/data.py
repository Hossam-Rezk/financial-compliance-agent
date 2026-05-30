from fastapi import FastAPI, APIRouter, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse
import os
from src.models.enums.ResponsEnums import ResponseStatus
from src.helpers.config import get_settings, Settings
from src.controllers.BaseController import BaseController
from src.controllers.DataController import DataController
from src.controllers.ProjectController import ProjectController
from src.controllers.ProcessController import ProcessController 
import aiofiles
import logging
import re
from src.routes.schemes import ProcessRequest
from langchain.text_splitter import RecursiveCharacterTextSplitter
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
    file_name = os.path.basename(file_location)
    file_id = file_name.split("_")[0]  # the random key e.g. "S6IY2bOd"

    try:
        async with aiofiles.open(file_location, 'wb') as out_file:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)
    except Exception as e:
        logger.error(f"Error occurred while uploading file: {e}")
        if os.path.exists(file_location):
            os.remove(file_location)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"signal": ResponseStatus.ERROR.value})

    return JSONResponse(content={
        "signal": ResponseStatus.SUCCESS.value,
        "file_name": file_name,
        "file_id": file_id   # ← returned to user
    })

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, request: ProcessRequest, app_settings: Settings = Depends(get_settings)):
    file_id = request.file_id          # ← ProcessRequest → request
    chunk_size = request.chunk_size or app_settings.FILE_DEFAULT_CHUNK_SIZE      # ← same
    overlap_size = request.overlap_size or app_settings.FILE_DEFAULT_OVERLAP_SIZE  # ← same

    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id)
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseStatus.processing_failed.value, "message": "No content to process."}
        )

    return JSONResponse(content={"signal": ResponseStatus.SUCCESS.value, "file_chunks": len(file_chunks)})