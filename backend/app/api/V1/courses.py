from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.course import Course
from app.models.user import User
from app.schemas.course import CourseCreate, CourseOut
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/courses", tags=["Courses"])


# ✅ Create a course (Admin/Instructor only)
@router.post("/", response_model=CourseOut)
async def create_course(
    course_in: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_role(current_user, ["admin", "instructor"])

    new_course = Course(
        title=course_in.title,
        description=course_in.description,
        category=course_in.category,
        created_by=current_user.id,
    )
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


# ✅ Get all courses (open to any logged-in user)
@router.get("/", response_model=list[CourseOut])
async def list_courses(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Course))
    courses = result.scalars().all()
    return courses


# ✅ Get one course by ID
@router.get("/{course_id}", response_model=CourseOut)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


# ✅ Update course (Admin/Instructor only, must own it if instructor)
@router.put("/{course_id}", response_model=CourseOut)
async def update_course(
    course_id: int,
    course_in: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Instructors can only update their own courses
    if current_user.role == "instructor" and course.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this course")

    course.title = course_in.title
    course.description = course_in.description
    course.category = course_in.category

    await db.commit()
    await db.refresh(course)
    return course


# ✅ Delete course (Admin only)
@router.delete("/{course_id}")
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_role(current_user, ["admin"])

    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    await db.delete(course)
    await db.commit()
    return {"message": f"Course {course_id} deleted"}
