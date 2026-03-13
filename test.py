from library.database import engine, Base, SessionLocal
from library.services import create_author, create_student, create_book, borrow_book

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    auth = create_author(db, "Abdulla Qodiriy")
    stu = create_student(db, "Ali Valiyev", "ali2@gmail.com")
    bk = create_book(db, "O'tkan kunlar", auth.id, 1922)
    br = borrow_book(db, stu.id, bk.id)
    if br:
        print(f"Muvaffaqiyatli: {stu.full_name} kitobni oldi.")
finally:
    db.close()