import datetime
import uuid
from typing import Annotated
from fastapi import APIRouter, Response, Request, Form, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import check_password_hash,generate_password_hash
from jose import jwt, JWTError
from models import User, session

SECRET_KEY = 'c23b9de5ecc47c73e103dec1c04743653eea018316415109a454ad8a58ec9b78'
ALGORITHM = 'HS256'
ACCESS_TOKEN_SAVE = 30
ACCESS_TOKEN_DEFAULT = 1

router = APIRouter(
    prefix="/auth"
)


@router.post('/login')
async def login(response: Response,
                username: Annotated[str, Form()],
                password: Annotated[str, Form()],
                save_login: Annotated[bool, Form()] = False,
                session: AsyncSession = Depends(session)
                ):
    query = (await session.execute(select(User.password, User.id).where(User.username == username))).first()
    if query is not None and check_password_hash(query.password, password):
        (await session.execute(select(User).where(User.id == query.id))).scalars().first().is_online = True
        await session.commit()
        jwt_data = {'user_id': str(query.id)}
        if save_login is True:
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=ACCESS_TOKEN_SAVE)
        else:
            expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_DEFAULT)
        jwt_data['exp'] = expires
        token = jwt.encode(jwt_data, SECRET_KEY, algorithm=ALGORITHM)
        response.set_cookie('access_token', token)
        response.status_code = 200
    else:
        raise HTTPException(status_code=418)


@router.post('/logout')
async def logout(response: Response,
                 request: Request,
                 session: AsyncSession = Depends(session)):
    token = request.cookies.get('access_token')
    token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    (await session.execute(select(User).where(User.id == token['user_id']))).scalars().first().is_online = False
    await session.commit()
    response.delete_cookie('access_token')


@router.post('/register')
async def register(response: Response,
                   request: Request,
                   username: Annotated[str, Form()],
                   password: Annotated[str, Form()],
                   session: AsyncSession = Depends(session)):
    if len(username) < 6:
        response.status_code = 440
    elif len(password) < 8:
        response.status_code = 450
    elif (await session.execute(select(User).where(User.username == username))).one_or_none() is not None:
        response.status_code = 409
    else:
        user = User(
            id=uuid.uuid4(),
            username=username,
            password=generate_password_hash(password)
        )
        session.add(user)
        await session.commit()
        response.status_code = 200
