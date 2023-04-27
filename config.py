import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

load_dotenv()

DATABASE_URI = f"postgresql+asyncpg://{os.environ['DB_USER']}:" \
               f"{os.environ['DB_PASSWORD']}@localhost:5432/{os.environ['DB_NAME']}"
