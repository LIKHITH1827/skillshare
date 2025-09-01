from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.models.user import User
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate, EnrollmentOut
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

# ----------------------------------------
# Learner: Enroll in a course
# ----------------------------------------
@router.post("/", response_model=EnrollmentOut, status_code=201)
async def enroll_in_course(
    payload: EnrollmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # only learners enroll (keeps demo simple)
    require_role(current_user, ["learner"])

    # course must exist
    course_res = await db.execute(select(Course).where(Course.id == payload.course_id))
    course = course_res.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    enrollment = Enrollment(user_id=current_user.id, course_id=payload.course_id)
    db.add(enrollment)
    try:
        await db.commit()
        await db.refresh(enrollment)
    except IntegrityError:
        await db.rollback()
        # UniqueConstraint on (user_id, course_id) prevents duplicates
        raise HTTPException(status_code=400, detail="Already enrolled in this course")

    return enrollment


# ----------------------------------------
# Learner: List my enrollments
# ----------------------------------------
@router.get("/me", response_model=list[EnrollmentOut])
async def list_my_enrollments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    res = await db.execute(select(Enrollment).where(Enrollment.user_id == current_user.id))
    return res.scalars().all()


# ----------------------------------------
# Learner: Unenroll from a course
# ----------------------------------------
@router.delete("/{course_id}", status_code=200)
async def unenroll(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_role(current_user, ["learner"])

    res = await db.execute(
        select(Enrollment).where(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id,
        )
    )
    enrollment = res.scalars().first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    await db.delete(enrollment)
    await db.commit()
    return {"message": f"Unenrolled from course {course_id}"}


# ----------------------------------------
# Admin/Instructor: List enrollments for a course
#  - Admin: any course
#  - Instructor: only their own course
# ----------------------------------------
@router.get("/course/{course_id}", response_model=list[EnrollmentOut])
async def list_enrollments_for_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # load the course
    c_res = await db.execute(select(Course).where(Course.id == course_id))
    course = c_res.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # permission check
    if current_user.role == "instructor":
        if course.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized for this course")
    elif current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    res = await db.execute(select(Enrollment).where(Enrollment.course_id == course_id))
    return res.scalars().all()
