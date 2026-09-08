from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.training_week import TrainingWeek
from app.schemas.training_week import TrainingWeekCreate, TrainingWeekUpdate
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
