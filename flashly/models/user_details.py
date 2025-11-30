from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserDetailsModel:
    __tablename__ = 'user_details'

    id: UUID
    user_id: UUID
    about_me: str
    created_at: datetime
    updated_at: datetime
