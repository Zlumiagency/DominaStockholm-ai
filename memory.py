from database import db
from datetime import datetime


class MemoryEngine:

    def register_user(self, telegram_id, username="", first_name=""):
        existing = db.fetchone(
            "SELECT * FROM users WHERE telegram_id=?",
            (str(telegram_id),)
        )

        if existing:
            db.execute(
                """
                UPDATE users
                SET username=?,
                    first_name=?,
                    last_seen=CURRENT_TIMESTAMP
                WHERE telegram_id=?
                """,
                (
                    username,
                    first_name,
                    str(telegram_id)
                )
            )
        else:
            db.execute(
                """
                INSERT INTO users
                (telegram_id, username, first_name)
                VALUES (?, ?, ?)
                """,
                (
                    str(telegram_id),
                    username,
                    first_name
                )
            )

    def save_message(self, telegram_id, role, message):
        db.execute(
            """
            INSERT INTO conversations
            (telegram_id, role, message)
            VALUES (?, ?, ?)
            """,
            (
                str(telegram_id),
                role,
                message
            )
        )

    def get_recent_conversation(self, telegram_id, limit=20):

        rows = db.fetchall(
            """
            SELECT role, message
            FROM conversations
            WHERE telegram_id=?
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                str(telegram_id),
                limit
            )
        )

        rows.reverse()

        history = []

        for row in rows:
            history.append({
                "role": row["role"],
                "content": row["message"]
            })

        return history


memory = MemoryEngine()