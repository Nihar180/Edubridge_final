from sqlalchemy import Column, Integer, String, ForeignKey, Text

from app.database import Base


class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, autoincrement=True)

    module_id = Column(
        Integer,
        ForeignKey("modules.id"),
        nullable=False
    )

    question = Column(
        Text,
        nullable=False
    )

    answer = Column(
        Text,
        nullable=False
    )

    difficulty = Column(
        String(30),
        nullable=True
    )