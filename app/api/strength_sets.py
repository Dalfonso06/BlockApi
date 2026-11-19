from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.strength_set import StrengthSetCreate, StrengthSetResponse, StrengthSetUpdate
from app.services import strength_set_service

router = APIRouter(prefix="/strength-sets", tags=["strength-sets"])


@router.get("/", response_model=list[StrengthSetResponse])
def list_strength_sets(
    strength_exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return strength_set_service.get_strength_sets_by_detail(db, strength_exercise_id, current_user.id)


@router.get("/{set_id}", response_model=StrengthSetResponse)
def get_strength_set(set_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return strength_set_service.get_strength_set_owned(db, set_id, current_user.id)


@router.post("/", response_model=StrengthSetResponse, status_code=status.HTTP_201_CREATED)
def create_strength_set(
    set_in: StrengthSetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return strength_set_service.create_strength_set(db, current_user.id, set_in)


@router.patch("/{set_id}", response_model=StrengthSetResponse)
def update_strength_set(
    set_id: int,
    set_in: StrengthSetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    strength_set = strength_set_service.get_strength_set_owned(db, set_id, current_user.id)
    return strength_set_service.update_strength_set(db, strength_set, set_in, current_user.id)


@router.delete("/{set_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_strength_set(
    set_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    strength_set = strength_set_service.get_strength_set_owned(db, set_id, current_user.id)
    strength_set_service.delete_strength_set(db, strength_set)
