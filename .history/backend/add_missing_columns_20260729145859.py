from app.database import engine
from sqlalchemy import text


def update_database():

    with engine.connect() as conn:

        print("Updating database...")

        # Add telegram_username to leads
        conn.execute(text("""
            ALTER TABLE leads
            ADD COLUMN IF NOT EXISTS telegram_username VARCHAR(100);
        """))


        # Add service to bookings
        conn.execute(text("""
            ALTER TABLE bookings
            ADD COLUMN IF NOT EXISTS service VARCHAR(255);
        """))


        conn.commit()


    print("✅ Database updated successfully")


if __name__ == "__main__":
    update_database()