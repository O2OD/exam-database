from sqlalchemy.orm import Session
from sqlalchemy import select, func
from library.models import Author, Book, Student, Borrow
from datetime import datetime, timedelta


def create_author(db: Session, name: str, bio: str = None) -> Author:
    author = Author(name=name, bio=bio)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

def get_author_by_id(db: Session, author_id: int) -> Author | None:
    return db.get(Author, author_id)

def get_all_authors(db: Session) -> list[Author]:
    return db.execute(select(Author)).scalars().all()

def update_author(db: Session, author_id: int, name: str = None, bio: str = None) -> Author | None:
    author = db.get(Author, author_id)
    if author:
        if name: author.name = name
        if bio: author.bio = bio
        db.commit()
        db.refresh(author)
    return author

def delete_author(db: Session, author_id: int) -> bool:
    author = db.get(Author, author_id)
    if author and not author.books:
        db.delete(author)
        db.commit()
        return True
    return False


def create_book(db: Session, title: str, author_id: int, published_year: int, isbn: str = None) -> Book:
    book = Book(title=title, author_id=author_id, published_year=published_year, isbn=isbn)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get_book_by_id(db: Session, book_id: int) -> Book | None:
    return db.get(Book, book_id)

def get_all_books(db: Session) -> list[Book]:
    return db.execute(select(Book)).scalars().all()

def search_books_by_title(db: Session, title: str) -> list[Book]:
    return db.execute(select(Book).where(Book.title.contains(title))).scalars().all()

def delete_book(db: Session, book_id: int) -> bool:
    book = db.get(Book, book_id)
    if book:
        db.delete(book)
        db.commit()
        return True
    return False


def create_student(db: Session, full_name: str, email: str, grade: str = None) -> Student:
    student = Student(full_name=full_name, email=email, grade=grade)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def get_student_by_id(db: Session, student_id: int) -> Student | None:
    return db.get(Student, student_id)

def get_all_students(db: Session) -> list[Student]:
    return db.execute(select(Student)).scalars().all()

def update_student_grade(db: Session, student_id: int, grade: str) -> Student | None:
    student = db.get(Student, student_id)
    if student:
        student.grade = grade
        db.commit()
        db.refresh(student)
    return student

def borrow_book(db: Session, student_id: int, book_id: int) -> Borrow | None:
    student = db.get(Student, student_id)
    book = db.get(Book, book_id)
    if not student or not book or not book.is_available:
        return None
    active_borrows = db.execute(select(func.count(Borrow.id)).where(Borrow.student_id == student_id, Borrow.returned_at == None)).scalar()
    if active_borrows >= 3:
        return None
    new_borrow = Borrow(student_id=student_id, book_id=book_id)
    book.is_available = False
    db.add(new_borrow)
    db.commit()
    db.refresh(new_borrow)
    return new_borrow

def return_book(db: Session, borrow_id: int) -> bool:
    borrow = db.get(Borrow, borrow_id)
    if not borrow or borrow.returned_at:
        return False
    borrow.returned_at = datetime.now()
    borrow.book.is_available = True
    db.commit()
    return True


def get_student_borrow_count(db: Session, student_id: int) -> int:
    return db.execute(select(func.count(Borrow.id)).where(Borrow.student_id == student_id)).scalar()

def get_currently_borrowed_books(db: Session):
    return db.execute(select(Book, Student, Borrow.borrowed_at).join(Borrow, Book.id == Borrow.book_id).join(Student, Borrow.student_id == Student.id).where(Borrow.returned_at == None)).all()

def get_books_by_author(db: Session, author_id: int) -> list[Book]:
    return db.execute(select(Book).where(Book.author_id == author_id)).scalars().all()

def get_overdue_borrows(db: Session):
    today = datetime.now()
    results = db.execute(select(Borrow, Student, Book).join(Student).join(Book).where(Borrow.returned_at == None, Borrow.due_date < today)).all()
    return [(b, s, bk, (today - b.due_date).days) for b, s, bk in results]