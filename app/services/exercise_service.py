from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate


def get_all_exercises(db: Session) -> list[Exercise]:
    return db.query(Exercise).all()


def get_exercise_by_id(db: Session, exercise_id: int) -> Exercise | None:
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()


def get_exercise_required(db: Session, exercise_id: int) -> Exercise:
    exercise = get_exercise_by_id(db, exercise_id)

    if exercise is None:
        raise NotFoundError("Exercise not found")

    return exercise


def create_exercise(db: Session, exercise_in: ExerciseCreate) -> Exercise:
    exercise = Exercise(**exercise_in.model_dump())
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


def update_exercise(db: Session, exercise: Exercise, exercise_in: ExerciseUpdate) -> Exercise:
    data = exercise_in.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(exercise, field, value)

    db.commit()
    db.refresh(exercise)
    return exercise


def delete_exercise(db: Session, exercise: Exercise) -> None:
    db.delete(exercise)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("Cannot delete an exercise that is still referenced by existing strength activity details")
