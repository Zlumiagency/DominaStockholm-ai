from database import db
import re


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

        self.learn_memory(telegram_id, message)

    def learn_memory(self, telegram_id, message):

        text = message.lower()

        patterns = [
            (r"jag heter (.+)", "name"),
            (r"mitt namn är (.+)", "name"),
            (r"min favoritfärg är (.+)", "favorite_color"),
            (r"jag bor i (.+)", "city"),
            (r"jag kommer från (.+)", "country"),
            (r"jag gillar (.+)", "likes")
        ]

        for pattern, category in patterns:

            match = re.search(pattern, text)

            if match:

                value = match.group(1).strip()

                existing = db.fetchone(
                    """
                    SELECT id
                    FROM memories
                    WHERE telegram_id=?
                    AND category=?
                    """,
                    (
                        str(telegram_id),
                        category
                    )
                )

                if existing:

                    db.execute(
                        """
                        UPDATE memories
                        SET memory=?,
                            last_used=CURRENT_TIMESTAMP
                        WHERE id=?
                        """,
                        (
                            value,
                            existing["id"]
                        )
                    )

                else:

                    db.execute(
                        """
                        INSERT INTO memories
                        (telegram_id, memory, category)
                        VALUES (?, ?, ?)
                        """,
                        (
                            str(telegram_id),
                            value,
                            category
                        )
                    )

    def get_memories(self, telegram_id):

        rows = db.fetchall(
            """
            SELECT category, memory
            FROM memories
            WHERE telegram_id=?
            ORDER BY importance DESC
            """,
            (
                str(telegram_id),
            )
        )

        if not rows:
            return ""

        text = "Known facts about the user:\n"

        for row in rows:
            text += f"- {row['category']}: {row['memory']}\n"

        return text

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