from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LearningContentCreate(BaseModel):
    module_id: int
    title: str
    content_type: str
    content: str | None = None
    media_url: str | None = None
    order_number: int


class LearningContentResponse(BaseModel):
    id: int
    module_id: int
    title: str
    content_type: str
    content: str | None = None
    media_url: str | None = None
    order_number: int
    is_completed: bool = False

    model_config = ConfigDict(from_attributes=True)


class LearningContentCompletionResponse(BaseModel):
    message: str
    content_id: int
    module_id: int
    completed_at: datetime
    module_content_completion_percentage: float
    all_content_completed: bool
    quiz_unlocked: bool
