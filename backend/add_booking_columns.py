from sqlalchemy import text
from app.database import engine


def update_booking_table():

    columns = [
        """
        ALTER TABLE bookings
        ADD COLUMN IF NOT EXISTS service VARCHAR(255)
        """,

        """
        ALTER TABLE bookings
        ADD COLUMN IF NOT EXISTS scheduled_at TIMESTAMP WITH TIME ZONE
        """,

        """
        ALTER TABLE bookings
        ADD COLUMN IF NOT EXISTS duration_minutes INTEGER DEFAULT 30
        """,

        """
        ALTER TABLE bookings
        ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'pending'
        """,

        """
        ALTER TABLE bookings
        ADD COLUMN IF NOT EXISTS notes TEXT
        """,

        """
        ALTER TABLE bookings
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        """
    ]


    with engine.connect() as conn:

        for query in columns:
            conn.execute(text(query))

        conn.commit()


    print("✅ Booking table updated successfully")


if __name__ == "__main__":
    update_booking_table()