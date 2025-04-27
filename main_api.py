from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
from routes.base_router import base_router



app = FastAPI()


app.include_router(base_router)
