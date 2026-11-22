from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError, PermissionDeniedError
from app.models.strength_activity_detail import StrengthActivityDetail
from app.schemas.strength_activity_detail import StrengthActivityDetailCreate, StrengthActivityDetailUpdate
from app.services import activity_service, exercise_service


def get_strength_activity_detail_by_id(db: Session, detail_id: int) -> StrengthActivityDetail | None:
    return db.query(StrengthActivityDetail).filter(StrengthActivityDetail.id == detail_id).first()


def get_strength_activity_detail_owned(db: Session, detail_id: int, user_id: int) -> StrengthActivityDetail:
    detail = get_strength_activity_detail_by_id(db, detail_id)

    if detail is None:
        raise NotFoundError("Strength activity detail not found")

    activity = activity_service.get_activity_by_id(db, detail.activity_id)

    if activity is None or activity.user_id != user_id:
        raise PermissionDeniedError("Not authorized to access this strength activity detail")

    return detail


def get_strength_activity_details_by_activity(
    db: Session, activity_id: int, user_id: int
) -> list[StrengthActivityDetail]:
    activity_service.get_activity_owned(db, activity_id, user_id)
    return db.query(StrengthActivityDetail).filter(StrengthActivityDetail.activity_id == activity_id).all()


def create_strength_activity_detail(
    db: Session, user_id: int, detail_in: StrengthActivityDetailCreate
) -> StrengthActivityDetail:
    activity_service.get_activity_owned(db, detail_in.activity_id, user_id)
    exercise_service.get_exercise_required(db, detail_in.exercise_id)

    detail = StrengthActivityDetail(**detail_in.model_dump())
    db.add(detail)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("A strength activity detail with this sequence already exists for this activity")

    db.refresh(detail)
    return detail


def update_strength_activity_detail(
    db: Session, detail: StrengthActivityDetail, detail_in: StrengthActivityDetailUpdate, user_id: int
) -> StrengthActivityDetail:
    data = detail_in.model_dump(exclude_unset=True)

    new_activity_id = data.get("activity_id")
    if new_activity_id is not None and new_activity_id != detail.activity_id:
        activity_service.get_activity_owned(db, new_activity_id, user_id)

    new_exercise_id = data.get("exercise_id")
    if new_exercise_id is not None and new_exercise_id != detail.exercise_id:
        exercise_service.get_exercise_required(db, new_exercise_id)

    for field, value in data.items():
        setattr(detail, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("A strength activity detail with this sequence already exists for this activity")

    db.refresh(detail)
    return detail


def delete_strength_activity_detail(db: Session, detail: StrengthActivityDetail) -> None:
    db.delete(detail)
    db.commit()
