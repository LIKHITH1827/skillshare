from pydantic import BaseModel

class CourseCreate(BaseModel):
    title: str
    description: str
    category: str = "General"

class CourseOut(BaseModel):
    id: int
    title: str
    description: str
    category: str
    created_by: int

    class Config:
        from_attributes = True
