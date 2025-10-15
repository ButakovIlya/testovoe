from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Integer, MetaData, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from infrastructure.enum import RoleEnum


class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}
    metadata = MetaData()

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, index=True, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    registration_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    role: Mapped[RoleEnum] = mapped_column(
        Enum(RoleEnum, name="role", native_enum=False),
        nullable=False,
        default=RoleEnum.USER,
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post", back_populates="author", cascade="all, delete-orphan", lazy="selectin"
    )


class Category(Base):
    __tablename__ = "post_categories"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    posts: Mapped[list["Post"]] = relationship(
        "Post", back_populates="category", cascade="all, delete-orphan", lazy="selectin"
    )


class Post(Base):
    __tablename__ = "posts"

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(
        ForeignKey("post_categories.id", ondelete="CASCADE")
    )

    title: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    body: Mapped[str] = mapped_column(Text, default=None, server_default=None)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, server_default="now()"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, server_default="now()"
    )

    author: Mapped["User"] = relationship("User", back_populates="posts", lazy="joined")
    category: Mapped["Category"] = relationship(
        "Category", back_populates="posts", lazy="joined"
    )
