from typing import Annotated
from fastapi import FastAPI, Form
from models import async_session

app = FastAPI()

from auth import router as auth_router
app.include_router(auth_router)


@app.get('/')
async def root():
    return {'message': 'Hello'}


@app.post('/create_new_chat')
async def create_new_chat(chat_name: Annotated[str, Form()]):
    return {'message': chat_name}
