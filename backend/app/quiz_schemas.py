from datetime import datetime
from pydantic import BaseModel, ConfigDict


# --- Question Option Schemas ---
class QuestionOptionCreate(BaseModel):
    option_text: str
    is_correct: bool = False
    order_number: int = 1


class QuestionOptionUpdate(BaseModel):
    option_text: str | None = None
    is_correct: bool | None = None
    order_number: int | None = None


class QuestionOptionResponse(BaseModel):
    id: int
    question_id: int
    option_text: str
    is_correct: bool
    order_number: int

    model_config = ConfigDict(from_attributes=True)


class QuestionOptionStudentResponse(BaseModel):
    id: int
    question_id: int
    option_text: str
    order_number: int

    model_config = ConfigDict(from_attributes=True)


# --- Question Schemas ---
class QuestionCreate(BaseModel):
    question_text: str
    question_type: str = "mcq"
    difficulty: str = "Medium"
    marks: int = 4
    order_number: int = 1
    is_approved: bool = True
    options: list[QuestionOptionCreate] = []


class QuestionUpdate(BaseModel):
    question_text: str | None = None
    question_type: str | None = None
    difficulty: str | None = None
    marks: int | None = None
    order_number: int | None = None
    is_approved: bool | None = None


class QuestionResponse(BaseModel):
    id: int
    quiz_id: int
    question_text: str
    question_type: str
    difficulty: str = "Medium"
    marks: int
    order_number: int
    is_approved: bool = True
    options: list[QuestionOptionResponse] = []

    model_config = ConfigDict(from_attributes=True)


class QuestionStudentResponse(BaseModel):
    id: int
    quiz_id: int
    question_text: str
    question_type: str
    difficulty: str = "Medium"
    marks: int = 4
    order_number: int
    options: list[QuestionOptionStudentResponse] = []

    model_config = ConfigDict(from_attributes=True)


# --- Quiz Schemas ---
class QuizCreate(BaseModel):
    module_id: int
    title: str
    description: str | None = None
    total_marks: int = 0
    pass_percentage: float = 60.0
    time_limit_minutes: int = 10
    questions: list[QuestionCreate] = []


class QuizUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    total_marks: int | None = None
    pass_percentage: float | None = None
    time_limit_minutes: int | None = None


class QuizSummaryResponse(BaseModel):
    id: int
    module_id: int
    title: str
    description: str | None = None
    total_marks: int
    pass_percentage: float
    time_limit_minutes: int = 10
    is_locked: bool | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class QuizResponse(BaseModel):
    id: int
    module_id: int
    title: str
    description: str | None = None
    total_marks: int
    pass_percentage: float
    time_limit_minutes: int = 10
    created_at: datetime | None = None
    questions: list[QuestionResponse] = []

    model_config = ConfigDict(from_attributes=True)


class QuizStudentResponse(BaseModel):
    id: int
    module_id: int
    title: str
    description: str | None = None
    total_marks: int
    pass_percentage: float
    time_limit_minutes: int = 10
    total_questions: int = 0
    questions: list[QuestionStudentResponse] = []

    model_config = ConfigDict(from_attributes=True)


class QuizBankGenerateRequest(BaseModel):
    count: int = 30


# --- Quiz Submission & Attempt Schemas ---
class QuestionAnswerSubmit(BaseModel):
    question_id: int
    selected_option_id: int | None = None


class QuizSubmissionRequest(BaseModel):
    attempt_id: int | None = None
    answers: list[QuestionAnswerSubmit] = []


class QuestionAttemptResultResponse(BaseModel):
    question_id: int
    question_text: str
    selected_option_id: int | None
    correct_option_id: int | None
    is_correct: bool
    marks_awarded: float
    max_marks: int


class QuizAttemptResultResponse(BaseModel):
    attempt_id: int
    quiz_id: int
    user_id: int
    score: float
    total_marks: float
    percentage: float
    passed: bool
    latest_score: float | None = None
    best_score: float | None = None
    accuracy: float | None = None
    weakness_level: str | None = None
    time_taken_seconds: int | None = None
    started_at: datetime
    completed_at: datetime | None
    question_results: list[QuestionAttemptResultResponse] = []


class QuizAttemptSummaryResponse(BaseModel):
    id: int
    quiz_id: int
    user_id: int
    score: float
    total_marks: float
    percentage: float
    passed: bool
    time_taken_seconds: int | None = None
    started_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
