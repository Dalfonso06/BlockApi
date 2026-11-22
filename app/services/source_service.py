from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.source import Source
from app.schemas.source import SourceCreate, SourceUpdate


def get_all_sources(db: Session) -> list[Source]:
    return db.query(Source).all()


def get_source_by_id(db: Session, source_id: int) -> Source | None:
    return db.query(Source).filter(Source.id == source_id).first()


def get_source_required(db: Session, source_id: int) -> Source:
    source = get_source_by_id(db, source_id)

    if source is None:
        raise NotFoundError("Source not found")

    return source


def create_source(db: Session, source_in: SourceCreate) -> Source:
    source = Source(**source_in.model_dump())
    db.add(source)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("A source with this key already exists")

    db.refresh(source)
    return source


def update_source(db: Session, source: Source, source_in: SourceUpdate) -> Source:
    data = source_in.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(source, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("A source with this key already exists")

    db.refresh(source)
    return source


def delete_source(db: Session, source: Source) -> None:
    db.delete(source)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("Cannot delete a source that is still referenced by existing activities")
