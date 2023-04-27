import datetime
import uuid
from typing import Annotated
from fastapi import APIRouter, Response, Request, Form, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import check_password_hash,generate_password_hash
from jose import jwt, JWTError
from models import Chat, session
from security import token_required


router = APIRouter(
    prefix="/chat",
    dependencies=[Depends(token_required)]
)


@router.post('/create')
async def create_new_chat(response: Response,
                          chat_name: Annotated[str, Form()],
                          type_id: Annotated[int, Form()],
                          session: AsyncSession = Depends(session)
                          ):
    chat=Chat(
        id=uuid.uuid4(),
        name=chat_name,
        type_id=type_id
    )
    session.add(chat)
    await session.commit()