from fastapi import FastAPI, APIRouter, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse
import os
from src.helpers.config import get_settings, Settings
from src.controllers.BaseController import BaseController
from src.controllers.DataController import DataController
from src.controllers import ProjectController
import aiofiles
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, app_settings: Settings = Depends(get_settings), file: UploadFile = File(...)):
        is_valid, message = DataController().ValidateFile(file=file)
        if not is_valid:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status": "error", "message": message})
        # Save the file to a temporary location

        project_dir = ProjectController().get_project_dir(project_id=project_id)
        file_location = os.path.join(project_dir, file.filename)
        async with aiofiles.open(file_location, 'wb') as out_file:
            while chunk := await file.read(app_settings.FiLE_DEFAULT_CHUNCK_SIZE):
                await out_file.write(chunk)