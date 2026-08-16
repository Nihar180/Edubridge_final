from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from app.database import Base


class StudentFlashcard(Base):
    __tablename__ = "student_flashcards"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    flashcard_id = Column(
        Integer,
        ForeignKey("flashcards.id"),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=True
    )

    last_reviewed = Column(
        DateTime,
        nullable=True
    )

    next_review = Column(
        DateTime,
        nullable=True
    )