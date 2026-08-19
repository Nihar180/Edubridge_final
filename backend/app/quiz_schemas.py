from typing import List, Optional
from pydantic import BaseModel


class QuestionOptionResponse(BaseModel):
    id: int
    option_text: str

    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    question_type: str
    difficulty: Optional[str] = None
    explanation: Optional[str] = None
    options: List[QuestionOptionResponse] = []

    class Config:
        from_attributes = True


class QuizResponse(BaseModel):
    id: int
    module_id: int
    title: str
    description: Optional[str] = None
    time_limit: Optional[int] = None
    quiz_type: Optional[str] = None
    questions: List[QuestionResponse] = []

    class Config:
        from_attributes = True


class QuizAnswer(BaseModel):
    question_id: int
    selected_option_id: Optional[int] = None
    time_taken: Optional[int] = None


class QuizSubmitRequest(BaseModel):
    answers: List[QuizAnswer]


class QuizResultResponse(BaseModel):
    attempt_id: int
    quiz_id: int
    score: int
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    unanswered: int
    percentage: float
    performance: str
    completed_at: str