from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.user_profile import UserProfile
from app.auth.dependencies import get_current_user
from app.profile_schemas import ProfileResponse, ProfileUpdate

router = APIRouter(
    prefix="/profiles",
    tags=["User Profiles"]
)


def _get_or_create_profile(user: User, db: Session) -> UserProfile:
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == user.id
    ).first()

    if not profile:
        profile = UserProfile(
            user_id=user.id,
            profile_image_url=None,
            preferred_language="English",
            learning_goal=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile


@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = _get_or_create_profile(current_user, db)
    return ProfileResponse(
        id=profile.id,
        user_id=current_user.id,
        name=current_user.name,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        grade_id=current_user.grade_id,
        profile_image_url=profile.profile_image_url,
        preferred_language=profile.preferred_language,
        learning_goal=profile.learning_goal,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )


@router.put("/me", response_model=ProfileResponse)
def update_my_profile(
    profile_in: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = _get_or_create_profile(current_user, db)

    if profile_in.profile_image_url is not None:
        profile.profile_image_url = profile_in.profile_image_url
    if profile_in.preferred_language is not None:
        profile.preferred_language = profile_in.preferred_language
    if profile_in.learning_goal is not None:
        profile.learning_goal = profile_in.learning_goal

    profile.updated_at = datetime.now()
    db.commit()
    db.refresh(profile)

    return ProfileResponse(
        id=profile.id,
        user_id=current_user.id,
        name=current_user.name,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        grade_id=current_user.grade_id,
        profile_image_url=profile.profile_image_url,
        preferred_language=profile.preferred_language,
        learning_goal=profile.learning_goal,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )
