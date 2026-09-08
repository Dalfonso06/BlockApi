from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.workout import Workout
from app.schemas.workout import WorkoutCreate, WorkoutUpdate
from app.services import training_week_service, workout_type_service


def get_workout_by_id(db: Session, workout_id: int) -> Workout | None:
    return db.query(Workout).filter(Workout.id == workout_id).first()


def get_workout_owned(db: Session, workout_id: int, user_id: int) -> Workout:
    workout = get_workout_by_id(db, workout_id)

    if workout is None:
        raise NotFoundError("Workout not found")

    if workout.user_id != user_id:
        raise PermissionDeniedError("Not authorized to access this workout")

    return workout


def get_workouts_by_week(db: Session, training_week_id: int, user_id: int) -> list[Workout]:
    training_week_service.get_training_week_owned(db, training_week_id, user_id)
    return db.query(Workout).filter(Workout.training_week_id == training_week_id).all()


def create_workout(db: Session, user_id: int, workout_in: WorkoutCreate) -> Workout:
    training_week_service.get_training_week_owned(db, workout_in.training_week_id, user_id)
    workout_type_service.get_workout_type_required(db, workout_in.workout_type_id)

    workout = Workout(user_id=user_id, **workout_in.model_dump())
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


def update_workout(db: Session, workout: Workout, workout_in: WorkoutUpdate, user_id: int) -> Workout:
    data = workout_in.model_dump(exclude_unset=True)

    new_week_id = data.get("training_week_id")
    if new_week_id is not None and new_week_id != workout.training_week_id:
        training_week_service.get_training_week_owned(db, new_week_id, user_id)

    new_workout_type_id = data.get("workout_type_id")
    if new_workout_type_id is not None:
        workout_type_service.get_workout_type_required(db, new_workout_type_id)

    for field, value in data.items():
        setattr(workout, field, value)

    db.commit()
    db.refresh(workout)
    return workout


def delete_workout(db: Session, workout: Workout) -> None:
    db.delete(workout)
    db.commit()
