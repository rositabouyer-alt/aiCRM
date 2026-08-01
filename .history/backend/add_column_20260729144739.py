from sqlalchemy import text
from app.database import engine


def add_telegram_username_column():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='leads'
            AND column_name='telegram_username';
            """)
        )

        exists = result.fetchone()


        if exists:
            print("telegram_username already exists")
            return


        conn.execute(
            text("""
            ALTER TABLE leads
            ADD COLUMN telegram_username VARCHAR(100);
            """)
        )

        conn.commit()

        print("✅ telegram_username column added successfully")


if __name__ == "__main__":
    add_telegram_username_column()