from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.source import SourceCreate, SourceResponse, SourceUpdate
from app.services import source_service

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("/", response_model=list[SourceResponse])
def list_sources(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return source_service.get_all_sources(db)


@router.get("/{source_id}", response_model=SourceResponse)
def get_source(source_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return source_service.get_source_required(db, source_id)


@router.post("/", response_model=SourceResponse, status_code=status.HTTP_201_CREATED)
def create_source(
    source_in: SourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return source_service.create_source(db, source_in)


@router.patch("/{source_id}", response_model=SourceResponse)
def update_source(
    source_id: int,
    source_in: SourceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    source = source_service.get_source_required(db, source_id)
    return source_service.update_source(db, source, source_in)


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_source(
    source_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    source = source_service.get_source_required(db, source_id)
    source_service.delete_source(db, source)
