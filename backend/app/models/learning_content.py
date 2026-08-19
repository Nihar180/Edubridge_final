from sqlalchemy import Column, Integer, String, ForeignKey, Text

from app.database import Base


class LearningContent(Base):
    __tablename__ = "learning_contents"

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

    content_type = Column(
        String(30),
        nullable=False
    )

    content = Column(
        Text,
        nullable=True
    )

    media_url = Column(
        Text,
        nullable=True
    )

    order_number = Column(
        Integer,
        nullable=False
    )