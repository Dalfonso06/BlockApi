from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.workout_type import WorkoutType
from app.schemas.workout_type import WorkoutTypeCreate, WorkoutTypeUpdate


def get_all_workout_types(db: Session) -> list[WorkoutType]:
    return db.query(WorkoutType).all()


def get_workout_type_by_id(db: Session, workout_type_id: int) -> WorkoutType | None:
    return db.query(WorkoutType).filter(WorkoutType.id == workout_type_id).first()


def get_workout_type_required(db: Session, workout_type_id: int) -> WorkoutType:
    workout_type = get_workout_type_by_id(db, workout_type_id)

    if workout_type is None:
        raise NotFoundError("Workout type not found")

    return workout_type


def create_workout_type(db: Session, workout_type_in: WorkoutTypeCreate) -> WorkoutType:
    workout_type = WorkoutType(**workout_type_in.model_dump())
    db.add(workout_type)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("A workout type with this name already exists")

    db.refresh(workout_type)
    return workout_type


def update_workout_type(db: Session, workout_type: WorkoutType, workout_type_in: WorkoutTypeUpdate) -> WorkoutType:
    data = workout_type_in.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(workout_type, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("A workout type with this name already exists")

    db.refresh(workout_type)
    return workout_type


def delete_workout_type(db: Session, workout_type: WorkoutType) -> None:
    db.delete(workout_type)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("Cannot delete a workout type that is still referenced by existing workouts")
