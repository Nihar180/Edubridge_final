from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.module import Module
from app.models.unit import Unit
from app.models.user import User
from app.auth.dependencies import require_admin, get_current_user
from app.module_schemas import ModuleCreate, ModuleResponse


router = APIRouter(
    prefix="/modules",
    tags=["Modules"]
)


@router.post("/", response_model=ModuleResponse)
def create_module(
    module: ModuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    unit = db.query(Unit).filter(
        Unit.id == module.unit_id
    ).first()

    if not unit:
        raise HTTPException(
            status_code=404,
            detail="Unit not found"
        )

    new_module = Module(
        unit_id=module.unit_id,
        title=module.title,
        description=module.description,
        order_number=module.order_number,
        difficulty=module.difficulty
    )

    db.add(new_module)
    db.commit()
    db.refresh(new_module)

    return new_module


@router.get("/", response_model=list[ModuleResponse])
def get_modules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Module).order_by(Module.order_number).all()