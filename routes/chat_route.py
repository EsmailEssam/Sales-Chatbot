from fastapi import FastAPI , APIRouter , Depends , HTTPException
from main import App
from functools import lru_cache
from src.schemas.enums.api_errors_message import ErrorMessage
from src.log_manager.log_manager import get_logger

chat_router = APIRouter(
    tags= ['api_v1' , 'chat']
)

logger = get_logger(__name__)

@lru_cache()  # to make the App class Singleton (called once in the run time)
def get_app():
    return App()

@chat_router.get('/chat')
async def chat(user_query: str , session_id: str = None, app: App = Depends(get_app)):
    logger.info(f"Received chat request | user_query: {user_query} | session_id: {session_id}")
    try:
        events = app.run(user_query, session_id)
        response = events.get('output_formatter_response', {})
        logger.info(f"Chat response successful | session_id: {session_id}")
        return response
    
    
    except ValueError as e:
        logger.warning(f"Invalid input error | user_query: {user_query} | session_id: {session_id} | error details: {str(e)}")
        raise HTTPException(status_code=400, detail=ErrorMessage.INVALID_INPUT)
    except RuntimeError as e:
        logger.error(f"Model processing error | user_query: {user_query} | session_id: {session_id} | error details: {str(e)}")
        raise HTTPException(status_code=500, detail=ErrorMessage.MODEL_PROCESSING_ERROR)
    except Exception as e:
        logger.exception(f"Internal error | user_query: {user_query} | session_id: {session_id} | error details: {str(e)}")
        raise HTTPException(status_code=500, detail=ErrorMessage.INTERNAL_ERROR)
        