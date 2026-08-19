from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime

from app.database import Base


class AIMessage(Base):
    __tablename__ = "ai_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)

    conversation_id = Column(
        Integer,
        ForeignKey("ai_conversations.id"),
        nullable=False
    )

    sender = Column(
        String(20),
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False
    )