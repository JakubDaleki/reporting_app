from fastapi import APIRouter, status
from datetime import date

router = APIRouter()

@router.get("/{report_date}", status_code=status.HTTP_200_OK)
def get_report(report_date: date):
    return {"Status": "Success", "Date": report_date}
