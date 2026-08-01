from app.database import engine, Base
from app import models


def reset_database():

    print("Dropping existing tables...")

    Base.metadata.drop_all(
        bind=engine
    )


    print("Creating new tables...")

    Base.metadata.create_all(
        bind=engine
    )


    print("Database reset completed successfully!")


if __name__ == "__main__":
    reset_database()