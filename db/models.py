from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String())
    password: Mapped[str] = mapped_column(String())
    role: Mapped[str] = mapped_column(String())


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())
    content: Mapped[str] = mapped_column(String())


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    postId: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(String())
    creatorId: Mapped[int] = mapped_column(Integer)