from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine
from fastapi import FastAPI, Form

engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/test")

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello'}


@app.post('/create_new_chat')
async def create_new_chat(chat_name: Annotated[str, Form()]):
    return {'message': chat_name}
