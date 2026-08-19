from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PerformanceResponse(BaseModel):
    id: int
    user_id: int
    module_id: int | None = None
    total_attempts: int
    correct_answers: int
    total_questions: int = 0
    accuracy: float
    weakness_level: str
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PerformanceSummaryResponse(BaseModel):
    user_id: int
    total_attempts: int
    correct_answers: int
    total_questions: int
    accuracy: float
    weakness_level: str
    module_performances: list[PerformanceResponse] = []
