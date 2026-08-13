from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.workout_type import WorkoutTypeCreate, WorkoutTypeResponse, WorkoutTypeUpdate
from app.services import workout_type_service

router = APIRouter(prefix="/workout-types", tags=["workout-types"])


@router.get("/", response_model=list[WorkoutTypeResponse])
def list_workout_types(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return workout_type_service.get_all_workout_types(db)


@router.get("/{workout_type_id}", response_model=WorkoutTypeResponse)
def get_workout_type(
    workout_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return workout_type_service.get_workout_type_required(db, workout_type_id)


@router.post("/", response_model=WorkoutTypeResponse, status_code=status.HTTP_201_CREATED)
def create_workout_type(
    workout_type_in: WorkoutTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return workout_type_service.create_workout_type(db, workout_type_in)


@router.patch("/{workout_type_id}", response_model=WorkoutTypeResponse)
def update_workout_type(
    workout_type_id: int,
    workout_type_in: WorkoutTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workout_type = workout_type_service.get_workout_type_required(db, workout_type_id)
    return workout_type_service.update_workout_type(db, workout_type, workout_type_in)


@router.delete("/{workout_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout_type(
    workout_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workout_type = workout_type_service.get_workout_type_required(db, workout_type_id)
    workout_type_service.delete_workout_type(db, workout_type)
