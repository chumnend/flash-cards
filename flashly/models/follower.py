from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class FollowerModel:
    __tablename__ = 'followers'

    id: UUID
    follower_id: UUID
    following_id: UUID
    created_at: datetime
