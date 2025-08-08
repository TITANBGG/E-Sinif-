from sqlalchemy import Column, String, Text, Integer, ForeignKey
from database import Base
import datetime

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(String, default=datetime.datetime.now().isoformat)

class Class(Base):
    __tablename__ = "classes"
    id = Column(String, primary_key=True)
    teacher_id = Column(String, ForeignKey("teachers.id"))
    name = Column(String)
    description = Column(Text)
    code = Column(String, unique=True)
    created_at = Column(String)

class Student(Base):
    __tablename__ = "students"
    id = Column(String, primary_key=True)
    class_id = Column(String, ForeignKey("classes.id"))
    code_name = Column(String, unique=True)
    created_at = Column(String)

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey("students.id"))
    file_path = Column(String)
    uploaded_at = Column(String)
    status = Column(String, default="Pending")

class Evaluation(Base):
    __tablename__ = "evaluations"
    id = Column(String, primary_key=True)
    assignment_id = Column(String, ForeignKey("assignments.id"))
    teacher_id = Column(String, ForeignKey("teachers.id"))
    coherence = Column(Integer)
    sources = Column(Integer)
    reasoning = Column(Integer)
    language = Column(Integer)
    total_score = Column(Integer)
    feedback = Column(Text)
    ai_suggestion = Column(Text)
    evaluated_at = Column(String)

