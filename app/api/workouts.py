from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.workout import WorkoutCreate, WorkoutResponse, WorkoutUpdate
from app.services import workout_service

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.get("/", response_model=list[WorkoutResponse])
def list_workouts(
    training_week_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return workout_service.get_workouts_by_week(db, training_week_id, current_user.id)


@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(workout_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return workout_service.get_workout_owned(db, workout_id, current_user.id)


@router.post("/", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
def create_workout(
    workout_in: WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return workout_service.create_workout(db, current_user.id, workout_in)


@router.patch("/{workout_id}", response_model=WorkoutResponse)
def update_workout(
    workout_id: int,
    workout_in: WorkoutUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workout = workout_service.get_workout_owned(db, workout_id, current_user.id)
    return workout_service.update_workout(db, workout, workout_in, current_user.id)


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workout = workout_service.get_workout_owned(db, workout_id, current_user.id)
    workout_service.delete_workout(db, workout)
