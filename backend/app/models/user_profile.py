from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from app.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )
    profile_image_url = Column(String(500), nullable=True)
    preferred_language = Column(String(50), nullable=True, default="English")
    learning_goal = Column(String(500), nullable=True)
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
