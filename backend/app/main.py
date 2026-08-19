import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine

from sqlalchemy import text

# Import all SQLAlchemy models to ensure complete metadata registration
from app.models.user import User
from app.models.grade import Grade
from app.models.subject import Subject
from app.models.unit import Unit
from app.models.module import Module
from app.models.learning_content import LearningContent, UserLearningContentProgress
from app.models.quiz import Quiz, Question, QuestionOption
from app.models.quiz_attempt import QuizAttempt, QuestionAttempt
from app.models.unit_assessment import UnitAssessment, AssessmentAttempt
from app.models.student_progress import StudentProgress
from app.models.performance_analysis import PerformanceAnalysis
from app.models.user_profile import UserProfile

# Ensure all tables are created in the database
Base.metadata.create_all(bind=engine)


def _sync_database_schema():
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE questions ADD COLUMN IF NOT EXISTS difficulty VARCHAR(20) DEFAULT 'Medium';"))
            conn.execute(text("ALTER TABLE questions ADD COLUMN IF NOT EXISTS is_approved BOOLEAN DEFAULT TRUE;"))
            conn.execute(text("ALTER TABLE quizzes ADD COLUMN IF NOT EXISTS time_limit_minutes INTEGER DEFAULT 10;"))
            conn.execute(text("ALTER TABLE quiz_attempts ADD COLUMN IF NOT EXISTS time_taken_seconds INTEGER DEFAULT 0;"))
            conn.execute(text("ALTER TABLE performance_analysis ADD COLUMN IF NOT EXISTS module_id INTEGER REFERENCES modules(id);"))
            conn.execute(text("""
                DO $$
                BEGIN
                    IF EXISTS (
                        SELECT 1 FROM pg_constraint WHERE conname = 'performance_analysis_user_id_key'
                    ) THEN
                        ALTER TABLE performance_analysis DROP CONSTRAINT performance_analysis_user_id_key;
                    END IF;
                END $$;
            """))
            conn.commit()
    except Exception as e:
        print(f"Schema sync note: {e}")


_sync_database_schema()

# Import all routers
from app.auth.routes import router as auth_router
from app.grade_routes import router as grade_router
from app.student_routes import router as student_router
from app.subject_routes import router as subject_router
from app.unit_routes import router as unit_router
from app.module_routes import router as module_router
from app.learning_content_routes import router as learning_content_router
from app.quiz_routes import router as quiz_router
from app.unit_assessment_routes import router as unit_assessment_router
from app.progress_routes import router as progress_router
from app.performance_routes import router as performance_router
from app.profile_routes import router as profile_router

app = FastAPI(title="EduBridge AI Tutor")

# Mount uploads static directory for PDF and media access
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Include API routers
app.include_router(auth_router)
app.include_router(grade_router)
app.include_router(student_router)
app.include_router(subject_router)
app.include_router(unit_router)
app.include_router(module_router)
app.include_router(learning_content_router)
app.include_router(quiz_router)
app.include_router(unit_assessment_router)
app.include_router(progress_router)
app.include_router(performance_router)
app.include_router(profile_router)


@app.get("/")
def root():
    return {"message": "EduBridge API is running"}