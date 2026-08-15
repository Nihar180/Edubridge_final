from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User
from app.models.grade import Grade
from app.auth.routes import router as auth_router
from app.grade_routes import router as grade_router
from app.student_routes import router as student_router
from app.models.subject import Subject
from app.subject_routes import router as subject_router
from app.models.unit import Unit
from app.unit_routes import router as unit_router
from app.models.module import Module
from app.module_routes import router as module_router
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EduBridge AI Tutor")

app.include_router(auth_router)
app.include_router(grade_router)
app.include_router(student_router)
app.include_router(subject_router)
app.include_router(unit_router)
app.include_router(module_router)

@app.get("/")
def root():
    return {"message": "EduBridge API is running"}