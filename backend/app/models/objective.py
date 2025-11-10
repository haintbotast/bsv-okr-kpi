"""Objective model for OKR system."""

from sqlalchemy import Column, Integer, String, Text, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Objective(Base):
    """
    Objective model for OKR hierarchical structure.

    Supports 5-level hierarchy:
    - Level 0: Company goals (parent_id = NULL)
    - Level 1: Unit objectives
    - Level 2: Division objectives
    - Level 3: Team objectives
    - Level 4: Individual objectives
    """
    __tablename__ = "objectives"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    # Hierarchy
    parent_id = Column(Integer, ForeignKey("objectives.id", ondelete="CASCADE"), nullable=True, index=True)
    level = Column(String(20), nullable=False, index=True)  # 'company', 'unit', 'division', 'team', 'individual'

    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    department = Column(String(100), nullable=True)

    # Time period
    year = Column(Integer, nullable=False, index=True)
    quarter = Column(String(10), nullable=True, index=True)  # 'Q1', 'Q2', 'Q3', 'Q4', 'H1', 'H2', or NULL for annual
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    # Progress
    status = Column(String(20), nullable=False, default="active", index=True)  # active, completed, abandoned, on_hold
    progress_percentage = Column(Float, nullable=False, default=0.0)
    is_featured = Column(Integer, nullable=False, default=0)  # 0 = not featured, 1 = featured (using Integer for SQLite boolean)

    # Metadata
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=False)

    # Relationships
    parent = relationship("Objective", remote_side=[id], backref="children")
    owner = relationship("User", foreign_keys=[owner_id], backref="owned_objectives")
    creator = relationship("User", foreign_keys=[created_by], backref="created_objectives")
    kpi_links = relationship("ObjectiveKPILink", back_populates="objective", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Objective(id={self.id}, title='{self.title}', level='{self.level}')>"


class ObjectiveKPILink(Base):
    """
    Many-to-many relationship between objectives and KPIs.

    Allows a KPI to contribute to multiple objectives with different weights.
    """
    __tablename__ = "objective_kpi_links"

    id = Column(Integer, primary_key=True, index=True)
    objective_id = Column(Integer, ForeignKey("objectives.id", ondelete="CASCADE"), nullable=False, index=True)
    kpi_id = Column(Integer, ForeignKey("kpis.id", ondelete="CASCADE"), nullable=False, index=True)
    weight = Column(Float, nullable=False, default=1.0)  # 0.0 - 1.0, how much this KPI contributes to objective
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    objective = relationship("Objective", back_populates="kpi_links")
    kpi = relationship("KPI", back_populates="objective_links")

    def __repr__(self):
        return f"<ObjectiveKPILink(objective_id={self.objective_id}, kpi_id={self.kpi_id}, weight={self.weight})>"
