from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, autoincrement=True)

    grade_id = Column(
        Integer,
        ForeignKey("grades.id"),
        nullable=False
    )

    name = Column(
        String(100),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )