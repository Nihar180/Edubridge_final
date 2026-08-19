from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, UniqueConstraint, func
from app.database import Base


class PerformanceAnalysis(Base):
    __tablename__ = "performance_analysis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    module_id = Column(
        Integer,
        ForeignKey("modules.id"),
        nullable=False
    )
    total_attempts = Column(Integer, nullable=False, default=0)
    correct_answers = Column(Integer, nullable=False, default=0)
    total_questions = Column(Integer, nullable=False, default=0)
    accuracy = Column(Float, nullable=False, default=0.0)
    weakness_level = Column(String(50), nullable=False, default="Weak")
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("user_id", "module_id", name="uq_user_module_performance"),
    )
