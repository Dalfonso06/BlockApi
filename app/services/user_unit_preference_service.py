from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.user_unit_preference import UserWorkoutTypeUnitPreference
from app.services import workout_type_service


def get_user_unit_preferences(db: Session, user_id: int) -> list[UserWorkoutTypeUnitPreference]:
    return (
        db.query(UserWorkoutTypeUnitPreference)
        .filter(UserWorkoutTypeUnitPreference.user_id == user_id)
        .all()
    )


def get_user_unit_preference(db: Session, user_id: int, workout_type_id: int) -> UserWorkoutTypeUnitPreference | None:
    return (
        db.query(UserWorkoutTypeUnitPreference)
        .filter(
            UserWorkoutTypeUnitPreference.user_id == user_id,
            UserWorkoutTypeUnitPreference.workout_type_id == workout_type_id,
        )
        .first()
    )


def get_user_unit_preference_required(db: Session, user_id: int, workout_type_id: int) -> UserWorkoutTypeUnitPreference:
    preference = get_user_unit_preference(db, user_id, workout_type_id)

    if preference is None:
        raise NotFoundError("No unit preference set for this workout type")

    return preference


def set_user_unit_preference(
    db: Session, user_id: int, workout_type_id: int, unit: str
) -> UserWorkoutTypeUnitPreference:
    workout_type_service.get_workout_type_required(db, workout_type_id)

    preference = get_user_unit_preference(db, user_id, workout_type_id)

    if preference is None:
        preference = UserWorkoutTypeUnitPreference(user_id=user_id, workout_type_id=workout_type_id, unit=unit)
        db.add(preference)
    else:
        preference.unit = unit

    db.commit()
    db.refresh(preference)
    return preference


def delete_user_unit_preference(db: Session, preference: UserWorkoutTypeUnitPreference) -> None:
    db.delete(preference)
    db.commit()
