import datetime
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, BOOLEAN, DATE, TIMESTAMP, JSON, ARRAY, BYTEA
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import text, ForeignKey
from config import DATABASE_URI

engine = create_async_engine(DATABASE_URI)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def session() -> AsyncSession:
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(VARCHAR(64), primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(32), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(128), nullable=False)
    is_online: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, server_default=text('False'))


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[str] = mapped_column(VARCHAR(64), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(128), nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("chat_types.id", onupdate="CASCADE", ondelete="RESTRICT"))


class ChatTypes(Base):
    __tablename__ = "chat_types"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(32), unique=True, nullable=False)


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(32), unique=True, nullable=False)


class File(Base):
    __tablename__ = "files"

    id: Mapped[str] = mapped_column(VARCHAR(64), primary_key=True)
    filename: Mapped[str] = mapped_column(VARCHAR(512), nullable=False)
    extension: Mapped[str] = mapped_column(VARCHAR(16), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False,
                                                          server_default=text("CURRENT_TIMESTAMP"))
    file: Mapped[bytearray] = mapped_column(BYTEA, nullable=False)


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(VARCHAR(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE"),
                                         nullable=True)
    chat_id: Mapped[str] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE", onupdate="CASCADE"),
                                         nullable=False)
    message_params: Mapped[dict] = mapped_column(JSON, nullable=False)


class ChatMember(Base):
    __tablename__ = "chat_members"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
                                         nullable=False, primary_key=True)
    chat_id: Mapped[str] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE", onupdate="CASCADE"),
                                         nullable=False, primary_key=True)
    permissions: Mapped[list] = mapped_column(ARRAY(INTEGER))


class UserFile(Base):
    __tablename__ = "user_files"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
                                         nullable=False, primary_key=True)
    file_id: Mapped[str] = mapped_column(ForeignKey("files.id", ondelete="CASCADE", onupdate="CASCADE"),
                                         nullable=False, primary_key=True)
    current_avatar: Mapped[bool] = mapped_column(BOOLEAN, nullable=True)


