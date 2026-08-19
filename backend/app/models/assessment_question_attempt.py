from sqlalchemy import Boolean, Column, ForeignKey, Integer

from app.database import Base


class AssessmentQuestionAttempt(Base):
    __tablename__ = "assessment_question_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    attempt_id = Column(
        Integer,
        ForeignKey("assessment_attempts.id"),
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
    is_correct = Column(Boolean, nullable=False)
    time_taken = Column(Integer, nullable=True)
