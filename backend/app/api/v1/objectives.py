"""API endpoints for objectives."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.objective import Objective
from app.schemas.objective import (
    ObjectiveCreate,
    ObjectiveUpdate,
    ObjectiveResponse,
    ObjectiveDetail,
    ObjectiveListResponse,
    ObjectiveTreeNode,
    ObjectiveStats,
    ProgressCalculation,
    ObjectiveKPILinkCreate,
    ObjectiveKPILinkResponse,
)
from app.crud.objective import objective_crud

router = APIRouter()


# CRUD Endpoints
@router.post("", response_model=ObjectiveResponse, status_code=201)
def create_objective(
    objective_in: ObjectiveCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create new objective.

    Permissions:
    - Admin: Can create objectives at any level
    - Manager: Can create division/team/individual objectives
    - Employee: Can create individual objectives only
    """
    # Permission checks
    if current_user.role == "employee" and objective_in.level != "individual":
        raise HTTPException(
            status_code=403,
            detail="Employees can only create individual-level objectives",
        )

    if current_user.role == "manager" and objective_in.level == "company":
        raise HTTPException(
            status_code=403, detail="Managers cannot create company-level objectives"
        )

    # Validate parent relationship
    if objective_in.parent_id:
        parent = objective_crud.get(db, objective_in.parent_id)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent objective not found")

        # Validate level hierarchy
        level_order = {"company": 0, "unit": 1, "division": 2, "team": 3, "individual": 4}
        if level_order[objective_in.level] <= level_order[parent.level]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid hierarchy: {objective_in.level} cannot be child of {parent.level}",
            )

    objective = objective_crud.create(
        db, obj_in=objective_in, created_by=current_user.id
    )
    return objective


@router.get("", response_model=ObjectiveListResponse)
def list_objectives(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    owner_id: Optional[int] = Query(None),
    level: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    quarter: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    List objectives with filters.

    Permissions:
    - Admin: Can see all objectives
    - Manager: Can see all objectives in their department
    - Employee: Can only see their own objectives
    """
    # Apply role-based filters
    if current_user.role == "employee":
        owner_id = current_user.id  # Force filter to own objectives
    elif current_user.role == "manager" and not owner_id:
        # If manager doesn't specify owner_id, show their department
        if not department:
            department = current_user.department

    objectives = objective_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        owner_id=owner_id,
        level=level,
        year=year,
        quarter=quarter,
        status=status,
        department=department,
    )

    # Enrich with details
    items = []
    for objective in objectives:
        detail = ObjectiveDetail.model_validate(objective)

        # Add owner name
        if objective.owner:
            detail.owner_name = objective.owner.full_name or objective.owner.username

        # Add parent title
        if objective.parent:
            detail.parent_title = objective.parent.title

        # Count children and KPIs
        detail.children_count = len(objective_crud.get_children(db, objective.id))
        detail.kpi_count = len(objective_crud.get_linked_kpis(db, objective.id))

        items.append(detail)

    # Get total count (without pagination)
    total_objectives = objective_crud.get_multi(
        db,
        skip=0,
        limit=10000,  # Large number to get all
        owner_id=owner_id,
        level=level,
        year=year,
        quarter=quarter,
        status=status,
        department=department,
    )
    total = len(total_objectives)

    # Calculate pagination
    page = (skip // limit) + 1 if limit > 0 else 1
    total_pages = (total + limit - 1) // limit if limit > 0 else 1

    return ObjectiveListResponse(
        items=items,
        total=total,
        page=page,
        page_size=limit,
        total_pages=total_pages
    )


@router.get("/{objective_id}", response_model=ObjectiveDetail)
def get_objective(
    objective_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get objective by ID with details."""
    objective = objective_crud.get(db, objective_id)
    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")

    # Permission check
    if current_user.role == "employee" and objective.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this objective"
        )

    # Build detail response
    detail = ObjectiveDetail.model_validate(objective)

    # Add owner name
    if objective.owner:
        detail.owner_name = objective.owner.full_name or objective.owner.username

    # Add parent title
    if objective.parent:
        detail.parent_title = objective.parent.title

    # Count children and KPIs
    detail.children_count = len(objective_crud.get_children(db, objective_id))
    detail.kpi_count = len(objective_crud.get_linked_kpis(db, objective_id))

    return detail


@router.put("/{objective_id}", response_model=ObjectiveResponse)
def update_objective(
    objective_id: int,
    objective_in: ObjectiveUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update objective.

    Permissions:
    - Admin: Can update any objective
    - Manager: Can update objectives in their department
    - Employee: Can only update their own objectives
    """
    objective = objective_crud.get(db, objective_id)
    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")

    # Permission checks
    if current_user.role == "employee" and objective.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this objective"
        )

    if (
        current_user.role == "manager"
        and objective.department != current_user.department
        and objective.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=403, detail="Not authorized to update this objective"
        )

    # Validate parent change if provided
    if objective_in.parent_id is not None and objective_in.parent_id != objective.parent_id:
        if objective_in.parent_id:
            parent = objective_crud.get(db, objective_in.parent_id)
            if not parent:
                raise HTTPException(status_code=404, detail="Parent objective not found")

    updated_objective = objective_crud.update(db, db_obj=objective, obj_in=objective_in)
    return updated_objective


@router.delete("/{objective_id}", status_code=204)
def delete_objective(
    objective_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete objective.

    Permissions:
    - Admin: Can delete any objective
    - Manager: Can delete objectives they created
    - Employee: Can delete their own objectives
    """
    objective = objective_crud.get(db, objective_id)
    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")

    # Permission checks
    if current_user.role != "admin":
        if current_user.role == "employee" and objective.owner_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Not authorized to delete this objective"
            )
        if (
            current_user.role == "manager"
            and objective.created_by != current_user.id
            and objective.owner_id != current_user.id
        ):
            raise HTTPException(
                status_code=403, detail="Not authorized to delete this objective"
            )

    objective_crud.delete(db, objective_id=objective_id)
    return None


