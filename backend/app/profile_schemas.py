from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProfileUpdate(BaseModel):
    profile_image_url: str | None = None
    preferred_language: str | None = None
    learning_goal: str | None = None


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    name: str
    username: str
    email: str
    role: str
    grade_id: int | None = None
    profile_image_url: str | None = None
    preferred_language: str | None = "English"
    learning_goal: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
