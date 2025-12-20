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
        with db_conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO decks (id, name, description, publish_status, owner_id, rating)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (self.id, self.name, self.description, self.publish_status, self.owner_id, self.rating)
            )
            db_conn.commit()

    def update(self, db_conn):
        with db_conn.cursor() as cur:
            cur.execute(
                """
                UPDATE decks 
                SET name = %s, description = %s, publish_status = %s, updated_at = %s
                WHERE id = %s
                """,
                (self.name, self.description, self.publish_status, self.updated_at, self.id)
            )
            db_conn.commit()

    def delete(self, db_conn):
        with db_conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM decks WHERE id = %s
                """,
                (self.id,)
            )
            db_conn.commit()

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
        except Exception as e:
            print(f"Error in find_explore_decks: {e}")
            return None

    @classmethod
    def find_feed_decks(cls, db_conn, user_id):
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
                    JOIN users u ON d.owner_id = u.id
                    JOIN followers f ON d.owner_id = f.following_id
                    LEFT JOIN cards c ON d.id = c.deck_id
                    WHERE d.publish_status = 'public'
                    AND f.follower_id = %s
                    GROUP BY d.id, d.name, d.description, d.rating, d.created_at, d.updated_at, u.username
                    ORDER BY d.created_at DESC, d.rating DESC
                    """,
                    (user_id,)
                )
                decks = cur.fetchall()

                return decks
        except Exception as e:
            print(f"Error in find_feed_decks: {e}")
            return None

    @classmethod
    def find_decks_by_user_id(cls, db_conn, user_id: str):
        try:
            with db_conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        d.id,
                        d.name,
                        d.description,
                        d.publish_status,
                        d.rating,
                        d.created_at,
                        d.updated_at,
                        u.username as owner,
                        COUNT(c.id) as card_count
                    FROM decks d
                    JOIN users u ON d.owner_id = u.id
                    LEFT JOIN cards c ON d.id = c.deck_id
                    WHERE d.owner_id = %s
                    GROUP BY d.id, d.name, d.description, d.publish_status, d.rating, d.created_at, d.updated_at, u.username
                    ORDER BY d.created_at DESC
                    """,
                    (user_id,)
                )
                decks = cur.fetchall()
                
                return decks
        except Exception as e:
            print(f"Error in find_decks_by_user_id: {e}")
            return None

    @classmethod
    def find_deck_by_id(cls, db_conn, id: str):
        try:
            with db_conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        d.id,
                        d.name,
                        d.description,
                        d.publish_status,
                        d.owner_id,
                        d.rating,
                        d.created_at,
                        d.updated_at,
                        u.username as owner,
                        COUNT(c.id) as card_count
                    FROM decks d
                    JOIN users u ON d.owner_id = u.id
                    LEFT JOIN cards c ON d.id = c.deck_id
                    WHERE d.id = %s
                    GROUP BY d.id, d.name, d.description, d.publish_status, d.owner_id, d.rating, d.created_at, d.updated_at, u.username
                    """,
                    (id,)
                )
                deck = cur.fetchone()
                
                return deck
        except Exception as e:
            print(f"Error in find_deck_by_id: {e}")
            return None
