from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.assessment_schemas import (
    AssessmentAttemptStartResponse,
    AssessmentQuestionResponse,
    AssessmentResponse,
    AssessmentResultResponse,
    AssessmentSubmitRequest,
)
from app.auth.dependencies import require_student
from app.database import get_db
from app.models.assessment_question import AssessmentQuestion
from app.models.assessment_question_attempt import AssessmentQuestionAttempt
from app.models.assessment_attempt import AssessmentAttempt
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.unit_assessment import UnitAssessment
from app.models.user import User

router = APIRouter(prefix="/assessments", tags=["Assessments"])


def _assessment_questions(db: Session, assessment_id: int):
    return (
        db.query(Question)
        .join(AssessmentQuestion, AssessmentQuestion.question_id == Question.id)
        .filter(AssessmentQuestion.assessment_id == assessment_id)
        .order_by(AssessmentQuestion.id)
        .all()
    )


def _performance(correct: int, total: int, answered: int):
    percentage = round((correct / total) * 100, 2) if total else 0
    if percentage >= 80:
        label = "Excellent"
    elif percentage >= 60:
        label = "Good"
    elif percentage >= 40:
        label = "Needs improvement"
    else:
        label = "Needs significant improvement"
    return {
        "correct_answers": correct,
        "incorrect_answers": max(answered - correct, 0),
        "unanswered": max(total - answered, 0),
        "percentage": percentage,
        "performance": label,
    }


@router.get("/{assessment_id}", response_model=AssessmentResponse)
def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    assessment = db.query(UnitAssessment).filter(UnitAssessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    questions = []
    for question in _assessment_questions(db, assessment_id):
        options = db.query(QuestionOption).filter(QuestionOption.question_id == question.id).all()
        questions.append(AssessmentQuestionResponse(
            id=question.id,
            question_text=question.question_text,
            question_type=question.question_type,
            difficulty=question.difficulty,
            options=options,
        ))

    return AssessmentResponse(
        id=assessment.id,
        unit_id=assessment.unit_id,
        title=assessment.title,
        description=assessment.description,
        time_limit=assessment.time_limit,
        questions=questions,
    )


@router.post("/{assessment_id}/attempts", response_model=AssessmentAttemptStartResponse)
def start_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    assessment = db.query(UnitAssessment).filter(UnitAssessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    questions = _assessment_questions(db, assessment_id)
    if not questions:
        raise HTTPException(status_code=400, detail="Assessment has no questions")

    attempt = AssessmentAttempt(
        user_id=current_user.id,
        assessment_id=assessment_id,
        score=0,
        total_questions=len(questions),
        started_at=datetime.utcnow(),
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return {
        "attempt_id": attempt.id,
        "assessment_id": assessment_id,
        "total_questions": attempt.total_questions,
        "started_at": attempt.started_at.isoformat(),
    }


@router.post("/{assessment_id}/attempts/{attempt_id}/submit", response_model=AssessmentResultResponse)
def submit_assessment(
    assessment_id: int,
    attempt_id: int,
    submission: AssessmentSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    attempt = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.id == attempt_id,
        AssessmentAttempt.assessment_id == assessment_id,
        AssessmentAttempt.user_id == current_user.id,
    ).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Assessment attempt not found")
    if attempt.completed_at:
        raise HTTPException(status_code=409, detail="Assessment attempt already submitted")

    questions = _assessment_questions(db, assessment_id)
    question_map = {question.id: question for question in questions}
    submitted_ids = set()
    correct = 0
    answered = 0

    for answer in submission.answers:
        if answer.question_id in submitted_ids:
            raise HTTPException(status_code=400, detail="Duplicate question answer")
        submitted_ids.add(answer.question_id)
        question = question_map.get(answer.question_id)
        if not question:
            raise HTTPException(status_code=400, detail="Question does not belong to assessment")

        selected = None
        if answer.selected_option_id is not None:
            selected = db.query(QuestionOption).filter(
                QuestionOption.id == answer.selected_option_id,
                QuestionOption.question_id == question.id,
            ).first()
            if not selected:
                raise HTTPException(status_code=400, detail="Option does not belong to question")
            answered += 1
        is_correct = bool(selected and selected.is_correct)
        correct += int(is_correct)
        db.add(AssessmentQuestionAttempt(
            attempt_id=attempt.id,
            question_id=question.id,
            selected_option_id=selected.id if selected else None,
            is_correct=is_correct,
            time_taken=answer.time_taken,
        ))

    attempt.score = correct
    attempt.completed_at = datetime.utcnow()
    db.commit()
    performance = _performance(correct, len(questions), answered)
    return {
        "attempt_id": attempt.id,
        "assessment_id": assessment_id,
        "score": correct,
        "total_questions": len(questions),
        "completed_at": attempt.completed_at.isoformat(),
        **performance,
    }


@router.get("/attempts/{attempt_id}", response_model=AssessmentResultResponse)
def get_assessment_result(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    attempt = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.id == attempt_id,
        AssessmentAttempt.user_id == current_user.id,
    ).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Assessment attempt not found")
    answers = db.query(AssessmentQuestionAttempt).filter(
        AssessmentQuestionAttempt.attempt_id == attempt.id
    ).all()
    performance = _performance(
        attempt.score or 0,
        attempt.total_questions,
        sum(answer.selected_option_id is not None for answer in answers),
    )
    return {
        "attempt_id": attempt.id,
        "assessment_id": attempt.assessment_id,
        "score": attempt.score or 0,
        "total_questions": attempt.total_questions,
        "completed_at": (attempt.completed_at or attempt.started_at).isoformat(),
        **performance,
    }


@router.get("/my-attempts", response_model=list[AssessmentResultResponse])
def get_my_assessment_attempts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    attempts = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.user_id == current_user.id,
        AssessmentAttempt.completed_at.isnot(None),
    ).order_by(AssessmentAttempt.completed_at.desc()).all()
    return [get_assessment_result(attempt.id, db, current_user) for attempt in attempts]


router.routes.sort(key=lambda route: route.path == "/assessments/{assessment_id}")