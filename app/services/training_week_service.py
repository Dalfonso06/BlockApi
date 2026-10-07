from datetime import timedelta

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.training_block import TrainingBlock
from app.models.training_week import TrainingWeek
from app.models.workout import DistanceUnit, Workout
from app.models.workout_type import WorkoutType
from app.schemas.training_week import (
    TrainingWeekBreakdownResponse,
    TrainingWeekCreate,
    TrainingWeekUpdate,
    WorkoutTypeBreakdownItem,
)
from app.services import training_block_service


def get_training_week_by_id(db: Session, week_id: int) -> TrainingWeek | None:
    return db.query(TrainingWeek).filter(TrainingWeek.id == week_id).first()


def get_training_week_owned(db: Session, week_id: int, user_id: int) -> TrainingWeek:
    week = get_training_week_by_id(db, week_id)

    if week is None:
        raise NotFoundError("Training week not found")

    block = training_block_service.get_training_block_by_id(db, week.training_block_id)

    if block is None or block.user_id != user_id:
        raise PermissionDeniedError("Not authorized to access this training week")

    return week


def get_training_weeks_by_block(db: Session, training_block_id: int, user_id: int) -> list[TrainingWeek]:
    training_block_service.get_training_block_owned(db, training_block_id, user_id)
    return db.query(TrainingWeek).filter(TrainingWeek.training_block_id == training_block_id).all()


def create_training_week(db: Session, user_id: int, week_in: TrainingWeekCreate) -> TrainingWeek:
    training_block_service.get_training_block_owned(db, week_in.training_block_id, user_id)

    week = TrainingWeek(**week_in.model_dump())
    db.add(week)
    db.commit()
    db.refresh(week)
    return week


def update_training_week(db: Session, week: TrainingWeek, week_in: TrainingWeekUpdate, user_id: int) -> TrainingWeek:
    data = week_in.model_dump(exclude_unset=True)

    new_block_id = data.get("training_block_id")
    if new_block_id is not None and new_block_id != week.training_block_id:
        training_block_service.get_training_block_owned(db, new_block_id, user_id)

    for field, value in data.items():
        setattr(week, field, value)

    db.commit()
    db.refresh(week)
    return week


def delete_training_week(db: Session, week: TrainingWeek) -> None:
    db.delete(week)
    db.commit()


def get_training_week_breakdown(db: Session, week_id: int, user_id: int) -> TrainingWeekBreakdownResponse:
    week = get_training_week_owned(db, week_id, user_id)

    rows = (
        db.query(Workout, WorkoutType.name)
        .join(WorkoutType, Workout.workout_type_id == WorkoutType.id)
        .filter(Workout.training_week_id == week_id)
        .order_by(WorkoutType.name)
        .all()
    )

    workouts_by_type: dict[str, list[Workout]] = {}
    for workout, workout_type_name in rows:
        workouts_by_type.setdefault(workout_type_name, []).append(workout)

    workout_types = []
    for workout_type_name, workouts in workouts_by_type.items():
        duration_sum = sum(workout.planned_duration or 0 for workout in workouts)

        # Only sum distance when every workout that has one shares the same
        # unit — adding e.g. miles and meters together would be meaningless.
        distance_entries = [
            (workout.planned_distance, workout.unit)
            for workout in workouts
            if workout.planned_distance is not None and workout.unit is not None
        ]
        units = {unit for _, unit in distance_entries}
        single_unit = DistanceUnit(units.pop()) if len(units) == 1 else None
        distance = sum(value for value, _ in distance_entries) if single_unit is not None else None

        workout_types.append(
            WorkoutTypeBreakdownItem(
                workout_type=workout_type_name,
                duration_sum=duration_sum,
                distance=distance,
                unit=single_unit,
            )
        )

    total_planned_duration_minutes = sum(workout.planned_duration or 0 for workout, _ in rows)

    return TrainingWeekBreakdownResponse(
        training_week_id=week.id,
        week_number=week.week_number,
        start_date=week.start_date,
        end_date=week.end_date,
        total_planned_duration_minutes=total_planned_duration_minutes,
        workout_types=workout_types,
    )


def generate_weeks_for_block(db: Session, block: TrainingBlock) -> list[TrainingWeek]:
    """Split a block's date range into Monday-Sunday weeks, numbered from 1.

    The first and last weeks are truncated to the block's actual start_date/
    end_date, so they can be partial; every week in between runs a full
    Monday through Sunday.
    """
    weeks: list[TrainingWeek] = []
    current_start = block.start_date
    week_number = 1

    while current_start <= block.end_date:
        days_until_sunday = 6 - current_start.weekday()
        natural_week_end = current_start + timedelta(days=days_until_sunday)
        week_end = min(natural_week_end, block.end_date)

        week = TrainingWeek(
            training_block_id=block.id,
            week_number=week_number,
            start_date=current_start,
            end_date=week_end,
        )
        db.add(week)
        weeks.append(week)

        week_number += 1
        current_start = week_end + timedelta(days=1)

    db.commit()

    for week in weeks:
        db.refresh(week)

    return weeks
