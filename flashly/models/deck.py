from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class DeckModel:
    __tablename__ = "decks"

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
                (
                    self.id,
                    self.name,
                    self.description,
                    self.publish_status,
                    self.owner_id,
                    self.rating,
                ),
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
                (
                    self.name,
                    self.description,
                    self.publish_status,
                    self.updated_at,
                    self.id,
                ),
            )
            db_conn.commit()

    def delete(self, db_conn):
        with db_conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM decks WHERE id = %s
                """,
                (self.id,),
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
                    (user_id,),
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
                    (user_id,),
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
                    (id,),
                )
                deck = cur.fetchone()

                return deck
        except Exception as e:
            print(f"Error in find_deck_by_id: {e}")
            return None


def serialize_single_deck_tuple(deck_tuple):
    """
    Sérialise un tuple de données de deck en format JSON.
    Gère différents formats de tuples selon la requête SQL.
    """
    if len(deck_tuple) == 8:
        # Format pour explore_decks et feed_decks (sans publish_status et owner_id)
        return {
            "id": str(deck_tuple[0]),
            "name": deck_tuple[1],
            "description": deck_tuple[2],
            "rating": float(deck_tuple[3]),
            "created_at": deck_tuple[4].isoformat() if deck_tuple[4] else None,
            "updated_at": deck_tuple[5].isoformat() if deck_tuple[5] else None,
            "owner": deck_tuple[6],
            "card_count": int(deck_tuple[7]),
        }
    elif len(deck_tuple) == 9:
        # Format pour find_decks_by_user_id (avec publish_status)
        return {
            "id": str(deck_tuple[0]),
            "name": deck_tuple[1],
            "description": deck_tuple[2],
            "publish_status": deck_tuple[3],
            "rating": float(deck_tuple[4]),
            "created_at": deck_tuple[5].isoformat() if deck_tuple[5] else None,
            "updated_at": deck_tuple[6].isoformat() if deck_tuple[6] else None,
            "owner": deck_tuple[7],
            "card_count": int(deck_tuple[8]),
        }
    elif len(deck_tuple) == 10:
        # Format pour find_deck_by_id (avec publish_status et owner_id)
        return {
            "id": str(deck_tuple[0]),
            "name": deck_tuple[1],
            "description": deck_tuple[2],
            "publish_status": deck_tuple[3],
            "owner_id": str(deck_tuple[4]),
            "rating": float(deck_tuple[5]),
            "created_at": deck_tuple[6].isoformat() if deck_tuple[6] else None,
            "updated_at": deck_tuple[7].isoformat() if deck_tuple[7] else None,
            "owner": deck_tuple[8],
            "card_count": int(deck_tuple[9]),
        }
    else:
        # Fallback pour des formats non reconnus
        return deck_tuple


def serialize_deck_data(deck_data):
    """
    Sérialise les données de deck(s) en format JSON avec les champs comme clés.
    Peut accepter un seul deck ou une liste de decks.
    """
    if isinstance(deck_data, DeckModel):
        # Si c'est une instance de DeckModel
        return {
            "id": str(deck_data.id),
            "name": deck_data.name,
            "description": deck_data.description,
            "publish_status": deck_data.publish_status,
            "owner_id": str(deck_data.owner_id),
            "rating": float(deck_data.rating),
            "created_at": (deck_data.created_at.isoformat() if deck_data.created_at else None),
            "updated_at": (deck_data.updated_at.isoformat() if deck_data.updated_at else None),
        }
    elif isinstance(deck_data, (list, tuple)) and deck_data:
        if isinstance(deck_data[0], (list, tuple)):
            # Liste de tuples (résultats de requêtes SQL)
            return [serialize_single_deck_tuple(deck) for deck in deck_data]
        else:
            # Tuple unique (résultat d'une requête SQL)
            return serialize_single_deck_tuple(deck_data)
    else:
        return deck_data
