from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserModel:
    __tablename__ = 'users'

    id: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    password_hash: str
    created_at: datetime
    updated_at: datetime
