from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.grade import Grade
from app.grade_schemas import GradeResponse

from app.models.user import User
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/grades",
    tags=["Grades"]
)


@router.get("/", response_model=list[GradeResponse])
def get_grades(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Grade).all()