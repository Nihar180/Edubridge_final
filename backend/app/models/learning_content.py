from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, func
from app.database import Base


class LearningContent(Base):
    __tablename__ = "learning_contents"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    module_id = Column(
        Integer,
        ForeignKey("modules.id"),
        nullable=False
    )

    title = Column(
        String(150),
        nullable=False
    )

    content_type = Column(
        String(50),
        nullable=False
    )

    content = Column(
        Text,
        nullable=True
    )

    media_url = Column(
        String(500),
        nullable=True
    )

    order_number = Column(
        Integer,
        nullable=False
    )


class UserLearningContentProgress(Base):
    __tablename__ = "user_learning_content_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    learning_content_id = Column(
        Integer,
        ForeignKey("learning_contents.id"),
        nullable=False
    )
    completed_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("user_id", "learning_content_id", name="uq_user_learning_content_progress"),
    )
