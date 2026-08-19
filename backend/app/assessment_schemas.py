from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class AssessmentQuestionOptionResponse(BaseModel):
    id: int
    option_text: str

    model_config = ConfigDict(from_attributes=True)


class AssessmentQuestionResponse(BaseModel):
    id: int
    question_text: str
    question_type: str
    difficulty: Optional[str] = None
    options: List[AssessmentQuestionOptionResponse] = []


class AssessmentResponse(BaseModel):
    id: int
    unit_id: int
    title: str
    description: Optional[str] = None
    time_limit: Optional[int] = None
    questions: List[AssessmentQuestionResponse] = []


class AssessmentAnswer(BaseModel):
    question_id: int
    selected_option_id: Optional[int] = None
    time_taken: Optional[int] = None


class AssessmentSubmitRequest(BaseModel):
    answers: List[AssessmentAnswer]


class PerformanceSummary(BaseModel):
    correct_answers: int
    incorrect_answers: int
    unanswered: int
    percentage: float
    performance: str


class AssessmentResultResponse(PerformanceSummary):
    attempt_id: int
    assessment_id: int
    score: int
    total_questions: int
    completed_at: str


class AssessmentAttemptStartResponse(BaseModel):
    attempt_id: int
    assessment_id: int
    total_questions: int
    started_at: str
