from fastapi import FastAPI , APIRouter , Depends
import os
from main import App
from src.graph import get_graph

chat_router = APIRouter(
    tags= ['api_v1' , 'chat']
)



@chat_router.get('/chat')
async def chat(user_query: str , session_id: str = None):
    
        app = App()
        
        events = app.run(user_query ,session_id )
        
    
        return events['output_formatter_response']
    
    