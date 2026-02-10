from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserDetailsModel:
    __tablename__ = "user_details"

    id: UUID
    user_id: UUID
    about_me: str
    created_at: datetime
    updated_at: datetime

    def save(self, db_conn):
        with db_conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO user_details (id, user_id, about_me)
                    VALUES (%s, %s, %s)
                """,
                (self.id, self.user_id, self.about_me),
            )
        db_conn.commit()
