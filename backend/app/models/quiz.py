from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean, func, literal
from sqlalchemy.orm import column_property, relationship
from app.database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(
        Integer,
        ForeignKey("modules.id"),
        nullable=False
    )
    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    total_marks = column_property(literal(0))
    pass_percentage = column_property(literal(60.0))
    time_limit_minutes = Column(Integer, nullable=False, default=10)
    created_at = column_property(literal(None))

    questions = relationship(
        "Question",
        back_populates="quiz",
        cascade="all, delete-orphan",
        order_by="Question.id"
    )

