from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.subject import Subject
from app.models.grade import Grade
from app.subject_schemas import SubjectCreate, SubjectResponse

from app.auth.dependencies import require_admin, get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"]
)


@router.post("/", response_model=SubjectResponse)
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    grade = db.query(Grade).filter(
        Grade.id == subject.grade_id
    ).first()

    if not grade:
        raise HTTPException(
            status_code=404,
            detail="Grade not found"
        )

    new_subject = Subject(
        grade_id=subject.grade_id,
        name=subject.name,
        description=subject.description
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject


@router.get("/", response_model=list[SubjectResponse])
def get_subjects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Subject).all()