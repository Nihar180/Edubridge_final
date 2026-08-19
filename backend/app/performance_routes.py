from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.module import Module
from app.models.performance_analysis import PerformanceAnalysis
from app.auth.dependencies import get_current_user
from app.performance_schemas import PerformanceResponse, PerformanceSummaryResponse
from app.services.analytics_service import update_performance_analysis

router = APIRouter(
    prefix="/performance",
    tags=["Performance Analysis"]
)


@router.get("/me", response_model=PerformanceResponse)
def get_my_performance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns latest/primary module performance analysis for current student.
    """
    performance = update_performance_analysis(db, current_user.id)
    return performance


@router.get("/module/{module_id}", response_model=PerformanceResponse)
def get_module_performance(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns performance analysis for a specific module.
    """
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    performance = update_performance_analysis(db, current_user.id, module_id=module_id)
    return performance


@router.get("/summary", response_model=PerformanceSummaryResponse)
def get_performance_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns full module-by-module performance breakdown and aggregate stats.
    """
    perf_records = db.query(PerformanceAnalysis).filter(
        PerformanceAnalysis.user_id == current_user.id
    ).all()

    total_attempts = sum(p.total_attempts for p in perf_records)
    total_correct = sum(p.correct_answers for p in perf_records)
    total_q = sum(p.total_questions for p in perf_records)
    overall_acc = round((total_correct / total_q * 100.0), 2) if total_q > 0 else 0.0

    if overall_acc >= 80.0:
        overall_weakness = "Strong"
    elif overall_acc >= 60.0:
        overall_weakness = "Moderate"
    else:
        overall_weakness = "Weak"

    return PerformanceSummaryResponse(
        user_id=current_user.id,
        total_attempts=total_attempts,
        correct_answers=total_correct,
        total_questions=total_q,
        accuracy=overall_acc,
        weakness_level=overall_weakness,
        module_performances=perf_records
    )
