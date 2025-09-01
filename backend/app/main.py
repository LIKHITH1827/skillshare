from fastapi import FastAPI
from app.api.V1 import auth, courses, enrollments  # 👈 add enrollments

app = FastAPI(title="SkillShare+ API", version="0.1.0")

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(enrollments.router)

@app.get("/")
def root():
    return {"message": "SkillShare+ Backend Running 🚀"}
