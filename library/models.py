from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import String, Text, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from library.database import Base

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    books: Mapped[List["Book"]] = relationship(back_populates="author")

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    published_year: Mapped[int] = mapped_column()
    isbn: Mapped[Optional[str]] = mapped_column(String(13), unique=True)
    is_available: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    author: Mapped["Author"] = relationship(back_populates="books")
    borrows: Mapped[List["Borrow"]] = relationship(back_populates="book")

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    grade: Mapped[Optional[str]] = mapped_column(String(20))
    registered_at: Mapped[datetime] = mapped_column(server_default=func.now())
    borrows: Mapped[List["Borrow"]] = relationship(back_populates="student")

class Borrow(Base):
    __tablename__ = "borrows"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    borrowed_at: Mapped[datetime] = mapped_column(server_default=func.now())
    due_date: Mapped[datetime] = mapped_column(default=lambda: datetime.now() + timedelta(days=14))
    returned_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    student: Mapped["Student"] = relationship(back_populates="borrows")
    book: Mapped["Book"] = relationship(back_populates="borrows")