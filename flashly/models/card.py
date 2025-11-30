from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CardModel:
    __tablename__ = 'cards'

    id: UUID
    front_text: str
    back_text: str
    difficulty: str
    times_reviewed: int
    success_rate: float
    deck_id: UUID
    created_at: datetime
    updated_at: datetime
