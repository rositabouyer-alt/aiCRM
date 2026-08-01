from sqlalchemy import text
from app.database import engine


def update_database():

    with engine.connect() as conn:

        try:
            conn.execute(
                text(
                    """
                    ALTER TABLE leads
                    ADD COLUMN IF NOT EXISTS telegram_username VARCHAR(100);
                    """
                )
            )

            conn.commit()

            print("✅ Database updated successfully")

        except Exception as e:
            print("❌ Database update error:")
            print(e)


if __name__ == "__main__":
    update_database()