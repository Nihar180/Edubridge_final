from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.learning_content import LearningContent
from app.models.module import Module
from app.models.user import User
from app.auth.dependencies import require_admin, get_current_user
from app.learning_content_schemas import (
    LearningContentCreate,
    LearningContentResponse
)


router = APIRouter(
    prefix="/learning-contents",
    tags=["Learning Contents"]
)


@router.post("/", response_model=LearningContentResponse)
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
    return db.query(LearningContent).order_by(LearningContent.order_number).all()
