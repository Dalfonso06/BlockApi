from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.strength_activity_detail import (
    StrengthActivityDetailCreate,
    StrengthActivityDetailResponse,
    StrengthActivityDetailUpdate,
)
from app.services import strength_activity_detail_service

router = APIRouter(prefix="/strength-activity-details", tags=["strength-activity-details"])


@router.get("/", response_model=list[StrengthActivityDetailResponse])
def list_strength_activity_details(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return strength_activity_detail_service.get_strength_activity_details_by_activity(
        db, activity_id, current_user.id
    )


@router.get("/{detail_id}", response_model=StrengthActivityDetailResponse)
def get_strength_activity_detail(
    detail_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return strength_activity_detail_service.get_strength_activity_detail_owned(db, detail_id, current_user.id)


@router.post("/", response_model=StrengthActivityDetailResponse, status_code=status.HTTP_201_CREATED)
def create_strength_activity_detail(
    detail_in: StrengthActivityDetailCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return strength_activity_detail_service.create_strength_activity_detail(db, current_user.id, detail_in)


@router.patch("/{detail_id}", response_model=StrengthActivityDetailResponse)
def update_strength_activity_detail(
    detail_id: int,
    detail_in: StrengthActivityDetailUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    detail = strength_activity_detail_service.get_strength_activity_detail_owned(db, detail_id, current_user.id)
    return strength_activity_detail_service.update_strength_activity_detail(
        db, detail, detail_in, current_user.id
    )


@router.delete("/{detail_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_strength_activity_detail(
    detail_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    detail = strength_activity_detail_service.get_strength_activity_detail_owned(db, detail_id, current_user.id)
    strength_activity_detail_service.delete_strength_activity_detail(db, detail)
