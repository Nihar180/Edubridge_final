from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.grade import Grade
from app.auth.schemas import RegisterRequest, LoginRequest
from app.auth.security import hash_password, verify_password, create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# REGISTER
@router.post("/register")
def register(
    user: RegisterRequest,
    db: Session = Depends(get_db)
):

    # Check username or email already exists
    existing_user = db.query(User).filter(
        (User.email == user.email) |
        (User.username == user.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )

    # Check whether grade exists
    grade = db.query(Grade).filter(
        Grade.id == user.grade_id
    ).first()

    if not grade:
        raise HTTPException(
            status_code=404,
            detail="Grade not found"
        )

    # Create user
    new_user = User(
        name=user.name,
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
        grade_id=user.grade_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


# LOGIN
@router.post("/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):

    # Find user by username
    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Verify password
    if not verify_password(
        user.password,
        existing_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Create JWT token
    token = create_access_token({
        "user_id": existing_user.id
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }