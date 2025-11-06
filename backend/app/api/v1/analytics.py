"""Analytics and reporting API endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.kpi import KPI
from app.services.report_service import report_service
from app.services.pdf_service import pdf_service
from app.crud.user import user as user_crud
from app.crud.kpi import kpi_crud

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


@router.get("/reports/pdf")
def export_pdf_report(
    user_id: Optional[int] = Query(None),
    year: Optional[int] = Query(None),
    quarter: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Export KPI report to PDF.

    Generates a professional PDF report with:
    - User information and filters
    - Summary statistics
    - Detailed KPI table
    - Page numbers
    """
    # Employee can only export their own KPIs
    if current_user.role == "employee":
        user_id = current_user.id

    # Get user info for report header
    if user_id:
        target_user = user_crud.get(db, user_id=user_id)
    else:
        target_user = current_user

    user_info = {
        "full_name": target_user.full_name or target_user.username,
        "email": target_user.email,
        "department": target_user.department or "N/A",
        "role": target_user.role,
    }

    # Get KPIs
    kpis_query = db.query(KPI)

    if user_id:
        kpis_query = kpis_query.filter(KPI.user_id == user_id)

    if year:
        kpis_query = kpis_query.filter(KPI.year == year)

    if quarter:
        kpis_query = kpis_query.filter(KPI.quarter == quarter)

    if status:
        kpis_query = kpis_query.filter(KPI.status == status)

    kpis = kpis_query.all()

    # Convert KPIs to dict format
    kpis_data = [
        {
            "title": kpi.title,
            "description": kpi.description,
            "year": kpi.year,
            "quarter": kpi.quarter,
            "target_value": kpi.target_value,
            "actual_value": kpi.actual_value,
            "unit": kpi.unit,
            "status": kpi.status,
            "category": kpi.category,
        }
        for kpi in kpis
    ]

    # Prepare filters dict
    filters = {}
    if year:
        filters["year"] = year
    if quarter:
        filters["quarter"] = quarter
    if status:
        filters["status"] = status

    # Generate PDF
    pdf_buffer = pdf_service.generate_kpi_report(
        kpis=kpis_data, user_info=user_info, filters=filters
    )

    filename = f"kpi_report_{year or 'all'}_{quarter or 'all'}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
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
