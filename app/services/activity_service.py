from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError, PermissionDeniedError
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate
from app.services import source_service, workout_service, workout_type_service


def get_activity_by_id(db: Session, activity_id: int) -> Activity | None:
    return db.query(Activity).filter(Activity.id == activity_id).first()


def get_activity_owned(db: Session, activity_id: int, user_id: int) -> Activity:
    activity = get_activity_by_id(db, activity_id)

    if activity is None:
        raise NotFoundError("Activity not found")

    if activity.user_id != user_id:
        raise PermissionDeniedError("Not authorized to access this activity")

    return activity


def get_activities_by_user(db: Session, user_id: int) -> list[Activity]:
    return db.query(Activity).filter(Activity.user_id == user_id).all()


def create_activity(db: Session, user_id: int, activity_in: ActivityCreate) -> Activity:
    workout_type_service.get_workout_type_required(db, activity_in.workout_type_id)
    source_service.get_source_required(db, activity_in.source_id)

    if activity_in.planned_workout_id is not None:
        workout_service.get_workout_owned(db, activity_in.planned_workout_id, user_id)

    activity = Activity(user_id=user_id, **activity_in.model_dump())
    db.add(activity)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("An activity with this source and external ID already exists")

    db.refresh(activity)
    return activity


def update_activity(db: Session, activity: Activity, activity_in: ActivityUpdate, user_id: int) -> Activity:
    data = activity_in.model_dump(exclude_unset=True)

    if "workout_type_id" in data:
        workout_type_service.get_workout_type_required(db, data["workout_type_id"])

    if "source_id" in data:
        source_service.get_source_required(db, data["source_id"])

    if "planned_workout_id" in data and data["planned_workout_id"] is not None:
        workout_service.get_workout_owned(db, data["planned_workout_id"], user_id)

    for field, value in data.items():
        setattr(activity, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("An activity with this source and external ID already exists")

    db.refresh(activity)
    return activity


def delete_activity(db: Session, activity: Activity) -> None:
    db.delete(activity)
    db.commit()
