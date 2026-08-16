from sqlalchemy import Column, Integer, ForeignKey, DateTime

from app.database import Base


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    assessment_id = Column(
        Integer,
        ForeignKey("unit_assessments.id"),
        nullable=False
    )

    score = Column(
        Integer,
        nullable=True
    )

    total_questions = Column(
        Integer,
        nullable=False
    )

    started_at = Column(
        DateTime,
        nullable=True
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )