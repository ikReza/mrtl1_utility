import streamlit as st
import pandas as pd
from datetime import datetime, date
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="Site Visit Progress Report",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem;
        margin-top: 1rem;
    }
    
    .stSelectbox > div > div {
        background-color: white;
        border: 2px solid #e1e5e9;
        border-radius: 10px;
    }
    
    .stTextInput > div > div > input {
        background-color: white;
        border: 2px solid #e1e5e9;
        border-radius: 10px;
        padding: 10px;
    }
    
    .stTextArea > div > div > textarea {
        background-color: white;
        border: 2px solid #e1e5e9;
        border-radius: 10px;
        padding: 10px;
    }
    
    .stDateInput > div > div > input {
        background-color: white;
        border: 2px solid #e1e5e9;
        border-radius: 10px;
    }
    
    .stNumberInput > div > div > input {
        background-color: white;
        border: 2px solid #e1e5e9;
        border-radius: 10px;
    }
    
    .section-header {
        background: linear-gradient(90deg, #3498db, #2980b9);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0 10px 0;
        font-weight: bold;
        text-align: center;
    }
    
    .report-header {
        text-align: center;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #3498db;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def create_pdf_report(report_data, images):
    """Create PDF report with all the collected data"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        alignment=TA_CENTER,
        spaceAfter=15
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=11,
        textColor=colors.HexColor('#34495e'),
        spaceBefore=8,
        spaceAfter=5,
        leftIndent=0,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#2c3e50'),
        leftIndent=0
    )
    
    small_style = ParagraphStyle(
        'SmallStyle',
        parent=styles['Normal'],
        fontSize=7,
        textColor=colors.HexColor('#2c3e50'),
        leftIndent=0
    )
    
    story = []
    
    # Header
    story.append(Paragraph("DAILY CONSTRUCTION REPORT", title_style))
    story.append(Spacer(1, 10))
    
    # Basic Information Table (like in your image)
    basic_info_data = [
        ['Daily Report No:', '', 'Date:', report_data['report_date'].strftime('%B %d, %Y')],
        ['Contractor:', report_data['contractor_name'], 'Project No:', ''],
        ['Project Name:', report_data['project_name'], '', ''],
    ]
    
    basic_table = Table(basic_info_data, colWidths=[1.2*inch, 2.3*inch, 1*inch, 2*inch])
    basic_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(basic_table)
    story.append(Spacer(1, 10))
    
    # Weather and Site Conditions Table
    weather_data = [
        ['Weather:', '', 'Site Conditions:', '', 'Day:'],
        ['☐ Clear', '☐ Windy', '☐ Clear', '☐ Dusty', '☐ Monday   ☐ Thursday'],
        ['☐ Cool', '☐ Overcast', '☐ Dusty', '☐ Dry', '☐ Tuesday   ☐ Friday'],
        ['☐ Fog', '☐ Warm', '☐ Muddy', '', '☐ Wednesday'],
    ]
    
    # Mark selected weather condition
    weather_condition = report_data['weather_condition'].lower()
    if 'sunny' in weather_condition or 'clear' in weather_condition:
        weather_data[1][0] = '☑ Clear'
    elif 'cool' in weather_condition:
        weather_data[2][0] = '☑ Cool'
    elif 'fog' in weather_condition:
        weather_data[3][0] = '☑ Fog'
    elif 'windy' in weather_condition:
        weather_data[1][1] = '☑ Windy'
    elif 'overcast' in weather_condition or 'cloudy' in weather_condition:
        weather_data[2][1] = '☑ Overcast'
    elif 'warm' in weather_condition:
        weather_data[3][1] = '☑ Warm'
    
    weather_table = Table(weather_data, colWidths=[1*inch, 1.2*inch, 1.2*inch, 1*inch, 2.1*inch])
    weather_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, 0), 'Helvetica-Bold'),
        ('FONTNAME', (4, 0), (4, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(weather_table)
    story.append(Spacer(1, 8))
    
    # Station and Progress Info
    progress_data = [
        ['Station Name:', report_data['project_location'], 'Overall Progress:', f"{report_data['overall_progress']}%"],
        ['Workers Present:', f"{report_data['workers_present']} personnel", 'Equipment Units:', f"{report_data['equipment_count']} units"],
        ['Sub-contractor:', report_data['subcontractor_name'], 'Safety Status:', report_data['safety_compliance']],
    ]
    
    progress_table = Table(progress_data, colWidths=[1.2*inch, 2.3*inch, 1.2*inch, 1.8*inch])
    progress_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(progress_table)
    story.append(Spacer(1, 8))
    
    # Remarks Section
    story.append(Paragraph("Remarks:", heading_style))
    remarks_text = report_data['activities_completed'] or "No specific remarks for today."
    story.append(Paragraph(remarks_text, normal_style))
    story.append(Spacer(1, 6))
    
    # Project Leader Comments
    story.append(Paragraph("Project Leader Comments:", heading_style))
    comments_text = report_data['recommendations'] or "No additional comments."
    story.append(Paragraph(comments_text, normal_style))
    story.append(Spacer(1, 6))
    
    # Nature of Exception/Defects
    story.append(Paragraph("Nature of Exception/Defects:", heading_style))
    defects_text = report_data['issues_challenges'] or "No exceptions or defects reported."
    story.append(Paragraph(defects_text, normal_style))
    story.append(Spacer(1, 8))
    
    # Add images if any (compact 2x2 grid)
    if images and any(img is not None for img in images):
        story.append(Paragraph("Site Photographs:", heading_style))
        
        # Process images and create compact 2x2 grid
        processed_images = []
        
        for i, img_data in enumerate(images):
            if img_data is not None:
                try:
                    img_data.seek(0)
                    img = Image(img_data, width=1.4*inch, height=1.1*inch)
                    processed_images.append(img)
                except Exception as e:
                    processed_images.append(Paragraph(f"Img {i+1}: Error", small_style))
            else:
                processed_images.append(Paragraph("No Image", small_style))
        
        # Ensure we have exactly 4 slots
        while len(processed_images) < 4:
            processed_images.append(Paragraph("", small_style))
        
        # Create compact 2x2 grid
        image_grid_data = [
            [processed_images[0], processed_images[1]],
            [processed_images[2], processed_images[3]]
        ]
        
        image_table = Table(image_grid_data, colWidths=[1.5*inch, 1.5*inch], rowHeights=[1.2*inch, 1.2*inch])
        image_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        
        story.append(image_table)
        story.append(Spacer(1, 8))
    
    # Signature and completion section
    signature_data = [
        ['Contractor Signature:', '', 'Inspector Signature:', ''],
        ['', '', '', ''],
        ['Completion Date:', report_data['report_date'].strftime('%B %d, %Y'), 'Report By:', report_data['inspector_name']],
    ]
    
    signature_table = Table(signature_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch], rowHeights=[0.3*inch, 0.5*inch, 0.3*inch])
    signature_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(signature_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def main():
    # Header
    st.markdown("""
    <div class="report-header">
        <h1>🏗️ Daily Site Visit Progress Report Generator</h1>
        <p>Professional reporting tool for construction and project management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for quick actions
    with st.sidebar:
        st.markdown("### 📋 Quick Actions")
        st.markdown("Fill out the form to generate your professional site visit report")
        st.markdown("---")
        st.markdown("### 📊 Report Features")
        st.markdown("• Professional PDF export")
        st.markdown("• Image attachments")
        st.markdown("• Comprehensive progress tracking")
        st.markdown("• Official formatting")
    
    # Main form
    with st.form("progress_report_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-header">🏢 Project Information</div>', unsafe_allow_html=True)
            project_name = st.text_input("Project Name*", value="Dhaka Metro Rail Project", disabled=True)
            
            # Station Name dropdown with custom option
            station_options = [
                "S01-Kamlapur", "S02-Rajarbagh", "S03-Malibagh", "S04-Rampura", 
                "S05-Aftab Nagar", "S06-Badda", "S07-North Badda", "S08-Natun Bazar", 
                "S09-Nadda", "Custom Input"
            ]
            station_selection = st.selectbox("Station Name*", station_options)
            
            if station_selection == "Custom Input":
                project_location = st.text_input("Enter Custom Station Name*", placeholder="Enter custom station name")
            else:
                project_location = station_selection
            
            client_name = st.text_input("Client Name*", value="DMTCL", disabled=True)
            contractor_name = st.text_input("Contractor Name*", placeholder="Enter contractor name")
            subcontractor_name = st.text_input("Sub-contractor Name", placeholder="Enter sub-contractor name")
            
            st.markdown('<div class="section-header">👤 Inspector Details</div>', unsafe_allow_html=True)
            inspector_name = st.text_input("Inspector Name*", placeholder="Enter inspector name")
            report_date = st.date_input("Report Date*", value=date.today())
            
        with col2:
            st.markdown('<div class="section-header">⏰ Visit Information</div>', unsafe_allow_html=True)
            visit_start_time = st.time_input("Visit Start Time*")
            visit_end_time = st.time_input("Visit End Time*")
            
            st.markdown('<div class="section-header">🌤️ Site Conditions</div>', unsafe_allow_html=True)
            weather_condition = st.selectbox("Weather Condition*", 
                ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Stormy", "Foggy"])
            temperature = st.number_input("Temperature (°C)*", min_value=-50, max_value=60, value=25)
        
        # Full width sections
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-header">🚧 Site Status</div>', unsafe_allow_html=True)
            safety_compliance = st.selectbox("Safety Compliance*", 
                ["Fully Compliant", "Minor Issues", "Major Issues", "Non-Compliant"])
            workers_present = st.number_input("Number of Workers Present*", min_value=0, value=0)
            equipment_count = st.number_input("Equipment Units on Site*", min_value=0, value=0)
            
        with col2:
            st.markdown('<div class="section-header">📈 Progress Tracking</div>', unsafe_allow_html=True)
            overall_progress = st.slider("Overall Project Progress (%)*", 0, 100, 50)
            work_started = st.text_input("Work Started Today", placeholder="Describe work that began today")
            work_completed = st.text_input("Work Completed Today", placeholder="Describe completed activities")
        
        # Text areas for detailed information
        st.markdown('<div class="section-header">📝 Detailed Report</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            activities_completed = st.text_area("Activities Completed", 
                placeholder="Detailed description of all activities completed during the visit...", height=150)
            issues_challenges = st.text_area("Issues & Challenges", 
                placeholder="Describe any issues, challenges, or concerns observed...", height=150)
        
        with col2:
            recommendations = st.text_area("Recommendations", 
                placeholder="Provide recommendations for improvement or next steps...", height=150)
            next_day_plan = st.text_area("Next Day Activities Plan", 
                placeholder="Outline planned activities for the next day...", height=150)
        
        # Image uploads
        st.markdown('<div class="section-header">📷 Site Photographs</div>', unsafe_allow_html=True)
        st.markdown("Upload up to 4 images for your report")
        
        col1, col2, col3, col4 = st.columns(4)
        images = []
        
        with col1:
            img1 = st.file_uploader("Image 1", type=['png', 'jpg', 'jpeg'], key="img1")
            images.append(img1)
        with col2:
            img2 = st.file_uploader("Image 2", type=['png', 'jpg', 'jpeg'], key="img2")
            images.append(img2)
        with col3:
            img3 = st.file_uploader("Image 3", type=['png', 'jpg', 'jpeg'], key="img3")
            images.append(img3)
        with col4:
            img4 = st.file_uploader("Image 4", type=['png', 'jpg', 'jpeg'], key="img4")
            images.append(img4)
        
        # Submit button
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Generate Progress Report", use_container_width=True)
    
    # Handle form submission outside the form
    if submitted:
        # Validation
        required_fields = [project_name, project_location, client_name, inspector_name, contractor_name]
        if not all(required_fields):
            st.error("⚠️ Please fill in all required fields marked with *")
        else:
            # Prepare report data
            report_data = {
                'project_name': project_name,
                'project_location': project_location,
                'client_name': client_name,
                'contractor_name': contractor_name,
                'subcontractor_name': subcontractor_name,
                'inspector_name': inspector_name,
                'report_date': report_date,
                'visit_start_time': visit_start_time.strftime('%H:%M'),
                'visit_end_time': visit_end_time.strftime('%H:%M'),
                'weather_condition': weather_condition,
                'temperature': temperature,
                'safety_compliance': safety_compliance,
                'workers_present': workers_present,
                'equipment_count': equipment_count,
                'overall_progress': overall_progress,
                'work_started': work_started,
                'work_completed': work_completed,
                'activities_completed': activities_completed,
                'issues_challenges': issues_challenges,
                'recommendations': recommendations,
                'next_day_plan': next_day_plan
            }
            
            try:
                # Generate PDF
                pdf_buffer = create_pdf_report(report_data, images)
                
                # Success message
                st.success("✅ Report generated successfully!")
                
                # Display summary
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>📊 Progress</h4>
                        <h2>{overall_progress}%</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>👷 Workers</h4>
                        <h2>{workers_present}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>🚜 Equipment</h4>
                        <h2>{equipment_count}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>📷 Images</h4>
                        <h2>{len([img for img in images if img is not None])}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Download button
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_buffer.getvalue(),
                    file_name=f"Site_Visit_Report_{project_name.replace(' ', '_')}_{report_date.strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ Error generating report: {str(e)}")
                st.error("Please make sure you have installed: pip install reportlab")

if __name__ == "__main__":
    main()