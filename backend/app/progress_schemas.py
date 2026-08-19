from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProgressUpdate(BaseModel):
    completion_percentage: float | None = None
    mastery_score: float | None = None


class ProgressResponse(BaseModel):
    id: int
    user_id: int
    module_id: int
    completion_percentage: float
    mastery_score: float
    last_accessed: datetime

    model_config = ConfigDict(from_attributes=True)


class ProgressSummaryResponse(BaseModel):
    total_modules_tracked: int
    average_completion: float
    average_mastery: float
    progress_records: list[ProgressResponse]
