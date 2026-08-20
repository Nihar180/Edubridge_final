from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from app.database import Base


class UnitAssessment(Base):
    __tablename__ = "unit_assessments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    unit_id = Column(
        Integer,
        ForeignKey("units.id"),
        nullable=False
    )
    question_type = Column(
        String(50),
        nullable=False
    )  # "short_answer" or "long_answer"
    question_text = Column(Text, nullable=False)
    order_number = Column(Integer, nullable=False, default=1)
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
