from typing import Annotated
from fastapi import APIRouter, Response, Request, Form, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import check_password_hash
from jose import jwt, JWTError
from models import User, session

SECRET_KEY='c23b9de5ecc47c73e103dec1c04743653eea018316415109a454ad8a58ec9b78'

router = APIRouter(
    prefix="/auth"
)


async def query_exec(username: str,
                     session: AsyncSession):
    query = await session.execute(select(User.password, User.id).where(User.username == username))
    return query.first()


@router.post('/login')
async def login(response: Response,
                username: Annotated[str, Form()],
                password: Annotated[str, Form()],
                session: AsyncSession = Depends(session)
                ):
    query = (await session.execute(select(User.password, User.id).where(User.username == username))).first()
    if check_password_hash(query.password, password):
        token = jwt.encode({'user_id': query.id}, SECRET_KEY, 'HS256')
        response.set_cookie('access_token', token)
        return {'message': 'success'}
    else:
        return 403