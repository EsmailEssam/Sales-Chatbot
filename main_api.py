from fastapi import FastAPI
from routes.base_router import base_router 
from routes.chat_route import chat_router
from src.utils.metrics import setup_metrics


app = FastAPI()
setup_metrics(app)

app.include_router(base_router  )
app.include_router(chat_router )




