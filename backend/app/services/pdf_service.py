"""PDF report generation service."""

from datetime import datetime
from io import BytesIO
from typing import List, Dict, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas


class PDFReportService:
    """Service for generating PDF reports."""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Title style
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Heading1"],
                fontSize=24,
                textColor=colors.HexColor("#1e40af"),
                spaceAfter=30,
                alignment=TA_CENTER,
            )
        )

        # Subtitle style
        self.styles.add(
            ParagraphStyle(
                name="CustomSubtitle",
                parent=self.styles["Heading2"],
                fontSize=16,
                textColor=colors.HexColor("#3b82f6"),
                spaceAfter=12,
            )
        )

        # Section header
        self.styles.add(
            ParagraphStyle(
                name="SectionHeader",
                parent=self.styles["Heading3"],
                fontSize=14,
                textColor=colors.HexColor("#1f2937"),
                spaceBefore=16,
                spaceAfter=8,
                borderPadding=5,
                borderColor=colors.HexColor("#3b82f6"),
                borderWidth=0,
                leftIndent=0,
            )
        )

        # Info text
        self.styles.add(
            ParagraphStyle(
                name="InfoText",
                parent=self.styles["Normal"],
                fontSize=10,
                textColor=colors.HexColor("#6b7280"),
                alignment=TA_RIGHT,
            )
        )

    def generate_kpi_report(
        self,
        kpis: List[Dict[str, Any]],
        user_info: Dict[str, Any],
        filters: Dict[str, Any] = None,
    ) -> BytesIO:
        """
        Generate PDF report for KPIs.

        Args:
            kpis: List of KPI data dictionaries
            user_info: User information dict
            filters: Applied filters

        Returns:
            BytesIO containing PDF data
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )

        # Container for PDF elements
        story = []

        # Add header
        story.extend(self._create_header(user_info, filters))

        # Add summary statistics
        story.extend(self._create_summary_section(kpis))

        # Add KPI list
        story.extend(self._create_kpi_table(kpis))

        # Build PDF
        doc.build(story, onFirstPage=self._add_page_number, onLaterPages=self._add_page_number)

        buffer.seek(0)
        return buffer

    def _create_header(
        self, user_info: Dict[str, Any], filters: Dict[str, Any]
    ) -> List:
        """Create report header."""
        elements = []

        # Title
        title = Paragraph("KPI Performance Report", self.styles["CustomTitle"])
        elements.append(title)

        # User and date info
        generated_date = datetime.now().strftime("%B %d, %Y %H:%M")
        info_text = f"""
        <b>Generated for:</b> {user_info.get('full_name', 'N/A')}<br/>
        <b>Email:</b> {user_info.get('email', 'N/A')}<br/>
        <b>Department:</b> {user_info.get('department', 'N/A')}<br/>
        <b>Generated on:</b> {generated_date}
        """

        if filters:
            filter_parts = []
            if filters.get("year"):
                filter_parts.append(f"Year: {filters['year']}")
            if filters.get("quarter"):
                filter_parts.append(f"Quarter: {filters['quarter']}")
            if filters.get("status"):
                filter_parts.append(f"Status: {filters['status'].title()}")

            if filter_parts:
                info_text += f"<br/><b>Filters:</b> {', '.join(filter_parts)}"

        info = Paragraph(info_text, self.styles["Normal"])
        elements.append(info)
        elements.append(Spacer(1, 0.3 * inch))

        return elements

    def _create_summary_section(self, kpis: List[Dict[str, Any]]) -> List:
        """Create summary statistics section."""
        elements = []

        # Section header
        header = Paragraph("Summary Statistics", self.styles["CustomSubtitle"])
        elements.append(header)

        # Calculate statistics
        total = len(kpis)
        status_counts = {}
        total_target = 0
        total_actual = 0

        for kpi in kpis:
            status = kpi.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

            # Sum targets and actuals
            if kpi.get("target_value") is not None:
                total_target += float(kpi["target_value"])
            if kpi.get("actual_value") is not None:
                total_actual += float(kpi["actual_value"])

        # Achievement rate
        achievement_rate = (
            (total_actual / total_target * 100) if total_target > 0 else 0
        )

        # Create summary table
        summary_data = [
            ["Metric", "Value"],
            ["Total KPIs", str(total)],
            ["Draft", str(status_counts.get("draft", 0))],
            ["Submitted", str(status_counts.get("submitted", 0))],
            ["Approved", str(status_counts.get("approved", 0))],
            ["Rejected", str(status_counts.get("rejected", 0))],
            ["Total Target", f"{total_target:,.2f}"],
            ["Total Actual", f"{total_actual:,.2f}"],
            ["Achievement Rate", f"{achievement_rate:.1f}%"],
        ]

        summary_table = Table(summary_data, colWidths=[3 * inch, 2 * inch])
        summary_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3b82f6")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ]
            )
        )

        elements.append(summary_table)
        elements.append(Spacer(1, 0.4 * inch))

        return elements

    def _create_kpi_table(self, kpis: List[Dict[str, Any]]) -> List:
        """Create detailed KPI table."""
        elements = []

        # Section header
        header = Paragraph("KPI Details", self.styles["CustomSubtitle"])
        elements.append(header)

        if not kpis:
            no_data = Paragraph("No KPIs found matching the criteria.", self.styles["Normal"])
            elements.append(no_data)
            return elements

        # Table header
        table_data = [
            ["Title", "Period", "Target", "Actual", "Progress", "Status"]
        ]

        # Add KPI rows
        for kpi in kpis:
            period = f"Q{kpi.get('quarter', 'N/A')} {kpi.get('year', '')}"
            target = (
                f"{kpi.get('target_value', 0):,.2f}"
                if kpi.get("target_value") is not None
                else "N/A"
            )
            actual = (
                f"{kpi.get('actual_value', 0):,.2f}"
                if kpi.get("actual_value") is not None
                else "N/A"
            )

            # Calculate progress
            if kpi.get("target_value") and kpi.get("actual_value"):
                progress_pct = (
                    kpi["actual_value"] / kpi["target_value"] * 100
                )
                progress = f"{progress_pct:.1f}%"
            else:
                progress = "N/A"

            status = kpi.get("status", "N/A").title()

            # Wrap title in Paragraph for better text wrapping
            title_para = Paragraph(
                kpi.get("title", "Untitled")[:50], self.styles["Normal"]
            )

            table_data.append([title_para, period, target, actual, progress, status])

        # Create table
        kpi_table = Table(
            table_data,
            colWidths=[2.5 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch],
        )

        # Style the table
        kpi_table.setStyle(
            TableStyle(
                [
                    # Header row
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e40af")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    # Data rows
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                    ("ALIGN", (0, 1), (0, -1), "LEFT"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ]
            )
        )

        elements.append(kpi_table)

        return elements

    def _add_page_number(self, canvas_obj, doc):
        """Add page number to each page."""
        page_num = canvas_obj.getPageNumber()
        text = f"Page {page_num}"
        canvas_obj.saveState()
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor(colors.grey)
        canvas_obj.drawRightString(
            doc.pagesize[0] - 72, 30, text
        )
        canvas_obj.restoreState()


pdf_service = PDFReportService()
