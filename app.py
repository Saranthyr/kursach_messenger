from typing import Annotated
from fastapi import FastAPI, Form
from models import async_session

app = FastAPI()

from auth import router as auth_router
app.include_router(auth_router)

from chat import router as chat_router
app.include_router(chat_router)


@app.get('/')
async def root():
    return {'message': 'Hello'}

