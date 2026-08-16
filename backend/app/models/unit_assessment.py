from sqlalchemy import Column, Integer, String, ForeignKey, Text

from app.database import Base


class UnitAssessment(Base):
    __tablename__ = "unit_assessments"

    id = Column(Integer, primary_key=True, autoincrement=True)

    unit_id = Column(
        Integer,
        ForeignKey("units.id"),
        nullable=False
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    time_limit = Column(
        Integer,
        nullable=True
    )