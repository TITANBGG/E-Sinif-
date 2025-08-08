from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from database import SessionLocal, engine
from models import Base
import models, crud, schemas
from utils import verify_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
evaluations = relationship("Evaluation", back_populates="assignment")


@app.post("/teacher/login")
def login_teacher(login_data: schemas.TeacherBase, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.email == login_data.email).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

    if not verify_password(login_data.password, teacher.password):
        raise HTTPException(status_code=401, detail="Şifre yanlış")

    return {"message": "Giriş başarılı", "teacher_id": teacher.id}
@app.post("/student/login")
def login_student(class_code: str, db: Session = Depends(get_db)):
    class_obj = db.query(models.Class).filter(models.Class.code == class_code).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Sınıf kodu bulunamadı")

    import uuid
    new_student = models.Student(
        id=str(uuid.uuid4()),
        class_id=class_obj.id,
        code_name=str(uuid.uuid4())[:8],
        created_at=datetime.now().isoformat()
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {
        "message": "Öğrenci giriş başarılı",
        "student_id": new_student.id,
        "code_name": new_student.code_name
    }

@app.post("/teacher", response_model=schemas.TeacherOut)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return crud.create_teacher(db, teacher)

@app.post("/class", response_model=schemas.ClassOut)
def create_class(cls: schemas.ClassCreate, db: Session = Depends(get_db)):
    return crud.create_class(db, cls)

@app.post("/student", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)

@app.post("/assignment", response_model=schemas.AssignmentOut)
def upload_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    return crud.upload_assignment(db, assignment)

@app.post("/evaluation", response_model=schemas.EvaluationOut)
def evaluate_assignment(evaluation: schemas.EvaluationCreate, db: Session = Depends(get_db)):
    return crud.evaluate_assignment(db, evaluation)

@app.get("/teacher/{teacher_id}/assignments", response_model=list[schemas.AssignmentOut])
def get_teacher_assignments(teacher_id: str, db: Session = Depends(get_db)):
    return crud.get_assignments_by_teacher(db, teacher_id)

@app.get("/report/class/{class_id}", response_model=list[schemas.EvaluationOut])
def get_evaluation_report(class_id: str, db: Session = Depends(get_db)):
    return crud.get_evaluations_by_class(db, class_id)
from fastapi import File, UploadFile
from auto_evaluate import extract_text_from_pdf, evaluate_homework_with_gemini

@app.post("/auto-evaluate")
def auto_evaluate(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file)
    result = evaluate_homework_with_gemini(text)
    return result

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")  # 👈 burada açıkça dosya adı belirtildi

print("API KEY:", os.getenv("GEMINI_API_KEY"))


class Evaluation(Base):
    _tablename_ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    coherence = Column(Integer)
    sources = Column(Integer)
    reasoning = Column(Integer)
    language = Column(Integer)
    feedback = Column(String)
    total_score = Column(Float)

    assignment = relationship("Assignment", back_populates="evaluations")