# Hierarchy Endpoints
@router.get("/{objective_id}/children", response_model=List[ObjectiveResponse])
def get_objective_children(
    objective_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get direct children of an objective."""
    objective = objective_crud.get(db, objective_id)
    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")

    children = objective_crud.get_children(db, objective_id)
    return children


@router.get("/{objective_id}/ancestors", response_model=List[ObjectiveResponse])
def get_objective_ancestors(
    objective_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get ancestor chain (parent hierarchy) of an objective."""
    objective = objective_crud.get(db, objective_id)
    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")

    ancestors = objective_crud.get_ancestors(db, objective_id)
    return ancestors


@router.get("/tree/view", response_model=List[ObjectiveTreeNode])
def get_objective_tree(
    root_id: Optional[int] = Query(None, description="Root objective ID (optional)"),
    year: Optional[int] = Query(None, description="Filter by year"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get objective tree structure.

    If root_id provided, returns subtree from that root.
    If root_id is None, returns all top-level objectives.
    """
    # Get tree structure
    tree = objective_crud.get_tree(db, root_id)

    # Convert to tree node format
    def build_tree_node(obj: Objective) -> ObjectiveTreeNode:
        node = ObjectiveTreeNode(
            id=obj.id,
            title=obj.title,
            level=obj.level,
            progress_percentage=obj.progress_percentage,
            status=obj.status,
            owner_id=obj.owner_id,
            owner_name=obj.owner.full_name if obj.owner else None,
            children=[build_tree_node(child) for child in (obj.children or [])],
        )
        return node

    if isinstance(tree, list):
        return [build_tree_node(obj) for obj in tree]
    else:
        return [build_tree_node(tree)]


@router.post("/{objective_id}/move", response_model=ObjectiveResponse)
def move_objective(
    objective_id: int,
    new_parent_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Move objective to a different parent.

    Admin only.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Only admins can move objectives"
        )

    try:
        objective = objective_crud.move(
            db, objective_id=objective_id, new_parent_id=new_parent_id
        )
        if not objective:
            raise HTTPException(status_code=404, detail="Objective not found")
        return objective
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# KPI Linking Endpoints
@router.post("/{objective_id}/kpis", response_model=ObjectiveKPILinkResponse, status_code=201)
def link_kpi_to_objective(
    objective_id: int,
    link_in: ObjectiveKPILinkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Link a KPI to an objective."""
    objective = objective_crud.get(db, objective_id)
    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")

    # Check permission
    if current_user.role == "employee" and objective.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to modify this objective"
        )

    link = objective_crud.link_kpi(
        db, objective_id=objective_id, kpi_id=link_in.kpi_id, weight=link_in.weight
    )
    return link


@router.delete("/{objective_id}/kpis/{kpi_id}", status_code=204)
def unlink_kpi_from_objective(
    objective_id: int,
    kpi_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Unlink a KPI from an objective."""
    objective = objective_crud.get(db, objective_id)
    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")

    # Check permission
    if current_user.role == "employee" and objective.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to modify this objective"
        )

    success = objective_crud.unlink_kpi(db, objective_id=objective_id, kpi_id=kpi_id)
    if not success:
        raise HTTPException(status_code=404, detail="Link not found")

    return None


@router.get("/{objective_id}/kpis")
def get_objective_kpis(
    objective_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get all KPIs linked to an objective."""
    objective = objective_crud.get(db, objective_id)
    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")

    kpis = objective_crud.get_linked_kpis(db, objective_id)
    return kpis


# Progress Endpoints
@router.get("/{objective_id}/progress", response_model=ProgressCalculation)
def get_objective_progress(
    objective_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Calculate and return objective progress."""
    objective = objective_crud.get(db, objective_id)
    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")

    progress = objective_crud.calculate_progress(db, objective_id)
    children = objective_crud.get_children(db, objective_id)
    kpis = objective_crud.get_linked_kpis(db, objective_id)

    # Determine calculation method
    method = "manual"
    if children:
        method = "children"
    elif kpis:
        method = "kpis"

    return ProgressCalculation(
        objective_id=objective_id,
        progress_percentage=progress,
        calculation_method=method,
        child_count=len(children),
        kpi_count=len(kpis),
        last_calculated=objective.updated_at,
    )


@router.post("/{objective_id}/recalculate", response_model=ObjectiveResponse)
def recalculate_objective_progress(
    objective_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Manually trigger progress recalculation (cascades to parents)."""
    objective = objective_crud.get(db, objective_id)
    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")

    updated_objective = objective_crud.recalculate_progress(db, objective_id)
    return updated_objective


# Statistics Endpoint
@router.get("/stats/summary", response_model=ObjectiveStats)
def get_objectives_stats(
    owner_id: Optional[int] = Query(None),
    year: Optional[int] = Query(None),
    department: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get objectives statistics."""
    # Apply role-based filters
    filters = {}
    if owner_id:
        filters["owner_id"] = owner_id
    if year:
        filters["year"] = year
    if department:
        filters["department"] = department

    # Force filters for employees
    if current_user.role == "employee":
        filters["owner_id"] = current_user.id

    stats = objective_crud.get_stats(db, **filters)
    return ObjectiveStats(**stats)
