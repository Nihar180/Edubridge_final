from fastapi import APIRouter, Depends

from app.models.user import User
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "username": current_user.username,
        "email": current_user.email,
        "grade_id": current_user.grade_id
    }