import io
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from typing import Dict, List, Optional

def generate_pdf(
    original_medication: str,
    med_info: Dict,
    recommendations: List[Dict],
    insurance: str,
    budget: Optional[float]
) -> BytesIO:
    """
    Generate a PDF report of medication recommendations.
    
    Args:
        original_medication: Name of the prescribed medication
        med_info: Dictionary with original medication information
        recommendations: List of recommendation dictionaries
        insurance: Insurance provider
        budget: Monthly budget constraint (optional)
        
    Returns:
        BytesIO object containing the generated PDF
    """
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = styles["Title"]
    heading_style = styles["Heading1"]
    subheading_style = styles["Heading2"]
    normal_style = styles["Normal"]
    
    # Create a list to store our flowables
    elements = []
    
    # Add title
    elements.append(Paragraph("MediMatch AI Recommendation Report", title_style))
    elements.append(Spacer(1, 12))
    
    # Add date
    from datetime import datetime
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", normal_style))
    elements.append(Spacer(1, 24))
    
    # Add patient information section
    elements.append(Paragraph("Patient Information", heading_style))
    elements.append(Spacer(1, 12))
    
    patient_info = [
        ["Prescribed Medication:", original_medication],
        ["Insurance Provider:", insurance]
    ]
    
    if budget:
        patient_info.append(["Monthly Budget:", f"${budget:.2f}"])
    
    patient_table = Table(patient_info, colWidths=[150, 300])
    patient_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(patient_table)
    elements.append(Spacer(1, 24))
    
    # Original medication details
    elements.append(Paragraph("Original Prescribed Medication", heading_style))
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph(f"<b>{med_info['name']}</b> ({med_info['drug_class']})", subheading_style))
    elements.append(Paragraph(f"<b>Purpose:</b> {med_info['description']}", normal_style))
    elements.append(Paragraph(f"<b>Average Monthly Cost:</b> ${med_info['avg_cost']:.2f}", normal_style))
    elements.append(Paragraph(f"<b>Common Side Effects:</b> {med_info['side_effects']}", normal_style))
    elements.append(Paragraph(f"<b>Source:</b> {med_info['source']}", normal_style))
    
    elements.append(Spacer(1, 24))
    
    # Recommended alternatives
    elements.append(Paragraph("Recommended Alternatives", heading_style))
    elements.append(Spacer(1, 12))
    
    for i, rec in enumerate(recommendations):
        elements.append(Paragraph(f"{i+1}. <b>{rec['name']}</b> - {rec['recommendation_type']}", subheading_style))
        elements.append(Paragraph(f"<b>Average Monthly Cost:</b> ${rec['avg_cost']:.2f}", normal_style))
        
        if 'savings' in rec:
            elements.append(Paragraph(f"<b>Potential Savings:</b> ${rec['savings']:.2f}/month", normal_style))
        
        elements.append(Paragraph(f"<b>Why We Recommend This:</b>", normal_style))
        elements.append(Paragraph(rec['explanation'], normal_style))
        
        if 'availability' in rec:
            elements.append(Paragraph(f"<b>Availability:</b> {rec['availability']}", normal_style))
        
        elements.append(Paragraph(f"<b>Side Effects:</b> {rec['side_effects']}", normal_style))
        elements.append(Paragraph(f"<b>Source:</b> {rec['source']}", normal_style))
        
        elements.append(Spacer(1, 12))
    
    # Educational section
    elements.append(Paragraph("Educational Information", heading_style))
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph("<b>Understanding Brand vs. Generic Medications</b>", subheading_style))
    elements.append(Paragraph("""
    Generic medications contain the same active ingredients as brand-name drugs and work the same way in the body.
    The FDA requires generic drugs to be bioequivalent to the brand-name version and manufactured under the same strict standards.
    Generics are typically 80-85% less expensive than brand-name medications.
    """, normal_style))
    
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph("<b>How to Talk to Your Doctor About Medication Costs</b>", subheading_style))
    elements.append(Paragraph("""
    1. Be honest about your financial concerns.
    2. Ask specifically about generic alternatives.
    3. Bring this report with you to your appointment.
    4. Ask about medication assistance programs.
    5. Discuss the possibility of a higher dose that can be split (only with doctor approval).
    6. Inquire about therapeutic alternatives in the same drug class.
    7. Be clear if cost might prevent you from taking your medication as prescribed.
    """, normal_style))
    
    elements.append(Spacer(1, 12))
    
    # Disclaimer
    elements.append(Paragraph("Disclaimer", heading_style))
    elements.append(Paragraph("""
    This report is for informational purposes only and is not a substitute for professional medical advice.
    Never disregard professional medical advice or delay seeking it because of something you have read in this report.
    Always consult with your healthcare provider before making any changes to your medication regimen.
    """, normal_style))
    
    # Build the PDF
    doc.build(elements)
    
    # Reset buffer position to the beginning
    buffer.seek(0)
    
    return buffer
