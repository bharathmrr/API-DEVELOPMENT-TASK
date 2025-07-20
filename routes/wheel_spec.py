from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/forms/wheel-specifications", response_model=schemas.WheelSpecResponse)
def create_wheel_spec(data: schemas.WheelSpecCreate, db: Session = Depends(get_db)):
    fields = data.fields
    wheel = models.WheelSpecification(
        formNumber=data.formNumber,
        submittedBy=data.submittedBy,
        submittedDate=data.submittedDate,
        **fields.dict()
    )
    db.add(wheel)
    db.commit()
    db.refresh(wheel)

    return {
        "success": True,
        "message": "Wheel specification submitted successfully.",
        "data": {
            "formNumber": wheel.formNumber,
            "submittedBy": wheel.submittedBy,
            "submittedDate": wheel.submittedDate,
            "status": "Saved"
        }
    }

@router.get("/api/forms/wheel-specifications")
def get_filtered_specs(
    formNumber: str = Query(...),
    submittedBy: str = Query(...),
    submittedDate: str = Query(...),
    db: Session = Depends(get_db)
):
    records = db.query(models.WheelSpecification).filter_by(
        formNumber=formNumber,
        submittedBy=submittedBy,
        submittedDate=submittedDate
    ).all()

    return {
        "success": True,
        "message": "Filtered wheel specification forms fetched successfully.",
        "data": [r.__dict__ for r in records]
    }
