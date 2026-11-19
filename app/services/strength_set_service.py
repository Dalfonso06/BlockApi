from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.strength_set import StrengthSet
from app.schemas.strength_set import StrengthSetCreate, StrengthSetUpdate
from app.services import strength_activity_detail_service


def get_strength_set_by_id(db: Session, set_id: int) -> StrengthSet | None:
    return db.query(StrengthSet).filter(StrengthSet.id == set_id).first()


def get_strength_set_owned(db: Session, set_id: int, user_id: int) -> StrengthSet:
    strength_set = get_strength_set_by_id(db, set_id)

    if strength_set is None:
        raise NotFoundError("Strength set not found")

    # Delegate the ownership walk to strength_activity_detail_service rather
    # than re-implementing the 2-hop walk to Activity inline.
    strength_activity_detail_service.get_strength_activity_detail_owned(
        db, strength_set.strength_exercise_id, user_id
    )

    return strength_set


def get_strength_sets_by_detail(db: Session, strength_exercise_id: int, user_id: int) -> list[StrengthSet]:
    strength_activity_detail_service.get_strength_activity_detail_owned(db, strength_exercise_id, user_id)
    return db.query(StrengthSet).filter(StrengthSet.strength_exercise_id == strength_exercise_id).all()


def create_strength_set(db: Session, user_id: int, set_in: StrengthSetCreate) -> StrengthSet:
    strength_activity_detail_service.get_strength_activity_detail_owned(db, set_in.strength_exercise_id, user_id)

    strength_set = StrengthSet(**set_in.model_dump())
    db.add(strength_set)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("A strength set with this set number already exists for this exercise")

    db.refresh(strength_set)
    return strength_set


def update_strength_set(
    db: Session, strength_set: StrengthSet, set_in: StrengthSetUpdate, user_id: int
) -> StrengthSet:
    data = set_in.model_dump(exclude_unset=True)

    new_detail_id = data.get("strength_exercise_id")
    if new_detail_id is not None and new_detail_id != strength_set.strength_exercise_id:
        strength_activity_detail_service.get_strength_activity_detail_owned(db, new_detail_id, user_id)

    for field, value in data.items():
        setattr(strength_set, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("A strength set with this set number already exists for this exercise")

    db.refresh(strength_set)
    return strength_set


def delete_strength_set(db: Session, strength_set: StrengthSet) -> None:
    db.delete(strength_set)
    db.commit()
