from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.user_unit_preference import UserUnitPreferenceResponse, UserUnitPreferenceSet
from app.schemas.workout_type import WorkoutTypeUnitSummary
from app.services import user_service, user_unit_preference_service, workout_type_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_service.get_all_users(db)


@router.get("/me/workout-type-units", response_model=list[WorkoutTypeUnitSummary])
def get_my_workout_type_units(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return workout_type_service.get_workout_types_with_resolved_units(db, current_user.id)


@router.get("/me/unit-preferences", response_model=list[UserUnitPreferenceResponse])
def list_my_unit_preferences(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_unit_preference_service.get_user_unit_preferences(db, current_user.id)


@router.get("/me/unit-preferences/{workout_type_id}", response_model=UserUnitPreferenceResponse)
def get_my_unit_preference(
    workout_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_unit_preference_service.get_user_unit_preference_required(db, current_user.id, workout_type_id)


@router.put("/me/unit-preferences/{workout_type_id}", response_model=UserUnitPreferenceResponse)
def set_my_unit_preference(
    workout_type_id: int,
    preference_in: UserUnitPreferenceSet,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_unit_preference_service.set_user_unit_preference(
        db, current_user.id, workout_type_id, preference_in.unit
    )


@router.delete("/me/unit-preferences/{workout_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_unit_preference(
    workout_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    preference = user_unit_preference_service.get_user_unit_preference_required(
        db, current_user.id, workout_type_id
    )
    user_unit_preference_service.delete_user_unit_preference(db, preference)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = user_service.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authorized to update this user")

    user = user_service.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return user_service.update_user(db, user, user_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authorized to delete this user")

    user = user_service.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    user_service.delete_user(db, user)
