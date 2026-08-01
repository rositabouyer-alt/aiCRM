from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/api/appointments",
    tags=["appointments"]
)


@router.post("", response_model=schemas.AppointmentResponse)
def create_appointment(
    apt: schemas.AppointmentBase,
    db: Session = Depends(get_db)
):
    db_apt = models.Appointment(**apt.dict())

    db.add(db_apt)
    db.commit()
    db.refresh(db_apt)

    return db_apt


@router.get("", response_model=list[schemas.AppointmentResponse])
def get_appointments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return (
        db.query(models.Appointment)
        .offset(skip)
        .limit(limit)
        .all()
    )