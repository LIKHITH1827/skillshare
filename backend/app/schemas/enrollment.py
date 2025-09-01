from pydantic import BaseModel

class EnrollmentCreate(BaseModel):
    course_id: int

class EnrollmentOut(BaseModel):
    id: int
    user_id: int
    course_id: int

    class Config:
        from_attributes = True
