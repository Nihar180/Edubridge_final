from sqlalchemy import Column, ForeignKey, Integer

from app.database import Base


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    assessment_id = Column(
        Integer,
        ForeignKey("unit_assessments.id"),
        nullable=False
    )
    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False
    )
