from fastapi import APIRouter, status, HTTPException
from datetime import date
from services.report_generator import report_gen
from models.report import Report


router = APIRouter()

@router.get("/{report_date}", status_code=status.HTTP_200_OK)
def get_report(report_date: date) -> Report:
    if report_date > date.today():
        raise HTTPException(status_code=400, detail="Cannot generate report for future date.") 
    return report_gen.generate(report_date)
        
