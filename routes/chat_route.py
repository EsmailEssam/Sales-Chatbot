from fastapi import APIRouter, Depends, HTTPException
from functools import lru_cache
from src.schemas.routes_schemes.chat_request import ChatRequest
from src.schemas.enums.api_errors_message import ErrorMessage
from src.log_manager.log_manager import get_logger
from main import App

chat_router = APIRouter(
    tags=["api_v1", "chat"]
)

logger = get_logger(__name__)

@lru_cache()
def get_app():
    return App()

@chat_router.post('/chat')
async def chat(request: ChatRequest, app: App = Depends(get_app)):
    logger.info(f"Received chat request | user_query: {request.user_query} | session_id: {request.session_id}")
    
    try:
        events = app.run(request.user_query, request.session_id)
        response = events.get('output_formatter_response', {})
        logger.info(f"Chat response successful | session_id: {request.session_id}")
        return response
    
    
    except ValueError as e:
        logger.error(f"Invalid input error | session_id: {request.session_id} | error: {str(e)}")
        raise HTTPException(status_code=400, detail=ErrorMessage.INVALID_INPUT.value)

    except RuntimeError as e:
        logger.error(f"Model processing error | session_id: {request.session_id} | error: {str(e)}")
        raise HTTPException(status_code=500, detail=ErrorMessage.MODEL_PROCESSING_ERROR.value)

    except Exception as e:
        logger.error(f"Internal error | session_id: {request.session_id} | error: {str(e)}")
        raise HTTPException(status_code=500, detail=ErrorMessage.INTERNAL_ERROR.value)
        