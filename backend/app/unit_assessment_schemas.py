from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UnitAssessmentQuestionItem(BaseModel):
    id: int
    unit_id: int
    question_type: str
    question_text: str
    order_number: int

    model_config = ConfigDict(from_attributes=True)


class UnitAssessmentGroupedResponse(BaseModel):
    unit_id: int
    unit_title: str
    short_answer_questions: list[UnitAssessmentQuestionItem]
    long_answer_questions: list[UnitAssessmentQuestionItem]
    total_short_answer_questions: int
    total_long_answer_questions: int


class AssessmentAttemptResponse(BaseModel):
    id: int
    unit_id: int
    user_id: int
    accessed_at: datetime

    model_config = ConfigDict(from_attributes=True)
