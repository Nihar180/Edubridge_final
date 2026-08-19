from datetime import datetime
import os
import shutil
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.learning_content import LearningContent, UserLearningContentProgress
from app.models.module import Module
from app.models.user import User
from app.auth.dependencies import require_admin, get_current_user
from app.learning_content_schemas import (
    LearningContentCreate,
    LearningContentResponse,
    LearningContentCompletionResponse
)
from app.services.analytics_service import recalculate_student_module_progress

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(
    prefix="/learning-contents",
    tags=["Learning Contents"]
)


@router.post("/upload")
def upload_learning_media(
    file: UploadFile = File(...),
    current_user: User = Depends(require_admin)
):
    """
    Upload a media/PDF file and return the media_url for use in LearningContent.
    """
    ext = os.path.splitext(file.filename)[1] if file.filename else ".pdf"
    safe_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    media_url = f"/uploads/{safe_filename}"
    return {
        "filename": file.filename,
        "media_url": media_url,
        "message": "File uploaded successfully"
    }


@router.post("/", response_model=LearningContentResponse, status_code=status.HTTP_201_CREATED)
def create_learning_content(
    content: LearningContentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    module = db.query(Module).filter(
        Module.id == content.module_id
    ).first()

    if not module:
        raise HTTPException(
            status_code=404,
            detail="Module not found"
        )

    new_content = LearningContent(
        module_id=content.module_id,
        title=content.title,
        content_type=content.content_type,
        content=content.content,
        media_url=content.media_url,
        order_number=content.order_number
    )

    db.add(new_content)
    db.commit()
    db.refresh(new_content)

    return new_content


@router.get("/", response_model=list[LearningContentResponse])
def get_learning_contents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contents = db.query(LearningContent).order_by(LearningContent.order_number).all()
    completed_ids = set(
        cid for (cid,) in db.query(UserLearningContentProgress.learning_content_id).filter(
            UserLearningContentProgress.user_id == current_user.id
        ).all()
    )

    result = []
    for c in contents:
        resp = LearningContentResponse.model_validate(c)
        resp.is_completed = c.id in completed_ids
        result.append(resp)
    return result


@router.get("/module/{module_id}", response_model=list[LearningContentResponse])
def get_learning_contents_by_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contents = db.query(LearningContent).filter(
        LearningContent.module_id == module_id
    ).order_by(LearningContent.order_number).all()

    completed_ids = set(
        cid for (cid,) in db.query(UserLearningContentProgress.learning_content_id).filter(
            UserLearningContentProgress.user_id == current_user.id
        ).all()
    )

    result = []
    for c in contents:
        resp = LearningContentResponse.model_validate(c)
        resp.is_completed = c.id in completed_ids
        result.append(resp)
    return result


@router.post("/{content_id}/complete", response_model=LearningContentCompletionResponse)
def mark_learning_content_completed(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Student clicks 'Mark as Completed' on learning content item.
    Gradually updates module student_progress and unlocks the quiz once 100% is reached.
    """
    content = db.query(LearningContent).filter(LearningContent.id == content_id).first()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning content not found"
        )

    # Record completion
    existing = db.query(UserLearningContentProgress).filter(
        UserLearningContentProgress.user_id == current_user.id,
        UserLearningContentProgress.learning_content_id == content_id
    ).first()

    now = datetime.now()
    if not existing:
        progress_rec = UserLearningContentProgress(
            user_id=current_user.id,
            learning_content_id=content_id,
            completed_at=now
        )
        db.add(progress_rec)
        db.commit()

    # Recalculate progress for the module
    recalculate_student_module_progress(
        db=db,
        user_id=current_user.id,
        module_id=content.module_id
    )

    # Calculate statistics
    total_contents = db.query(LearningContent).filter(
        LearningContent.module_id == content.module_id
    ).count()

    completed_contents = db.query(UserLearningContentProgress).join(
        LearningContent,
        UserLearningContentProgress.learning_content_id == LearningContent.id
    ).filter(
        LearningContent.module_id == content.module_id,
        UserLearningContentProgress.user_id == current_user.id
    ).count()

    completion_percentage = (completed_contents / total_contents * 100.0) if total_contents > 0 else 100.0
    all_completed = completed_contents >= total_contents

    return LearningContentCompletionResponse(
        message="Learning content marked as completed successfully",
        content_id=content_id,
        module_id=content.module_id,
        completed_at=now,
        module_content_completion_percentage=round(completion_percentage, 2),
        all_content_completed=all_completed,
        quiz_unlocked=all_completed
    )
