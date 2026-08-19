from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(
        Integer,
        ForeignKey("modules.id"),
        nullable=False
    )
    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    total_marks = Column(Integer, nullable=False, default=0)
    pass_percentage = Column(Float, nullable=False, default=60.0)
    time_limit_minutes = Column(Integer, nullable=False, default=10)
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    questions = relationship(
        "Question",
        back_populates="quiz",
        cascade="all, delete-orphan",
        order_by="Question.order_number"
    )


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id"),
        nullable=False
    )
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False, default="mcq")
    difficulty = Column(String(20), nullable=False, default="Medium")
    marks = Column(Integer, nullable=False, default=4)
    order_number = Column(Integer, nullable=False, default=1)
    is_approved = Column(Boolean, nullable=False, default=True)

    quiz = relationship("Quiz", back_populates="questions")
    options = relationship(
        "QuestionOption",
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="QuestionOption.order_number"
    )


class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False
    )
    option_text = Column(String(500), nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)
    order_number = Column(Integer, nullable=False, default=1)

    question = relationship("Question", back_populates="options")
