from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.endurance_activity_detail import EnduranceActivityDetailResponse, EnduranceActivityDetailSet
from app.services import endurance_activity_detail_service

router = APIRouter(prefix="/endurance-activity-details", tags=["endurance-activity-details"])


@router.get("/{activity_id}", response_model=EnduranceActivityDetailResponse)
def get_endurance_activity_detail(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return endurance_activity_detail_service.get_endurance_activity_detail_owned(db, activity_id, current_user.id)


@router.put("/{activity_id}", response_model=EnduranceActivityDetailResponse)
def set_endurance_activity_detail(
    activity_id: int,
    detail_in: EnduranceActivityDetailSet,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return endurance_activity_detail_service.set_endurance_activity_detail(
        db, activity_id, current_user.id, detail_in
    )


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_endurance_activity_detail(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    detail = endurance_activity_detail_service.get_endurance_activity_detail_owned(db, activity_id, current_user.id)
    endurance_activity_detail_service.delete_endurance_activity_detail(db, detail)
