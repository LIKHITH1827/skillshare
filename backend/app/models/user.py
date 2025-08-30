from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum
from app.db.base import Base
import enum

# Define user roles
class Role(str, enum.Enum):
    admin = "admin"
    instructor = "instructor"
    learner = "learner"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str]
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.learner)

    # relationships
    courses = relationship("Course", back_populates="creator")
    enrollments = relationship("Enrollment", back_populates="user")
