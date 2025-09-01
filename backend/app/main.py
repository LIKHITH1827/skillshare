from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.V1 import auth, courses, enrollments  

app = FastAPI(title="SkillShare+ API", version="0.1.0")

# Allow frontend origin
origins = [
    "http://localhost:5173",  # Vite dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers AFTER middleware
app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(enrollments.router)

@app.get("/")
def root():
    return {"message": "SkillShare+ Backend Running 🚀"}
