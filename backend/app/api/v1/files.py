"""File management API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.kpi import KPI
from app.schemas.kpi import KPIEvidenceCreate, KPIEvidenceResponse
from app.crud.kpi_evidence import kpi_evidence_crud
from app.crud.kpi import kpi_crud
from app.services.file_service import file_service

router = APIRouter()


@router.post("/kpis/{kpi_id}/files", response_model=KPIEvidenceResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    kpi_id: int,
    file: UploadFile = File(...),
    description: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload a file as evidence for a KPI.

    **Security:**
    - File type validation (pdf, doc, docx, xls, xlsx, jpg, png)
    - File size limit: 50MB
    - UUID-based filenames
    - Ownership validation

    **Args:**
    - kpi_id: KPI ID to attach file to
    - file: File to upload
    - description: Optional file description

    **Returns:**
    - Evidence record with file metadata
    """
    # Verify KPI exists
    kpi = kpi_crud.get(db, kpi_id=kpi_id)
    if not kpi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KPI not found"
        )

    # Check permissions: only KPI owner can upload files
    if kpi.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only upload files to your own KPIs"
        )

    # Save file
    file_path, original_filename, file_size = await file_service.save_file(file)

    # Create evidence record
    evidence_in = KPIEvidenceCreate(
        file_name=original_filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=file_size,
        description=description
    )

    evidence = kpi_evidence_crud.create(
        db,
        kpi_id=kpi_id,
        evidence_in=evidence_in,
        uploaded_by=current_user.id
    )

    return evidence


@router.get("/kpis/{kpi_id}/files", response_model=List[KPIEvidenceResponse])
def list_files(
    kpi_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all files for a KPI.

    **Args:**
    - kpi_id: KPI ID

    **Returns:**
    - List of evidence records
    """
    # Verify KPI exists
    kpi = kpi_crud.get(db, kpi_id=kpi_id)
    if not kpi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KPI not found"
        )

    # Check permissions
    if current_user.role == "employee" and kpi.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own KPI files"
        )

    evidence_list = kpi_evidence_crud.get_by_kpi(db, kpi_id=kpi_id)
    return evidence_list


@router.get("/files/{evidence_id}/download")
def download_file(
    evidence_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Download a file.

    **Args:**
    - evidence_id: Evidence ID

    **Returns:**
    - File for download
    """
    # Get evidence
    evidence = kpi_evidence_crud.get(db, evidence_id=evidence_id)
    if not evidence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    # Get KPI to check permissions
    kpi = kpi_crud.get(db, kpi_id=evidence.kpi_id)
    if not kpi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated KPI not found"
        )

    # Check permissions
    if current_user.role == "employee" and kpi.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only download files from your own KPIs"
        )

    # Check if file exists
    file_path = file_service.get_file_path(evidence.file_path.split('/')[-1])
    if not file_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on disk"
        )

    return FileResponse(
        path=file_path,
        filename=evidence.file_name,
        media_type=evidence.file_type or 'application/octet-stream'
    )


@router.delete("/files/{evidence_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    evidence_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a file.

    **Security:**
    - Only file uploader or admin can delete
    - Deletes both database record and physical file

    **Args:**
    - evidence_id: Evidence ID to delete
    """
    # Get evidence
    evidence = kpi_evidence_crud.get(db, evidence_id=evidence_id)
    if not evidence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    # Check permissions: only uploader or admin can delete
    if evidence.uploaded_by != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete files you uploaded"
        )

    # Delete physical file
    file_service.delete_file(evidence.file_path)

    # Delete database record
    kpi_evidence_crud.delete(db, evidence_id=evidence_id)

    return None
