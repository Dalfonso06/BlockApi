from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.training_block import TrainingBlock
from app.schemas.training_block import TrainingBlockCreate, TrainingBlockUpdate


def get_training_block_by_id(db: Session, block_id: int) -> TrainingBlock | None:
    return db.query(TrainingBlock).filter(TrainingBlock.id == block_id).first()


def get_training_block_owned(db: Session, block_id: int, user_id: int) -> TrainingBlock:
    block = get_training_block_by_id(db, block_id)

    if block is None:
        raise NotFoundError("Training block not found")

    if block.user_id != user_id:
        raise PermissionDeniedError("Not authorized to access this training block")

    return block


def get_training_blocks_by_user(db: Session, user_id: int) -> list[TrainingBlock]:
    return db.query(TrainingBlock).filter(TrainingBlock.user_id == user_id).all()


def create_training_block(db: Session, user_id: int, block_in: TrainingBlockCreate) -> TrainingBlock:
    block = TrainingBlock(user_id=user_id, **block_in.model_dump())
    db.add(block)
    db.commit()
    db.refresh(block)
    return block


def update_training_block(db: Session, block: TrainingBlock, block_in: TrainingBlockUpdate) -> TrainingBlock:
    data = block_in.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(block, field, value)

    db.commit()
    db.refresh(block)
    return block


def delete_training_block(db: Session, block: TrainingBlock) -> None:
    db.delete(block)
    db.commit()
