from dataclasses import dataclass
from uuid import UUID


@dataclass
class DeckCategoryModel:
    __tablename__ = "deck_categories"

    deck_id: UUID
    category_id: UUID
