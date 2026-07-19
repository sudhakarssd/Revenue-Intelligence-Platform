from fastapi import APIRouter, Depends, HTTPException, status
from app.ai.contracts import AIRequest, AIResponse
from app.ai.gateway.gateway import AIGateway
from app.api.dependencies import get_gateway
from app.ai.exceptions.exceptions import AIException
from app.shared.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/generate", response_model=AIResponse)
async def generate_response(
    request: AIRequest,
    gateway: AIGateway = Depends(get_gateway)
) -> AIResponse:
    """Processes task-based generation requests using the platform-independent AIRequest contract.

    This maps requested tasks to configured policies, models, and providers.
    """
    try:
        response = await gateway.generate(request)
        return response
    except AIException as e:
        logger.error(f"Platform AI exception: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.exception("Unhandled application exception in generation route")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal application error: {str(e)}"
        )
