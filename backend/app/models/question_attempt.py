from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


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

    is_correct = Column(
        Boolean,
        nullable=False
    )

    time_taken = Column(
        Integer,
        nullable=True
    )

    attempt = relationship("QuizAttempt", back_populates="question_attempts")