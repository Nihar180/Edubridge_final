from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime

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

    completion_percentage = Column(
        Float,
        nullable=False,
        default=0
    )

    mastery_score = Column(
        Float,
        nullable=True
    )

    last_accessed = Column(
        DateTime,
        nullable=True
    )