from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class DeckModel:
    __tablename__ = 'decks'

    id: UUID
    name: str
    description: str
    publish_status: str
    owner_id: UUID
    rating: float
    created_at: datetime
    updated_at: datetime
