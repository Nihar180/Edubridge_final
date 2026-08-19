from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.unit import Unit
from app.models.subject import Subject
from app.models.unit_assessment import UnitAssessment, AssessmentAttempt
from app.auth.dependencies import get_current_user
from app.unit_assessment_schemas import UnitAssessmentGroupedResponse, UnitAssessmentQuestionItem
from app.services.ai_assessment_service import generate_unit_assessment_questions

router = APIRouter(
    prefix="/unit-assessments",
    tags=["Unit Assessments"]
)


def _ensure_and_get_unit_questions(unit: Unit, db: Session) -> list[UnitAssessment]:
    existing_questions = db.query(UnitAssessment).filter(
        UnitAssessment.unit_id == unit.id
    ).order_by(UnitAssessment.question_type, UnitAssessment.order_number).all()

    if existing_questions:
        return existing_questions

    # Generate questions using AI assessment service
    subject = db.query(Subject).filter(Subject.id == unit.subject_id).first()
    subject_name = subject.name if subject else ""

    generated = generate_unit_assessment_questions(
        unit_title=unit.title,
        subject_name=subject_name,
        unit_description=unit.description or ""
    )

    created_questions = []

    # Insert 10 SAQs
    for idx, q_text in enumerate(generated["short_answer_questions"], start=1):
        q = UnitAssessment(
            unit_id=unit.id,
            question_type="short_answer",
            question_text=q_text,
            order_number=idx
        )
        db.add(q)
        created_questions.append(q)

    # Insert 10 LAQs
    for idx, q_text in enumerate(generated["long_answer_questions"], start=1):
        q = UnitAssessment(
            unit_id=unit.id,
            question_type="long_answer",
            question_text=q_text,
            order_number=idx
        )
        db.add(q)
        created_questions.append(q)

    db.commit()
    for q in created_questions:
        db.refresh(q)

    return created_questions


@router.get("/unit/{unit_id}", response_model=UnitAssessmentGroupedResponse)
def get_unit_assessment(
    unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves theoretical practice/reference questions for a unit (10 SAQ + 10 LAQ).
    No scoring, no timer, no submission. Reference-only material.
    """
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit not found"
        )

    # Record access in assessment_attempts
    access_record = AssessmentAttempt(
        unit_id=unit.id,
        user_id=current_user.id,
        accessed_at=datetime.now()
    )
    db.add(access_record)
    db.commit()

    questions = _ensure_and_get_unit_questions(unit, db)

    saqs = [
        UnitAssessmentQuestionItem.model_validate(q)
        for q in questions if q.question_type == "short_answer"
    ]
    laqs = [
        UnitAssessmentQuestionItem.model_validate(q)
        for q in questions if q.question_type == "long_answer"
    ]

    return UnitAssessmentGroupedResponse(
        unit_id=unit.id,
        unit_title=unit.title,
        short_answer_questions=saqs,
        long_answer_questions=laqs,
        total_short_answer_questions=len(saqs),
        total_long_answer_questions=len(laqs)
    )


@router.post("/unit/{unit_id}/generate", response_model=UnitAssessmentGroupedResponse)
def regenerate_unit_assessment(
    unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Regenerates the 20 practice questions (10 SAQ + 10 LAQ) for the specified unit.
    """
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit not found"
        )

    # Delete existing unit assessment questions
    db.query(UnitAssessment).filter(UnitAssessment.unit_id == unit.id).delete()
    db.commit()

    # Generate fresh questions
    questions = _ensure_and_get_unit_questions(unit, db)

    saqs = [
        UnitAssessmentQuestionItem.model_validate(q)
        for q in questions if q.question_type == "short_answer"
    ]
    laqs = [
        UnitAssessmentQuestionItem.model_validate(q)
        for q in questions if q.question_type == "long_answer"
    ]

    return UnitAssessmentGroupedResponse(
        unit_id=unit.id,
        unit_title=unit.title,
        short_answer_questions=saqs,
        long_answer_questions=laqs,
        total_short_answer_questions=len(saqs),
        total_long_answer_questions=len(laqs)
    )
