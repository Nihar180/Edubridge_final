from pydantic import BaseModel


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
