from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.endurance_activity_detail import EnduranceActivityDetail
from app.schemas.endurance_activity_detail import EnduranceActivityDetailSet
from app.services import activity_service


def get_endurance_activity_detail(db: Session, activity_id: int) -> EnduranceActivityDetail | None:
    return db.query(EnduranceActivityDetail).filter(EnduranceActivityDetail.activity_id == activity_id).first()


def get_endurance_activity_detail_required(db: Session, activity_id: int) -> EnduranceActivityDetail:
    detail = get_endurance_activity_detail(db, activity_id)

    if detail is None:
        raise NotFoundError("No endurance detail set for this activity")

    return detail


def get_endurance_activity_detail_owned(db: Session, activity_id: int, user_id: int) -> EnduranceActivityDetail:
    activity_service.get_activity_owned(db, activity_id, user_id)
    return get_endurance_activity_detail_required(db, activity_id)


def set_endurance_activity_detail(
    db: Session, activity_id: int, user_id: int, detail_in: EnduranceActivityDetailSet
) -> EnduranceActivityDetail:
    activity_service.get_activity_owned(db, activity_id, user_id)

    detail = get_endurance_activity_detail(db, activity_id)
    data = detail_in.model_dump(exclude_unset=True)

    if detail is None:
        detail = EnduranceActivityDetail(activity_id=activity_id, **data)
        db.add(detail)
    else:
        for field, value in data.items():
            setattr(detail, field, value)

    db.commit()
    db.refresh(detail)
    return detail


def delete_endurance_activity_detail(db: Session, detail: EnduranceActivityDetail) -> None:
    db.delete(detail)
    db.commit()
