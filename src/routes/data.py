from fastapi import APIRouter, Depends, UploadFile, File, status, Request
from fastapi.responses import JSONResponse
import os
from src.models.enums.ResponsEnums import ResponseStatus
from src.helpers.config import get_settings, Settings
from src.controllers.DataController import DataController
from src.controllers.ProcessController import ProcessController
import aiofiles
import logging
from src.routes.schemes import ProcessRequest
from src.models.ProjectModel import ProjectModel

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)


@data_router.post("/upload/{project_id}")
async def upload_data(
    Request: Request,
    project_id: str,
    file: UploadFile = File(...),
    app_settings: Settings = Depends(get_settings)
):
    project_model = ProjectModel(database_client=Request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)
    data_controller = DataController()
    is_valid, message = data_controller.ValidateFile(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseStatus.ERROR.value, "message": message}
        )

    file_location = data_controller.generate_unique_file(
        orig_filename=file.filename,
        project_id=project_id
    )
    file_name = os.path.basename(file_location)

    try:
        async with aiofiles.open(file_location, 'wb') as out_file:
            # Bug 2 fix: use FILE_UPLOAD_CHUNK_SIZE for streaming, not text chunk size
            while chunk := await file.read(app_settings.FILE_UPLOAD_CHUNK_SIZE):
                await out_file.write(chunk)
    except Exception as e:
        logger.error(f"Error occurred while uploading file: {e}")
        if os.path.exists(file_location):
            os.remove(file_location)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"signal": ResponseStatus.ERROR.value}
        )

    return JSONResponse(content={
        "signal": ResponseStatus.SUCCESS.value,
        "file_name": file_name,   
        "project_id": str(project.id)
    })


@data_router.post("/process/{project_id}")
async def process_endpoint(
    project_id: str,
    request: ProcessRequest,
    app_settings: Settings = Depends(get_settings)
):
    file_name = request.file_name
    chunk_size = request.chunk_size or app_settings.FILE_DEFAULT_CHUNK_SIZE
    overlap_size = request.overlap_size or app_settings.FILE_DEFAULT_OVERLAP_SIZE

    process_controller = ProcessController(project_id=project_id)

    file_content = process_controller.get_file_content(file_name=file_name)
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    if not file_chunks:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseStatus.processing_failed.value,
                "message": "No content to process."
            }
        )

    return JSONResponse(content={
        "signal": ResponseStatus.SUCCESS.value,
        "file_chunks": len(file_chunks)
    })
