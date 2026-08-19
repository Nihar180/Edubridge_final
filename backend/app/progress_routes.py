from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.module import Module
from app.models.student_progress import StudentProgress
from app.auth.dependencies import get_current_user
from app.progress_schemas import ProgressResponse, ProgressUpdate, ProgressSummaryResponse
from app.services.analytics_service import update_student_progress

router = APIRouter(
    prefix="/progress",
    tags=["Student Progress"]
)


@router.get("/me", response_model=ProgressSummaryResponse)
def get_my_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    progress_list = db.query(StudentProgress).filter(
        StudentProgress.user_id == current_user.id
    ).all()

    total_modules = len(progress_list)
    avg_completion = round(sum(p.completion_percentage for p in progress_list) / total_modules, 2) if total_modules > 0 else 0.0
    avg_mastery = round(sum(p.mastery_score for p in progress_list) / total_modules, 2) if total_modules > 0 else 0.0

    return ProgressSummaryResponse(
        total_modules_tracked=total_modules,
        average_completion=avg_completion,
        average_mastery=avg_mastery,
        progress_records=progress_list
    )


@router.get("/module/{module_id}", response_model=ProgressResponse)
def get_module_progress(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )

    progress = db.query(StudentProgress).filter(
        StudentProgress.user_id == current_user.id,
        StudentProgress.module_id == module_id
    ).first()

    if not progress:
        progress = update_student_progress(
            db=db,
            user_id=current_user.id,
            module_id=module_id,
            completion_percentage=0.0,
            mastery_score=0.0
        )

    return progress


@router.post("/module/{module_id}", response_model=ProgressResponse)
def record_module_progress(
    module_id: int,
    progress_in: ProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )

    progress = update_student_progress(
        db=db,
        user_id=current_user.id,
        module_id=module_id,
        completion_percentage=progress_in.completion_percentage,
        mastery_score=progress_in.mastery_score
    )

    return progress
