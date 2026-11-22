from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.exercise import ExerciseCreate, ExerciseResponse, ExerciseUpdate
from app.services import exercise_service

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("/", response_model=list[ExerciseResponse])
def list_exercises(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return exercise_service.get_all_exercises(db)


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return exercise_service.get_exercise_required(db, exercise_id)


@router.post("/", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_exercise(
    exercise_in: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return exercise_service.create_exercise(db, exercise_in)


@router.patch("/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(
    exercise_id: int,
    exercise_in: ExerciseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exercise = exercise_service.get_exercise_required(db, exercise_id)
    return exercise_service.update_exercise(db, exercise, exercise_in)


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exercise = exercise_service.get_exercise_required(db, exercise_id)
    exercise_service.delete_exercise(db, exercise)
