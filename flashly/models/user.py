from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional

import bcrypt

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

    def set_password(self, password: str):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        self.password_hash = hashed_password.decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), expected_hash)
        return False
    
    def save(self, db_conn):
        with db_conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (id, first_name, last_name, username, email, password_hash) 
                   VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (str(self.id), self.first_name, self.last_name, self.username, self.email, self.password_hash)
            )
        db_conn.commit()
    
    @classmethod
    def find_by_email(cls, db_conn, email: str) -> Optional['UserModel']:
        with db_conn.cursor() as cur:
            cur.execute(
                "SELECT id, first_name, last_name, username, email, password_hash, created_at, updated_at FROM users WHERE email = %s",
                (email,)
            )
            record = cur.fetchone()
            if record:
                return cls(
                    id=UUID(record[0]),
                    first_name=record[1],
                    last_name=record[2],
                    username=record[3],
                    email=record[4],
                    password_hash=record[5],
                    created_at=record[6],
                    updated_at=record[7]
                )
        return None

    @classmethod
    def find_by_username(cls, db_conn, username: str):
        with db_conn.cursor() as cur:
            cur.execute(
                "SELECT id, first_name, last_name, username, email, password_hash, created_at, updated_at FROM users WHERE username = %s",
                (username,)
            )
            record = cur.fetchone()
            if record:
                return cls(
                    id=UUID(record[0]),
                    first_name=record[1],
                    last_name=record[2],
                    username=record[3],
                    email=record[4],
                    password_hash=record[5],
                    created_at=record[6],
                    updated_at=record[7]
                )
        return None
