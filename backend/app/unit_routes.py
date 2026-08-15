from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.unit import Unit
from app.models.subject import Subject
from app.unit_schemas import UnitCreate, UnitResponse

from app.models.user import User
from app.auth.dependencies import require_admin, get_current_user

router = APIRouter(
    prefix="/units",
    tags=["Units"]
)


@router.post("/", response_model=UnitResponse)
def create_unit(
    unit: UnitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    subject = db.query(Subject).filter(
        Subject.id == unit.subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    new_unit = Unit(
        subject_id=unit.subject_id,
        title=unit.title,
        description=unit.description,
        order_number=unit.order_number
    )

    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)

    return new_unit


@router.get("/", response_model=list[UnitResponse])
def get_units(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Unit).order_by(Unit.order_number).all()