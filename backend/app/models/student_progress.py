from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, func, UniqueConstraint
from app.database import Base


class StudentProgress(Base):
    __tablename__ = "student_progress"

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
    completion_percentage = Column(Float, nullable=False, default=0.0)
    mastery_score = Column(Float, nullable=False, default=0.0)
    last_accessed = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("user_id", "module_id", name="uq_user_module_progress"),
    )
