import datetime
import uuid
from typing import Annotated
from functools import wraps
from fastapi import APIRouter, Response, Request, Form, Depends, Cookie, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import check_password_hash,generate_password_hash
from jose import jwt, JWTError, ExpiredSignatureError
from models import Chat, session
from auth import ALGORITHM, SECRET_KEY


async def token_required(access_token: Annotated[str, Cookie()]):
    if access_token is None:
        raise HTTPException(status_code=403)
    else:
        try:
            jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
        except ExpiredSignatureError:
            raise HTTPException(status_code=403)


