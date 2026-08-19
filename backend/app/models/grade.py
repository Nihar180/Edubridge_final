from sqlalchemy import Column, Integer, String
from app.database import Base


class Grade(Base):
    __tablename__ = "grades"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        String(50),
        unique=True,
        nullable=False
    )