import streamlit as st
import anthropic
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import io
import random

# --- CONFIG & SECRETS ---
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# --- PAGE CONFIG ---
st.set_page_config(page_title="TailorMyCV Pro", page_icon="🚀", layout="centered")

# --- EXECUTIVE UI STYLING (The 15+ Exp Look) ---
st.markdown("""
    <style>
    /* Dark professional theme */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Fix for the white text/visibility issue */
    .stTextArea textarea, .stTextInput input {
        color: #111111 !important;
        background-color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }

    /* Custom Header */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e1b4b 100%);
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #312e81;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Morale Booster Card */
    .morale-box {
        background-color: #1e293b;
        border-left: 5px solid #3b82f6;
        padding: 25px;
        border-radius: 12px;
        margin-top: 30px;
        line-height: 1.6;
    }
    
    /* ATS Score Gauge */
    .ats-score-container {
        background: #10b98122;
        padding: 20px;
        border-radius: 50%;
        width: 150px;
        height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        border: 3px solid #10b981;
    }
    .ats-number {
        font-size: 42px;
        font-weight: 900;
        color: #10b981;
    }
    </style>
    
    <div class="main-header">
        <h1 style='margin:0; color:white; font-size: 3rem;'>TailorMyCV Pro</h1>
        <p style='color:#94a3b8; font-size: 1.2rem;'>Executive-Grade AI Resume Optimization</p>
    </div>
    """, unsafe_allow_html=True)

# --- DOCUMENT GENERATION FUNCTIONS ---

def create_docx(name, contact_info, content):
    doc = Document()
    
    # Header Section - Centered and Large
    name_p = doc.add_paragraph()
    name_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    name_run = name_p.add_run(name.upper())
    name_run.font.size = Pt(24)
    name_run.bold = True
    
    contact_p = doc.add_paragraph()
    contact_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact_run = contact_p.add_run(contact_info)
    contact_run.font.size = Pt(11)
    
    doc.add_paragraph("_" * 80).alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Content Processing
    for line in content.split('\n'):
        line = line.strip()
        if not line: continue
        
        if line.startswith('###') or (line.isupper() and len(line) < 30):
            p = doc.add_heading(line.replace('#', '').strip(), level=2)
        elif line.startswith('-') or line.startswith('•'):
            p = doc.add_paragraph(line.strip(' -•'), style='List Bullet')
        else:
            doc.add_paragraph(line)
                
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

def create_pdf(name, contact_info, content):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Draw Centered Header
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height - 50, name.upper())
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height - 65, contact_info)
    c.line(50, height - 75, width - 50, height - 75)
    
    # Body Content
    c.setFont("Helvetica", 10)
    text_object = c.beginText(50, height - 100)
    text_object.setLeading(14)
    
    lines = content.split('\n')
    for line in lines:
        wrapped_lines = simpleSplit(line, "Helvetica", 10, width - 100)
        for w_line in wrapped_lines:
            if text_object.getY() < 50:
                c.drawText(text_object)
                c.showPage()
                text_object = c.beginText(50, height - 50)
                text_object.setLeading(14)
            text_object.textLine(w_line)
    
    c.drawText(text_object)
    c.save()
    return buffer.getvalue()

# --- MAIN APP INTERFACE ---

# Input Section
with st.container():
    col_name, col_contact = st.columns(2)
    with col_name:
        full_name = st.text_input("Full Name", placeholder="e.g. John Doe")
    with col_contact:
        contact_details = st.text_input("Contact Info", placeholder="Email | Phone | LinkedIn")
    
    cv_text = st.text_area("Step 1: Paste your current CV details", height=150)
    jd_text = st.text_area("Step 2: Paste the Job Description", height=150)

if st.button("🚀 GENERATE MY OPTIMIZED CV"):
    if not full_name or not cv_text or not jd_text:
        st.warning("Please provide your name, CV, and the Job Description.")
    else:
        with st.spinner("Analyzing Keywords & Boosting Experience Points..."):
            prompt = f"""
            Role: Expert Executive Resume Writer.
            Task: Rewrite the user's CV to match the Job Description. 
            - Use strong action verbs (Led, Orchestrated, Developed).
            - Use bullet points for all experience.
            - Ensure high keyword density.
            - Provide an ATS Score (0-100) based on keyword matching at the very end in this format: [SCORE: XX]

            NAME: {full_name}
            JOB DESCRIPTION: {jd_text}
            CURRENT CV: {cv_text}
            """
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=2500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            full_text = response.content[0].text
            
            # Extract Score
            score = "85" # Default
            if "[SCORE:" in full_text:
                parts = full_text.split("[SCORE:")
                tailored_content = parts[0].strip()
                score = parts[1].split("]")[0].strip()
            else:
                tailored_content = full_text

            st.session_state.v2_cv = tailored_content
            st.session_state.v2_score = score
            st.session_state.v2_ready = True

# Results & Delivery
if st.session_state.get("v2_ready"):
    st.markdown("---")
    st.markdown(f"""
        <div class="ats-score-container">
            <div class="ats-number">{st.session_state.v2_score}%</div>
        </div>
        <p style='text-align:center; color:#10b981; font-weight:bold;'>ATS Match Strength</p>
    """, unsafe_allow_html=True)
    
    st.subheader("Your Tailored Content Preview")
    st.text_area("Review your content (Copying disabled in Pro version)", 
                 st.session_state.v2_cv[:600] + "...", height=150, disabled=True)

    st.markdown("### 📥 Download Your Polished Files")
    c1, c2 = st.columns(2)
    
    # Word Download
    docx_file = create_docx(full_name, contact_details, st.session_state.v2_cv)
    c1.download_button("📂 Download Word (.docx)", data=docx_file, 
                       file_name=f"{full_name}_Tailored_CV.docx", use_container_width=True)
    
    # PDF Download
    pdf_file = create_pdf(full_name, contact_details, st.session_state.v2_cv)
    c2.download_button("📄 Download PDF (.pdf)", data=pdf_file, 
                       file_name=f"{full_name}_Tailored_CV.pdf", use_container_width=True)

    # MORALE BOOSTER & REFERRAL
    boosters = [
        f"Your technical expertise in this field is undeniable, {full_name.split()[0]}. This CV now perfectly highlights your 15+ years of impact. Go crush that interview—you've got this! 🚀",
        "The way we've restructured your achievements shows you're not just an applicant, you're the leader they need. Confidence is key now. Good luck!",
        "This CV is built to win. You've got the skills, and now the ATS knows it too. Remember: You belong in that room. Best of luck!"
    ]
    
    st.markdown(f"""
        <div class="morale-box">
            <h3 style='margin-top:0;'>✨ You're Ready!</h3>
            <p>{random.choice(boosters)}</p>
            <p style='background:#0f172a; padding:10px; border-radius:5px; border: 1px solid #334155;'>
                <b>💡 Pro-Tip:</b> We recommend using the <b>Word (.docx)</b> file for large company portals (ATS), as some older systems read Word better than PDF. Use the PDF for direct emails to recruiters!
            </p>
            <p style='font-style: italic; font-size: 0.9rem; margin-top:15px;'>
                Found this helpful? Help your friends beat the bots too! Share <b>TailorMyCV</b> with your network. 
                Our goal is to get talented people like you past the filters and into the interview room.
            </p>
        </div>
    """, unsafe_allow_html=True)
