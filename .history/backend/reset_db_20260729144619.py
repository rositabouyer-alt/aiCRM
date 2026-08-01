from app.database import engine, Base
from app import models


def reset_database():

    print("Dropping existing tables...")

    with engine.connect() as conn:

        conn.execute(
            "DROP SCHEMA public CASCADE"
        )

        conn.execute(
            "CREATE SCHEMA public"
        )

        conn.commit()


    print("Creating new tables...")

    Base.metadata.create_all(
        bind=engine
    )


    print("Database reset completed successfully.")



if __name__ == "__main__":
    reset_database()