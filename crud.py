from sqlalchemy.orm import Session
import models, schemas
import uuid
from datetime import datetime
from utils import hash_password


def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    db_teacher = models.Teacher(
        id=str(uuid.uuid4()),
        email=teacher.email,
        password=hash_password(teacher.password),
        created_at=datetime.now().isoformat()
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

def create_class(db: Session, cls: schemas.ClassCreate):
    db_class = models.Class(
        id=cls.id,
        teacher_id=cls.teacher_id,
        name=cls.name,
        description=cls.description,
        code=cls.code,
        created_at=datetime.now().isoformat()
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(
        id=student.id,
        class_id=student.class_id,
        code_name=student.code_name,
        created_at=datetime.now().isoformat()
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def upload_assignment(db: Session, assignment: schemas.AssignmentCreate):
    db_assignment = models.Assignment(
        id=assignment.id,
        student_id=assignment.student_id,
        file_path=assignment.file_path,
        uploaded_at=datetime.now().isoformat(),
        status=assignment.status or "Pending"
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment



def evaluate_assignment(db: Session, evaluation: schemas.EvaluationCreate):
    db_evaluation = models.Evaluation(
        id=evaluation.id,
        assignment_id=evaluation.assignment_id,
        teacher_id=evaluation.teacher_id,
        coherence=evaluation.coherence,
        sources=evaluation.sources,
        reasoning=evaluation.reasoning,
        language=evaluation.language,
        total_score=evaluation.total_score,
        feedback=evaluation.feedback,
        ai_suggestion=evaluation.ai_suggestion,
        evaluated_at=datetime.now().isoformat()
    )
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)

    assignment = db.query(models.Assignment).filter(models.Assignment.id == evaluation.assignment_id).first()
    if assignment:
        assignment.status = "Evaluated"
        db.commit()

    return db_evaluation

def get_assignments_by_teacher(db: Session, teacher_id: str):
    return db.query(models.Assignment).join(models.Student).join(models.Class).filter(models.Class.teacher_id == teacher_id).all()

def get_evaluations_by_class(db: Session, class_id: str):
    return db.query(models.Evaluation).join(models.Assignment).join(models.Student).filter(models.Student.class_id == class_id).all()

def create_ai_evaluation(db: Session, evaluation: schemas.EvaluationCreate):
    db_evaluation = models.Evaluation(**evaluation.dict())
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation