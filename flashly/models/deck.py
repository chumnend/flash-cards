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

    def save(self, db_conn):
        pass

    def delete(self, db_conn):
        pass

    @classmethod
    def find_explore_decks(cls, db_conn):
        try:
            with db_conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        d.id,
                        d.name,
                        d.description,
                        d.rating,
                        d.created_at,
                        d.updated_at,
                        u.username as owner,
                        COUNT(c.id) as card_count
                    FROM decks d
                    JOIN users u on d.owner_id = u.id
                    LEFT JOIN cards c ON d.id = c.deck_id
                    WHERE d.publish_status = 'public'
                    GROUP BY d.id, d.name, d.description, d.rating, d.created_at, d.updated_at, u.username
                    ORDER BY d.rating DESC, d.created_at DESC
                    """
                )
                decks = cur.fetchall()

                return decks
        except:
            return None

    @classmethod
    def find_feed_decks(cls, db_conn):
        pass

    @classmethod
    def find_decks_by_user_id(cls, db_conn, user_id: str):
        pass

    @classmethod
    def find_deck_by_id(cls, db_conn, id: str):
        pass
