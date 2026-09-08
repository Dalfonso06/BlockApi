from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.training_block import TrainingBlockCreate, TrainingBlockResponse, TrainingBlockUpdate
from app.services import training_block_service

router = APIRouter(prefix="/training-blocks", tags=["training-blocks"])

# Unlike GET /users/{id}, these endpoints enforce ownership: training data is
# private per-user, with no analogous "public directory" use case.


@router.get("/", response_model=list[TrainingBlockResponse])
def list_training_blocks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return training_block_service.get_training_blocks_by_user(db, current_user.id)


@router.get("/{block_id}", response_model=TrainingBlockResponse)
def get_training_block(block_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return training_block_service.get_training_block_owned(db, block_id, current_user.id)


@router.post("/", response_model=TrainingBlockResponse, status_code=status.HTTP_201_CREATED)
def create_training_block(
    block_in: TrainingBlockCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return training_block_service.create_training_block(db, current_user.id, block_in)


@router.patch("/{block_id}", response_model=TrainingBlockResponse)
def update_training_block(
    block_id: int,
    block_in: TrainingBlockUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    block = training_block_service.get_training_block_owned(db, block_id, current_user.id)
    return training_block_service.update_training_block(db, block, block_in)


@router.delete("/{block_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_training_block(
    block_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    block = training_block_service.get_training_block_owned(db, block_id, current_user.id)
    training_block_service.delete_training_block(db, block)
