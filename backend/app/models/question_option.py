from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean

from app.database import Base


class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, autoincrement=True)

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False
    )

    option_text = Column(
        Text,
        nullable=False
    )

    is_correct = Column(
        Boolean,
        nullable=False,
        default=False
    )