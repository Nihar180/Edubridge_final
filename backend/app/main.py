from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User
from app.models.grade import Grade
from app.auth.routes import router as auth_router
from app.grade_routes import router as grade_router
from app.student_routes import router as student_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EduBridge AI Tutor")

app.include_router(auth_router)
app.include_router(grade_router)
app.include_router(student_router)

@app.get("/")
def root():
    return {"message": "EduBridge API is running"}