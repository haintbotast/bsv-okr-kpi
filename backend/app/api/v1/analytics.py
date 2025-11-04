"""Analytics and reporting API endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.services.report_service import report_service

router = APIRouter()


@router.get("/reports/excel")
def export_excel_report(
    user_id: Optional[int] = Query(None),
    year: Optional[int] = Query(None),
    quarter: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Export KPI report to Excel."""
    # Employee can only export their own KPIs
    if current_user.role == "employee":
        user_id = current_user.id

    excel_file = report_service.generate_excel_report(
        db, user_id=user_id, year=year, quarter=quarter, status=status
    )

    filename = f"kpi_report_{year or 'all'}_{quarter or 'all'}.xlsx"

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/analytics")
def get_analytics(
    user_id: Optional[int] = Query(None),
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get analytics data for dashboards."""
    # Employee can only view their own analytics
    if current_user.role == "employee":
        user_id = current_user.id

    analytics = report_service.get_analytics_data(db, user_id=user_id, year=year)
    return analytics
