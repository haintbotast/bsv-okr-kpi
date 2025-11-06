"""KPI related models."""

from sqlalchemy import Boolean, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class KPITemplate(Base):
    """KPI template model."""

    __tablename__ = "kpi_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=True, index=True)
    role = Column(String(20), nullable=True, index=True)
    measurement_method = Column(String(50), nullable=True)
    target_type = Column(String(50), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    creator = relationship("User", back_populates="templates")
    kpis = relationship("KPI", back_populates="template")

    def __repr__(self):
        return f"<KPITemplate {self.name}>"


class KPI(Base):
    """Main KPI model."""

    __tablename__ = "kpis"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    template_id = Column(Integer, ForeignKey("kpi_templates.id", ondelete="SET NULL"), nullable=True)
    year = Column(Integer, nullable=False, index=True)
    quarter = Column(String(10), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=True)
    target_value = Column(String(100), nullable=True)
    current_value = Column(String(100), nullable=True)
    progress_percentage = Column(Float, nullable=True)
    measurement_method = Column(String(50), nullable=True)
    status = Column(String(20), default="draft", nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    submitted_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    approved_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    user = relationship("User", back_populates="kpis", foreign_keys=[user_id])
    approver = relationship("User", back_populates="approved_kpis", foreign_keys=[approved_by])
    template = relationship("KPITemplate", back_populates="kpis")
    evidence = relationship("KPIEvidence", back_populates="kpi", cascade="all, delete-orphan")
    comments = relationship("KPIComment", back_populates="kpi", cascade="all, delete-orphan")
    history = relationship("KPIHistory", back_populates="kpi", cascade="all, delete-orphan")
    objective_links = relationship("ObjectiveKPILink", back_populates="kpi", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<KPI {self.title} - {self.year} {self.quarter}>"


class KPIEvidence(Base):
    """KPI evidence/file attachments model."""

    __tablename__ = "kpi_evidence"

    id = Column(Integer, primary_key=True, index=True)
    kpi_id = Column(Integer, ForeignKey("kpis.id", ondelete="CASCADE"), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(100), nullable=True)
    file_size = Column(Integer, nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    uploaded_at = Column(DateTime, server_default=func.now(), nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    kpi = relationship("KPI", back_populates="evidence")
    uploader = relationship("User", back_populates="uploaded_files")

    def __repr__(self):
        return f"<KPIEvidence {self.file_name}>"


class KPIComment(Base):
    """KPI comments model."""

    __tablename__ = "kpi_comments"

    id = Column(Integer, primary_key=True, index=True)
    kpi_id = Column(Integer, ForeignKey("kpis.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    kpi = relationship("KPI", back_populates="comments")
    user = relationship("User", back_populates="comments")

    def __repr__(self):
        return f"<KPIComment on KPI {self.kpi_id}>"


class KPIHistory(Base):
    """KPI change history/audit trail model."""

    __tablename__ = "kpi_history"

    id = Column(Integer, primary_key=True, index=True)
    kpi_id = Column(Integer, ForeignKey("kpis.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    action = Column(String(50), nullable=False)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)

    # Relationships
    kpi = relationship("KPI", back_populates="history")

    def __repr__(self):
        return f"<KPIHistory {self.action} on KPI {self.kpi_id}>"
