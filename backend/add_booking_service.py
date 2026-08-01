from sqlalchemy import text
from app.database import engine


def add_column():

    with engine.connect() as conn:

        conn.execute(
            text("""
            ALTER TABLE bookings
            ADD COLUMN IF NOT EXISTS service VARCHAR(255);
            """)
        )

        conn.commit()


    print("✅ bookings.service column added successfully")


if __name__ == "__main__":
    add_column()