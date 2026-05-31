from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import logging
from src.routes.schemes.nlp import QueryRequest, AnalyzeRequest
from src.controllers.NLPController import NLPController
from src.models.enums.ResponsEnums import ResponseStatus

logger = logging.getLogger("uvicorn.error")

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1", "nlp"],
)


@nlp_router.post("/query/{project_id}")
async def query_endpoint(project_id: str, request: QueryRequest):
    nlp_controller = NLPController()

    try:
        results = await nlp_controller.search(
            query=request.query,
            project_id=project_id,
            top_k=request.top_k,
        )
    except Exception as e:
        logger.error(f"NLP query failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"signal": ResponseStatus.ERROR.value, "message": str(e)},
        )

    return JSONResponse(content={
        "signal": ResponseStatus.SUCCESS.value,
        "results": results,
    })


@nlp_router.post("/analyze/{project_id}")
async def analyze_endpoint(project_id: str, request: AnalyzeRequest):
    nlp_controller = NLPController()

    try:
        report = await nlp_controller.analyze(
            query=request.query,
            project_id=project_id,
            top_k=request.top_k,
        )
    except Exception as e:
        logger.error(f"Compliance analysis failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "signal": ResponseStatus.ERROR.value,
                "message": str(e),
            },
        )

    return JSONResponse(content={
        "signal": ResponseStatus.SUCCESS.value,
        "report": report,
    })
