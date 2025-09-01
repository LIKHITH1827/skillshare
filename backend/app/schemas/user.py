from pydantic import BaseModel, EmailStr
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    instructor = "instructor"
    learner = "learner"

# Schema for user creation (input)
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role = Role.learner  # default role

# Schema for returning user (output)
class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: Role

    class Config:
        from_attributes = True  # allows mapping from ORM model

# For login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# For JWT response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
