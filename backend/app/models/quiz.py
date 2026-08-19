from sqlalchemy import Column, Integer, String, ForeignKey, Text

from app.database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, autoincrement=True)

    module_id = Column(
        Integer,
        ForeignKey("modules.id"),
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

    quiz_type = Column(
        String(30),
        nullable=True
    )