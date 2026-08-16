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
from app.models.learning_content import LearningContent
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.quiz_attempt import QuizAttempt
from app.models.question_attempt import QuestionAttempt
from app.models.unit_assessment import UnitAssessment
from app.models.assessment_attempt import AssessmentAttempt
from app.models.student_progress import StudentProgress
from app.models.flashcard import Flashcard
from app.models.student_flashcard import StudentFlashcard
from app.models.ai_conversation import AIConversation
from app.models.ai_message import AIMessage
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