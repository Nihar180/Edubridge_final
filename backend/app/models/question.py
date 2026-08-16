from sqlalchemy import Column, Integer, String, ForeignKey, Text

from app.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id"),
        nullable=False
    )

    question_text = Column(
        Text,
        nullable=False
    )

    question_type = Column(
        String(30),
        nullable=False
    )

    difficulty = Column(
        String(30),
        nullable=True
    )

    explanation = Column(
        Text,
        nullable=True
    )