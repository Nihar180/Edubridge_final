from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.database import Base


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id"),
        nullable=False
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    score = Column(Float, nullable=False, default=0.0)
    total_marks = Column(Float, nullable=False, default=0.0)
    percentage = Column(Float, nullable=False, default=0.0)
    passed = Column(Boolean, nullable=False, default=False)
    started_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    completed_at = Column(DateTime, nullable=True)
    time_taken_seconds = Column(Integer, nullable=True, default=0)

    question_attempts = relationship(
        "QuestionAttempt",
        back_populates="attempt",
        cascade="all, delete-orphan"
    )


class QuestionAttempt(Base):
    __tablename__ = "question_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    attempt_id = Column(
        Integer,
        ForeignKey("quiz_attempts.id"),
        nullable=False
    )
    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False
    )
    selected_option_id = Column(
        Integer,
        ForeignKey("question_options.id"),
        nullable=True
    )
    is_correct = Column(Boolean, nullable=False, default=False)
    marks_awarded = Column(Float, nullable=False, default=0.0)

    attempt = relationship("QuizAttempt", back_populates="question_attempts")
