from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CategoryModel:
    __tablename__ = "categories"

    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
