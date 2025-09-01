from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, String
from app.db.base_class import Base

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50), default="General")
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # relationships
    creator = relationship("User", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
