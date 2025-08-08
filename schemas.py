from pydantic import BaseModel
from typing import Optional

class TeacherBase(BaseModel):
    email: str
    password: str

class TeacherCreate(TeacherBase):
    id: str

class TeacherOut(BaseModel):
    id: str
    email: str
    created_at: Optional[str]

    class Config:
        orm_mode = True

class ClassBase(BaseModel):
    name: str
    description: Optional[str]
    code: str

class ClassCreate(ClassBase):
    id: str
    teacher_id: str

class ClassOut(BaseModel):
    id: str
    name: str
    description: Optional[str]
    code: str
    teacher_id: str
    created_at: Optional[str]

    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    code_name: str

class StudentCreate(StudentBase):
    id: str
    class_id: str

class StudentOut(BaseModel):
    id: str
    class_id: str
    code_name: str
    created_at: Optional[str]

    class Config:
        orm_mode = True

class AssignmentBase(BaseModel):
    file_path: str
    status: Optional[str] = "Pending"

class AssignmentCreate(AssignmentBase):
    id: str
    student_id: str

class AssignmentOut(BaseModel):
    id: str
    student_id: str
    file_path: str
    uploaded_at: Optional[str]
    status: str

    class Config:
        orm_mode = True

class EvaluationBase(BaseModel):
    coherence: int
    sources: int
    reasoning: int
    language: int
    feedback: Optional[str]
    total_score: float

class EvaluationCreate(EvaluationBase):
    assignment_id: int

class EvaluationOut(EvaluationBase):
    id: int
    assignment_id: int

    class Config:
        orm_mode = True
