# ================================================================
#  TailorMyCV V2 — Professional Edition  |  app_v2.py
#  AI-Powered Resume Intelligence for Success-Driven Professionals
# ================================================================

import streamlit as st
import anthropic
import io
import os
import re
import random
import time

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH

# --- Setup Parsers and PDF Engines ---
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_OK = True
except ImportError:
    REPORTLAB_OK = False

# ════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="TailorMyCV",
    page_icon="🎯",
    layout="centered",
)

# ════════════════════════════════════════════════════════════
#  PROFESSIONAL CSS
# ════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* Sophisticated Dark Theme */
.stApp { background-color: #0D1B2A !important; color: #F0EDE8 !important; }

/* Input Box Polish */
.stTextArea textarea { 
    height: 150px !important; 
    background-color: #0A1520 !important; 
    color: #F0EDE8 !important;
    border: 1px solid rgba(201,168,76,0.3) !important;
}

/* Button Colors */
div.stDownloadButton > button:first-child {
    background-color: #1A5C4A !important; /* Word Blue/Teal */
    color: white !important;
}
div.stDownloadButton + div.stDownloadButton > button:first-child {
    background-color: #9B2C2C !important; /* PDF Red */
    color: white !important;
}

/* Header Cleanup */
.masthead-logo { font-size: 2.2rem; font-weight: 700; color: #F0EDE8; text-align: center; margin-bottom: 5px; }
.masthead-sub { font-size: 0.9rem; color: #8FA3B8; text-align: center; margin-bottom: 25px; }

</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  MAIN LOGIC
# ════════════════════════════════════════════════════════════

# 1. Masthead
st.markdown('<div class="masthead-logo">TailorMyCV</div>', unsafe_allow_html=True)
st.markdown('<div class="masthead-sub">AI-Powered Resume Intelligence for Success-Driven Professionals</div>', unsafe_allow_html=True)

# 2. Lead Generation Form
if 'user_captured' not in st.session_state:
    st.session_state.user_captured = False

if not st.session_state.user_captured:
    with st.container():
        st.subheader("Where should we send your career insights?")
        u_name = st.text_input("Full Name")
        u_email = st.text_input("Email Address")
        if st.button("Start My Optimization"):
            if u_name and u_email:
                st.session_state.user_name = u_name
                st.session_state.user_email = u_email
                st.session_state.user_captured = True
                print(f"NEW LEAD: {u_name} ({u_email})") # Captured in Streamlit Logs
                st.rerun()
            else:
                st.error("Please provide both name and email to continue.")
    st.stop()

# 3. Main App Steps (After Lead Capture)
# [Your existing logic for JD and CV paste goes here, 
#  incorporating the 'Strict AI Instructions' in the Prompt]

# AI SYSTEM PROMPT UPDATE:
# "STRICT RULE: Do not invent skills. If a skill is in the JD but not the CV, 
# do not add it to the resume. Identify it only in 'What's missing for this role?'."

# 4. Success Animation & Morale
if st.session_state.get('optimization_complete'):
    st.balloons()
    role = st.session_state.get('target_role', 'Professional')
    st.success(f"Excellent work, {st.session_state.user_name}! As a {role}, your foundation is solid.")
    st.info("We highly recommend using the Word (.docx) file for the application portal for better results.")
