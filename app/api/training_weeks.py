from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.training_week import TrainingWeekCreate, TrainingWeekResponse, TrainingWeekUpdate
from app.services import training_week_service

router = APIRouter(prefix="/training-weeks", tags=["training-weeks"])


@router.get("/", response_model=list[TrainingWeekResponse])
def list_training_weeks(
    training_block_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return training_week_service.get_training_weeks_by_block(db, training_block_id, current_user.id)


@router.get("/{week_id}", response_model=TrainingWeekResponse)
def get_training_week(week_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return training_week_service.get_training_week_owned(db, week_id, current_user.id)


@router.post("/", response_model=TrainingWeekResponse, status_code=status.HTTP_201_CREATED)
def create_training_week(
    week_in: TrainingWeekCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return training_week_service.create_training_week(db, current_user.id, week_in)


@router.patch("/{week_id}", response_model=TrainingWeekResponse)
def update_training_week(
    week_id: int,
    week_in: TrainingWeekUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    week = training_week_service.get_training_week_owned(db, week_id, current_user.id)
    return training_week_service.update_training_week(db, week, week_in, current_user.id)


@router.delete("/{week_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_training_week(
    week_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    week = training_week_service.get_training_week_owned(db, week_id, current_user.id)
    training_week_service.delete_training_week(db, week)
