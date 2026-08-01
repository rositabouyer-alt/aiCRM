from sqlalchemy import text
from app.database import engine


def update_database():

    with engine.connect() as conn:

        conn.execute(
            text(
                """
                ALTER TABLE conversations
                ADD COLUMN IF NOT EXISTS status VARCHAR(50)
                DEFAULT 'open';
                """
            )
        )

        conn.commit()


    print("✅ Conversation table updated successfully")


if __name__ == "__main__":
    update_database()