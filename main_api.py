from fastapi import FastAPI
from routes.base_router import base_router 
from routes.chat_route import chat_router



app = FastAPI()

app.include_router(base_router  )
app.include_router(chat_router )




