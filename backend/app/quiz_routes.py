from datetime import datetime

from app.auth.dependencies import require_student
from app.models.user import User

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.quiz_attempt import QuizAttempt
from app.models.question_attempt import QuestionAttempt

from app.quiz_schemas import (
    QuizResponse,
    QuizSubmitRequest,
    QuizResultResponse,
)

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


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
        "incorrect_answers": max(answered - correct, 0),
        "unanswered": max(total - answered, 0),
        "percentage": percentage,
        "performance": label,
    }


@router.get("/attempts/{attempt_id}", response_model=QuizResultResponse)
def get_quiz_result(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    attempt = db.query(QuizAttempt).filter(
        QuizAttempt.id == attempt_id,
        QuizAttempt.user_id == current_user.id,
    ).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Quiz attempt not found")

    answers = db.query(QuestionAttempt).filter(
        QuestionAttempt.attempt_id == attempt.id
    ).all()
    correct = attempt.score or 0
    return {
        "attempt_id": attempt.id,
        "quiz_id": attempt.quiz_id,
        "score": correct,
        "total_questions": attempt.total_questions,
        "correct_answers": correct,
        "completed_at": (attempt.completed_at or attempt.started_at).isoformat(),
        **_performance(
            correct,
            attempt.total_questions,
            sum(answer.selected_option_id is not None for answer in answers),
        ),
    }


@router.get("/my-attempts", response_model=list[QuizResultResponse])
def get_my_quiz_attempts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.completed_at.isnot(None),
    ).order_by(QuizAttempt.completed_at.desc()).all()
    return [get_quiz_result(attempt.id, db, current_user) for attempt in attempts]


@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    questions = (
        db.query(Question)
        .filter(Question.quiz_id == quiz_id)
        .all()
    )

    question_data = []

    for question in questions:
        options = (
            db.query(QuestionOption)
            .filter(QuestionOption.question_id == question.id)
            .all()
        )

        question_data.append({
            "id": question.id,
            "question_text": question.question_text,
            "question_type": question.question_type,
            "difficulty": question.difficulty,
            "explanation": question.explanation,
            "options": options
        })

    return {
        "id": quiz.id,
        "module_id": quiz.module_id,
        "title": quiz.title,
        "description": quiz.description,
        "time_limit": quiz.time_limit,
        "quiz_type": quiz.quiz_type,
        "questions": question_data
    }


@router.post(
    "/{quiz_id}/submit",
    response_model=QuizResultResponse
)
def submit_quiz(
    quiz_id: int,
    submission: QuizSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    questions = (
        db.query(Question)
        .filter(Question.quiz_id == quiz_id)
        .all()
    )

    if not questions:
        raise HTTPException(
            status_code=400,
            detail="Quiz has no questions"
        )

    question_map = {
        question.id: question
        for question in questions
    }

    started_at = datetime.utcnow()

    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz_id,
        score=0,
        total_questions=len(questions),
        started_at=started_at,
        completed_at=datetime.utcnow()
    )

    db.add(attempt)
    db.flush()

    correct_answers = 0
    submitted_ids = set()

    for answer in submission.answers:

        if answer.question_id in submitted_ids:
            raise HTTPException(
                status_code=400,
                detail="Duplicate question answer"
            )
        submitted_ids.add(answer.question_id)

        question = question_map.get(answer.question_id)

        if not question:
            raise HTTPException(
                status_code=400,
                detail="Question does not belong to quiz"
            )

        selected_option = None

        if answer.selected_option_id is not None:
            selected_option = (
                db.query(QuestionOption)
                .filter(
                    QuestionOption.id == answer.selected_option_id,
                    QuestionOption.question_id == question.id
                )
                .first()
            )

            if not selected_option:
                raise HTTPException(
                    status_code=400,
                    detail="Option does not belong to question"
                )

        is_correct = (
            selected_option is not None
            and selected_option.is_correct
        )

        if is_correct:
            correct_answers += 1

        question_attempt = QuestionAttempt(
            attempt_id=attempt.id,
            question_id=question.id,
            selected_option_id=(
                selected_option.id
                if selected_option
                else None
            ),
            is_correct=is_correct,
            time_taken=answer.time_taken
        )

        db.add(question_attempt)

    attempt.score = correct_answers

    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": attempt.id,
        "quiz_id": quiz_id,
        "score": correct_answers,
        "total_questions": len(questions),
        "correct_answers": correct_answers,
        **_performance(correct_answers, len(questions), len(submitted_ids)),
        "completed_at": attempt.completed_at.isoformat()
    }