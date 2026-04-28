# ================================================================
#  TailorMyCV V3 — Production Edition (6-Refinement Update)
#  Stack: Streamlit · Claude Haiku · Razorpay
#         python-docx · reportlab
#
#  Refinements implemented:
#   1. Intelligent Lead Generation (Auto-Fill from CV + JD)
#   2. Enhanced Download Buttons (icons + Teal Word / Red PDF)
#   3. Bulleted Gap Analysis (⚠️ / 💡 icons per bullet)
#   4. Professional Document Formatting (bold company+dates, justified text)
#   5. Dynamic Morale Booster (name + role personalised)
#   6. Social Sharing Integration (Copy URL / WhatsApp / Instagram)
# ================================================================

import streamlit as st
import anthropic
import io, os, re, random

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH

try:
    import PyPDF2
    PDF_OK = True
except ImportError:
    PDF_OK = False

try:
    import docx2txt
    DOCX_OK = True
except ImportError:
    DOCX_OK = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Paragraph,
                                    Spacer, HRFlowable, KeepTogether)
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    REPORTLAB_OK = True
except ImportError:
    REPORTLAB_OK = False


# ════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="TailorMyCV — AI Resume Tailoring",
    page_icon="◆",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --navy:        #0D1B2A;
  --navy-2:      #132238;
  --navy-3:      #1A2F4A;
  --navy-card:   #1E3550;
  --gold:        #C9A84C;
  --gold-lt:     #E8C97A;
  --gold-dim:    rgba(201,168,76,0.15);
  --teal:        #2DD4BF;
  --teal-dim:    rgba(45,212,191,0.12);
  --text-prime:  #F0EDE8;
  --text-muted:  #8FA3B8;
  --text-dim:    #566D84;
  --border:      rgba(201,168,76,0.18);
  --border-soft: rgba(240,237,232,0.08);
  --danger:      #F87171;
  --success:     #34D399;
  --blue:        #3B82F6;
  --red:         #EF4444;
  --radius:      12px;
  --radius-lg:   18px;
  --shadow:      0 8px 32px rgba(0,0,0,0.40);
  --shadow-gold: 0 4px 20px rgba(201,168,76,0.25);
}

html, body, [class*="css"], .stApp {
  font-family: 'Inter', sans-serif !important;
  background-color: var(--navy) !important;
  color: var(--text-prime) !important;
}
#MainMenu, footer, header { visibility: hidden !important; }
.block-container { padding: 1.5rem 1rem 5rem !important; max-width: 800px !important; }

/* ── MASTHEAD ── */
.masthead {
  text-align: center;
  padding: 2.4rem 1.5rem 1.8rem;
  background: linear-gradient(160deg, var(--navy-3) 0%, var(--navy-2) 100%);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  margin-bottom: 2rem;
  box-shadow: var(--shadow);
  position: relative;
  overflow: hidden;
}
.masthead::before {
  content: '';
  position: absolute; top: -60px; right: -60px;
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(201,168,76,0.08) 0%, transparent 70%);
  border-radius: 50%;
}
.masthead-logo {
  font-family: 'Playfair Display', serif;
  font-size: 2.4rem; color: var(--text-prime);
  line-height: 1.1; margin-bottom: 0.45rem;
}
.masthead-logo .accent { color: var(--gold); }
.masthead-sub { font-size: 0.84rem; color: var(--text-muted); letter-spacing: 0.03em; }
.masthead-badges { display:flex; gap:8px; justify-content:center; flex-wrap:wrap; margin-top:1.1rem; }
.mbadge { background:var(--gold-dim); color:var(--gold-lt); border:1px solid rgba(201,168,76,0.3); border-radius:999px; font-size:0.7rem; font-weight:600; padding:4px 12px; }

/* ── STEP BAR ── */
.step-bar { display:flex; align-items:center; justify-content:center; gap:0; margin-bottom:2rem; flex-wrap:wrap; row-gap:6px; }
.step-pill { display:flex; align-items:center; gap:5px; padding:6px 12px; border-radius:999px; font-size:0.7rem; font-weight:600; color:var(--text-dim); background:var(--navy-card); border:1px solid var(--border-soft); transition:all .3s; white-space:nowrap; }
.step-pill.active { background:var(--gold-dim); color:var(--gold-lt); border-color:var(--border); box-shadow:var(--shadow-gold); }
.step-pill.done { background:var(--teal-dim); color:var(--teal); border-color:rgba(45,212,191,0.25); }
.step-connector { width:18px; height:1px; background:var(--border-soft); }

/* ── CARDS ── */
.card { background:var(--navy-card); border-radius:var(--radius-lg); border:1px solid var(--border-soft); padding:1.6rem 1.5rem; margin-bottom:1.1rem; box-shadow:var(--shadow); }
.card-title { font-family:'Playfair Display',serif; font-size:1.05rem; color:var(--gold-lt); margin-bottom:0.85rem; display:flex; align-items:center; gap:8px; }
.divider { height:1px; background:var(--border-soft); margin:1rem 0; }

/* ── STATUS BOXES ── */
.info-box   { background:rgba(45,212,191,0.07); border-left:3px solid var(--teal); border-radius:0 8px 8px 0; padding:9px 13px; font-size:0.81rem; color:var(--teal); margin:0.7rem 0; }
.warn-box   { background:rgba(248,113,113,0.08); border-left:3px solid var(--danger); border-radius:0 8px 8px 0; padding:9px 13px; font-size:0.81rem; color:#FCA5A5; margin:0.7rem 0; }
.success-box{ background:rgba(52,211,153,0.08); border-left:3px solid var(--success); border-radius:0 8px 8px 0; padding:9px 13px; font-size:0.81rem; color:var(--success); margin:0.7rem 0; }
.gold-box   { background:var(--gold-dim); border:1px solid rgba(201,168,76,0.30); border-radius:var(--radius); padding:13px 16px; font-size:0.83rem; color:var(--gold-lt); margin:0.7rem 0; }
.lead-box   { background:rgba(59,130,246,0.10); border:1px solid rgba(59,130,246,0.30); border-radius:var(--radius); padding:13px 16px; font-size:0.82rem; color:#93C5FD; margin:0.7rem 0; }

/* ── TEXT INPUTS — CONTRAST-FIXED ── */
.stTextArea textarea, textarea {
  background-color: #0A1520 !important;
  color: #F0EDE8 !important;
  caret-color: #C9A84C !important;
  border: 1px solid rgba(201,168,76,0.30) !important;
  border-radius: 10px !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.82rem !important;
  line-height: 1.55 !important;
  padding: 10px 12px !important;
  box-shadow: inset 0 2px 6px rgba(0,0,0,0.30) !important;
  transition: border-color .2s !important;
  resize: vertical !important;
}
.stTextArea textarea:focus, textarea:focus {
  border-color: #C9A84C !important;
  box-shadow: 0 0 0 3px rgba(201,168,76,0.14), inset 0 2px 6px rgba(0,0,0,0.30) !important;
  outline: none !important;
}
.stTextArea textarea::placeholder, textarea::placeholder { color:#566D84 !important; opacity:1 !important; }
.stTextArea textarea:disabled, textarea:disabled {
  background-color: #060E18 !important;
  color: #3D5568 !important;
  caret-color: transparent !important;
  border-color: rgba(255,255,255,0.04) !important;
  cursor: not-allowed !important;
}
.stTextInput input, input[type="text"], input[type="email"] {
  background-color: #0A1520 !important;
  color: #F0EDE8 !important;
  caret-color: #C9A84C !important;
  border: 1px solid rgba(201,168,76,0.30) !important;
  border-radius: 8px !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.87rem !important;
  padding: 9px 13px !important;
}
.stTextInput input:focus, input[type="text"]:focus, input[type="email"]:focus {
  border-color: #C9A84C !important;
  box-shadow: 0 0 0 3px rgba(201,168,76,0.14) !important;
  outline: none !important;
}
.stTextInput input::placeholder { color:#566D84 !important; }
.stTextArea label, .stTextInput label { color:var(--text-muted) !important; font-size:0.81rem !important; font-weight:500 !important; }

/* ── FILE UPLOADER ── */
.stFileUploader section, div[data-testid="stFileUploadDropzone"] {
  background: rgba(201,168,76,0.05) !important;
  border: 2px dashed rgba(201,168,76,0.35) !important;
  border-radius: var(--radius) !important;
}
.stFileUploader section:hover, div[data-testid="stFileUploadDropzone"]:hover {
  background: var(--gold-dim) !important; border-color: var(--gold) !important;
}
.stFileUploader label, .stFileUploader p, .stFileUploader span { color:var(--text-muted) !important; }
[data-testid="stFileUploadDropzone"] p { color:var(--gold-lt) !important; }

/* ── PRIMARY BUTTON (gold) ── */
.stButton > button {
  background: linear-gradient(135deg, #C9A84C 0%, #A8793A 100%) !important;
  color: #0D1B2A !important;
  border: none !important;
  border-radius: 999px !important;
  padding: 0.6rem 1.8rem !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.87rem !important;
  letter-spacing: 0.03em !important;
  transition: all .2s !important;
  box-shadow: 0 4px 18px rgba(201,168,76,0.25) !important;
}
.stButton > button:hover {
  background: linear-gradient(135deg, #E8C97A 0%, #C9A84C 100%) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 22px rgba(201,168,76,0.38) !important;
}

/* ── TEAL/GREEN DOWNLOAD BUTTON (Word) — Refinement #2 ── */
.dl-word .stDownloadButton > button {
  background: linear-gradient(135deg, #0D9488 0%, #0F766E 100%) !important;
  color: #fff !important;
  border: 1px solid rgba(45,212,191,0.40) !important;
  border-radius: 999px !important;
  padding: 0.6rem 1.8rem !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.87rem !important;
  box-shadow: 0 4px 16px rgba(13,148,136,0.35) !important;
  transition: all .2s !important;
}
.dl-word .stDownloadButton > button:hover {
  background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 8px 22px rgba(13,148,136,0.48) !important;
}

/* ── RED/CORAL DOWNLOAD BUTTON (PDF) — Refinement #2 ── */
.dl-pdf .stDownloadButton > button {
  background: linear-gradient(135deg, #E11D48 0%, #BE123C 100%) !important;
  color: #fff !important;
  border: 1px solid rgba(244,63,94,0.40) !important;
  border-radius: 999px !important;
  padding: 0.6rem 1.8rem !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.87rem !important;
  box-shadow: 0 4px 16px rgba(225,29,72,0.32) !important;
  transition: all .2s !important;
}
.dl-pdf .stDownloadButton > button:hover {
  background: linear-gradient(135deg, #F43F5E 0%, #E11D48 100%) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 8px 22px rgba(225,29,72,0.45) !important;
}

/* ── PAY BUTTON ── */
.pay-btn-wrap { text-align:center; margin:1.2rem 0; }
.pay-btn {
  display:inline-block;
  background:linear-gradient(135deg,#C9A84C 0%,#A8793A 100%);
  color:#0D1B2A !important;
  font-family:'Inter',sans-serif;
  font-weight:800; font-size:1rem;
  padding:14px 40px; border-radius:999px;
  text-decoration:none !important;
  box-shadow:0 4px 20px rgba(201,168,76,0.32);
  transition:all .2s; letter-spacing:0.02em;
}
.pay-btn:hover { background:linear-gradient(135deg,#E8C97A 0%,#C9A84C 100%); transform:translateY(-2px); box-shadow:0 8px 26px rgba(201,168,76,0.48); }

/* ── ATS SCORE ── */
.ats-wrap { background:var(--navy-3); border:1px solid var(--border); border-radius:var(--radius-lg); padding:1.3rem 1.5rem; margin:0.9rem 0; }
.ats-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:0.7rem; }
.ats-label { font-size:0.76rem; font-weight:600; letter-spacing:0.12em; text-transform:uppercase; color:var(--text-muted); }
.ats-num { font-family:'Playfair Display',serif; font-size:2.1rem; font-weight:700; line-height:1; }
.ats-num.high { color:var(--success); }
.ats-num.mid  { color:var(--gold); }
.ats-num.low  { color:var(--danger); }
.ats-track { width:100%; height:7px; background:rgba(255,255,255,0.07); border-radius:999px; overflow:hidden; }
.ats-fill  { height:100%; border-radius:999px; }
.ats-gap { margin-top:0.85rem; font-size:0.78rem; color:var(--text-muted); line-height:1.65; }
.ats-gap strong { color:var(--gold-lt); }

/* ── GAP ANALYSIS BULLETS — Refinement #3 ── */
.gap-bullet-list { list-style:none; margin:0.5rem 0 0 0; padding:0; }
.gap-bullet-list li {
  display:flex; align-items:flex-start; gap:7px;
  font-size:0.78rem; color:var(--text-muted);
  line-height:1.6; padding:3px 0;
  border-bottom:1px solid rgba(255,255,255,0.04);
}
.gap-bullet-list li:last-child { border-bottom:none; }
.gap-bullet-icon { font-size:0.85rem; flex-shrink:0; margin-top:1px; }

/* ── BADGES ── */
.badge { display:inline-block; background:var(--gold-dim); color:var(--gold-lt); border:1px solid rgba(201,168,76,0.25); font-size:0.67rem; font-weight:700; letter-spacing:0.05em; padding:3px 9px; border-radius:999px; margin-right:4px; margin-bottom:3px; text-transform:uppercase; }

/* ── MODE CARDS ── */
.mode-card { border:1px solid var(--border-soft); border-radius:var(--radius); padding:13px 9px; text-align:center; background:var(--navy-3); transition:all .2s; }
.mode-card.sel { border-color:var(--gold); background:var(--gold-dim); box-shadow:var(--shadow-gold); }
.mode-icon { font-size:1.45rem; }
.mode-label { font-size:0.76rem; font-weight:700; color:var(--text-prime); margin-top:5px; }
.mode-desc  { font-size:0.67rem; color:var(--text-muted); margin-top:2px; }

/* ── MORALE CARD ── */
.morale-card {
  background:linear-gradient(135deg,var(--navy-3) 0%,#1A3050 100%);
  border:1px solid rgba(201,168,76,0.28);
  border-radius:var(--radius-lg);
  padding:1.7rem; text-align:center;
  margin:1.1rem 0; box-shadow:var(--shadow-gold);
  position:relative; overflow:hidden;
}
.morale-card::after { content:'◆'; position:absolute; bottom:-18px; right:8px; font-size:5.5rem; color:rgba(201,168,76,0.05); line-height:1; }
.morale-icon { font-size:2rem; margin-bottom:0.5rem; }
.morale-text { font-family:'Playfair Display',serif; font-size:1rem; color:var(--gold-lt); line-height:1.55; font-style:italic; }

/* ── REFERRAL ── */
.referral-box { background:var(--teal-dim); border:1px solid rgba(45,212,191,0.18); border-radius:var(--radius); padding:0.95rem 1.1rem; text-align:center; margin-top:0.9rem; font-size:0.82rem; color:var(--teal); }
.referral-box strong { color:#fff; }

/* ── SOCIAL SHARING — Refinement #6 ── */
.share-row {
  background:var(--navy-3); border:1px solid var(--border-soft);
  border-radius:var(--radius); padding:1rem 1.2rem;
  margin-top:1rem; text-align:center;
}
.share-title { font-size:0.78rem; font-weight:600; color:var(--text-muted); letter-spacing:0.08em; text-transform:uppercase; margin-bottom:0.75rem; }
.share-btns { display:flex; gap:10px; justify-content:center; flex-wrap:wrap; }
.share-btn {
  display:inline-flex; align-items:center; gap:6px;
  padding:8px 18px; border-radius:999px;
  font-family:'Inter',sans-serif; font-size:0.78rem; font-weight:700;
  text-decoration:none !important; cursor:pointer;
  border:none; transition:all .2s;
}
.share-btn-copy  { background:rgba(201,168,76,0.18); color:var(--gold-lt); border:1px solid rgba(201,168,76,0.30); }
.share-btn-copy:hover  { background:rgba(201,168,76,0.30); transform:translateY(-1px); }
.share-btn-wa    { background:#25D366; color:#fff; }
.share-btn-wa:hover    { background:#22C55E; transform:translateY(-1px); }
.share-btn-ig    { background:linear-gradient(135deg,#E1306C,#833AB4); color:#fff; }
.share-btn-ig:hover    { background:linear-gradient(135deg,#F43F5E,#A855F7); transform:translateY(-1px); }

/* ── AUTO-FILL BADGE ── */
.autofill-badge {
  display:inline-block;
  background:rgba(45,212,191,0.15); color:var(--teal);
  border:1px solid rgba(45,212,191,0.25); border-radius:999px;
  font-size:0.67rem; font-weight:700; padding:2px 9px; margin-left:8px;
  vertical-align:middle;
}

/* ── CONFETTI CANVAS ── */
#confetti-canvas {
  position:fixed; top:0; left:0;
  width:100vw; height:100vh;
  pointer-events:none; z-index:9999;
}

/* ── MISC ── */
.stSpinner > div { border-top-color:var(--gold) !important; }
hr { border-color:var(--border-soft) !important; }
p, li { color:var(--text-prime) !important; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  CONSTANTS
# ════════════════════════════════════════════════════════════
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

APP_URL = "https://tailormycv.streamlit.app"  # ← update to your deployed URL

MODE_META = {
    "ATS-Optimizer": {
        "icon": "🎯",
        "desc": "Keyword-match to beat ATS filters",
        "instr": "Prioritise ATS keyword optimisation. Mirror EXACT terminology from the JD.",
    },
    "Executive Tone": {
        "icon": "💼",
        "desc": "C-suite gravitas & boardroom authority",
        "instr": "Rewrite with commanding executive authority. Lead with strategic business impact and P&L ownership.",
    },
    "Career Switch": {
        "icon": "🔄",
        "desc": "Pivot your story to a new industry",
        "instr": "Bridge the career gap. Aggressively reframe transferable skills; the Summary must connect past to future.",
    },
}

# Dynamic morale templates — Refinement #5: {name} + {role} substituted at render time
MORALE_TEMPLATES = [
    ("🚀", "Excellent work, {name}! This CV is now a tactical weapon for your {role} application. You've got the stats — now go crush the interview!"),
    ("🏆", "Outstanding, {name}! Every great {role} started exactly where you are. This CV is your launchpad — go own that room."),
    ("⚡", "{name}, the best {role} in the room walks in prepared. That's precisely what you are today. Go show them."),
    ("🎯", "Well done, {name}! Hiring managers looking for a {role} are about to see your full potential — unfiltered and unstoppable."),
    ("💎", "{name}, a {role} of your calibre deserves a CV that commands attention. Now you have one. Go make it count."),
    ("🔥", "Bots beaten, keywords matched, {name}! Now go show them why you're the {role} they've been waiting for."),
    ("🌟", "{name}, this isn't just a resume. It's a {role}'s story, told with precision, impact, and authority."),
    ("🦁", "The role of {role} doesn't choose anyone, {name}. You've earned your shot — now go take it with confidence!"),
]

DEFAULTS = {
    "step": 1,
    "cv_text": "",
    "jd_text": "",
    "jd_role": "Professional",
    "jd_company": "",                   # Refinement #1: extracted company
    "mode": "ATS-Optimizer",
    "lead_name": "",
    "lead_email": "",
    "lead_captured": False,
    "details_confirmed": False,         # Refinement #1: confirm step flag
    "tailored_cv": "",
    "ats_score": None,
    "ats_color": "mid",
    "ats_bar_color": "#C9A84C",
    "gap_analysis": "",
    "payment_verified": False,
    "downloaded": False,
    "morale_msg": None,
    "confetti_fired": False,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ════════════════════════════════════════════════════════════
#  HELPERS — PARSERS
# ════════════════════════════════════════════════════════════
def extract_pdf(b: bytes) -> str:
    if not PDF_OK: return ""
    r = PyPDF2.PdfReader(io.BytesIO(b))
    return "\n".join(p.extract_text() or "" for p in r.pages)

def extract_docx_text(b: bytes) -> str:
    if not DOCX_OK: return ""
    return docx2txt.process(io.BytesIO(b))


# ── Refinement #1: Regex extractors ──────────────────────────
def _extract_name_from_cv(cv_text: str) -> str:
    """
    Heuristic: The candidate's name is usually on the first non-empty line,
    containing 2–4 capitalised words with no digits or special chars.
    """
    for line in cv_text.split("\n"):
        s = line.strip()
        if not s:
            continue
        # Must be 2–4 words, all alpha + spaces (allow dots/hyphens for initials)
        if re.match(r'^[A-Z][a-zA-Z.\-]+(?:\s+[A-Z][a-zA-Z.\-]+){1,3}$', s):
            if len(s) < 60:
                return s
        break  # only check first non-empty line
    return ""

def _extract_email_from_cv(cv_text: str) -> str:
    """Extract first e-mail address found in CV text."""
    m = re.search(r'[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z]{2,}', cv_text)
    return m.group(0) if m else ""

def _guess_role(jd_text: str) -> str:
    """Best-effort role title extraction from JD."""
    snippet = jd_text[:400]
    for pattern in [
        r"(?:hiring|looking for|seeking|role[:\s]+|position[:\s]+|title[:\s]+)\s*(?:a\s+|an\s+)?([A-Z][^\n,.(]{3,40})",
        r"^([A-Z][^\n,.(]{3,40})(?:\n|$)",
    ]:
        m = re.search(pattern, snippet, re.IGNORECASE | re.MULTILINE)
        if m:
            role = m.group(1).strip().rstrip(".")
            if 3 < len(role) < 60:
                return role
    return "Professional"

def _guess_company(jd_text: str) -> str:
    """Best-effort company extraction from JD."""
    patterns = [
        r"(?:at|join|with|company[:\s]+|organisation[:\s]+|employer[:\s]+)\s+([A-Z][A-Za-z0-9& .\-]{2,35}?)(?:\s*[\n,.(]|$)",
        r"(?:About\s+)([A-Z][A-Za-z0-9& .\-]{2,35})(?:\s*[\n,.]|$)",
    ]
    for pat in patterns:
        m = re.search(pat, jd_text[:500], re.IGNORECASE)
        if m:
            company = m.group(1).strip().rstrip(".,")
            if 2 < len(company) < 50:
                return company
    return ""


# ── Refinement #3: Gap analysis → bullet list ────────────────
_GAP_ICONS = ["⚠️", "💡", "⚠️", "💡", "⚠️", "💡", "⚠️", "💡"]

def _gap_to_bullets_html(gap_text: str) -> str:
    """
    Splits the raw gap text into bullet points and prepends alternating icons.
    Handles both sentence-style text and already-bulleted text.
    """
    # Normalise: split on sentence endings, newlines, or existing bullets
    raw = re.split(r'(?<=[.!?])\s+|[\n•\-]+', gap_text)
    bullets = [s.strip() for s in raw if s.strip() and len(s.strip()) > 8]

    if not bullets:
        bullets = [gap_text.strip()]

    items_html = ""
    for i, bullet in enumerate(bullets):
        icon = _GAP_ICONS[i % len(_GAP_ICONS)]
        items_html += f'<li><span class="gap-bullet-icon">{icon}</span><span>{bullet}</span></li>'

    return f'<ul class="gap-bullet-list">{items_html}</ul>'


# ════════════════════════════════════════════════════════════
#  ANTHROPIC CLIENT
# ════════════════════════════════════════════════════════════
def get_client():
    try:
        key = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        st.error("ANTHROPIC_API_KEY not set. Add it in Streamlit → Settings → Secrets.")
        st.stop()
    return anthropic.Anthropic(api_key=key)


# ════════════════════════════════════════════════════════════
#  SYSTEM PROMPT — INTEGRITY-FIRST
# ════════════════════════════════════════════════════════════
def build_system_prompt(mode: str) -> str:
    instr = MODE_META[mode]["instr"]
    return f"""You are a world-class executive recruiter and ATS specialist with 25 years of experience
placing senior professionals at Fortune 500 companies and leading Indian enterprises.

## MODE
{instr}

## INTEGRITY RULES — NON-NEGOTIABLE
1. DO NOT invent or add any skill, tool, technology, qualification, or achievement
   that does not appear in the original CV. Every line must be truthful to the source.
2. If the candidate lacks a skill required by the JD, DO NOT include it in the CV body.
   Instead, list it ONLY inside the "MISSING FOR SUCCESS" section of the ATS block.
3. Your job is to REFRAME and OPTIMISE existing experience — not to fabricate.

## UNIVERSAL STYLE RULES
4. Use elite action verbs: Spearheaded, Architected, Orchestrated, Transformed, Accelerated,
   Championed, Instituted, Galvanised, Propelled.
5. Every experience bullet: [Action Verb] + [Context] + [Measurable Outcome].
6. Structure MUST follow exactly:

   [CANDIDATE FULL NAME]
   [Phone | Email | LinkedIn | City]

   PROFESSIONAL SUMMARY
   [3–4 sentences]

   CORE COMPETENCIES
   [8–12 pipe-separated skills — truthful to CV only]

   PROFESSIONAL EXPERIENCE
   [Company] | [Title] | [Dates]
   • [bullet]

   EDUCATION
   [Degree | Institution | Year]

   CERTIFICATIONS & AWARDS
   [only if present in original CV]

7. Output ONLY the CV text above — no commentary, no markdown, no preamble.
8. After the CV, on a new line, output EXACTLY:

---ATS_ANALYSIS---
SCORE: [integer 0-100]
MISSING: [2-3 sentences starting with "Your CV is missing..." naming specific skills/keywords from the JD that the candidate does NOT have]
---END_ATS---

Do NOT skip the ATS block."""


# ════════════════════════════════════════════════════════════
#  CLAUDE CALL + ATS PARSING
# ════════════════════════════════════════════════════════════
def call_claude(cv_text, jd_text, mode):
    client = get_client()
    msg = (
        f"=== ORIGINAL CV ===\n{cv_text}\n\n"
        f"=== JOB DESCRIPTION ===\n{jd_text}\n\n"
        f"Tailor strictly using the '{mode}' approach. "
        f"Remember: no invented skills. Append the ---ATS_ANALYSIS--- block."
    )
    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=3000,
        system=build_system_prompt(mode),
        messages=[{"role": "user", "content": msg}],
    )
    full = resp.content[0].text

    score, gap, cv_clean = None, "", full
    m = re.search(
        r"---ATS_ANALYSIS---\s*SCORE:\s*(\d+)\s*MISSING:\s*(.*?)\s*---END_ATS---",
        full, re.DOTALL | re.IGNORECASE,
    )
    if m:
        score    = min(100, max(0, int(m.group(1))))
        gap      = m.group(2).strip()
        cv_clean = full[:m.start()].strip()

    if score is None:
        jd_w  = set(re.findall(r'\b[a-z]{4,}\b', jd_text.lower()))
        cv_w  = set(re.findall(r'\b[a-z]{4,}\b', cv_clean.lower()))
        score = min(93, int((len(jd_w & cv_w) / max(len(jd_w), 1)) * 145))
        gap   = "Your CV is missing a detailed gap breakdown — review the JD keywords manually."

    color     = "high" if score >= 75 else ("mid" if score >= 50 else "low")
    bar_color = "#34D399" if color == "high" else ("#C9A84C" if color == "mid" else "#F87171")
    return {"cv_text": cv_clean, "score": score, "color": color,
            "bar_color": bar_color, "gap": gap}


# ════════════════════════════════════════════════════════════
#  DOCUMENT GENERATORS — Refinement #4: Bold company+dates, Justified text
# ════════════════════════════════════════════════════════════
def _parse_header(cv_text):
    lines = [l.strip() for l in cv_text.split("\n") if l.strip()]
    name = lines[0] if lines else "Candidate"
    contact = ""
    if len(lines) > 1 and ("|" in lines[1] or "@" in lines[1] or "+" in lines[1]):
        contact = lines[1]
    return name, contact

def _add_hr_docx(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot  = OxmlElement('w:bottom')
    bot.set(qn('w:val'), 'single')
    bot.set(qn('w:sz'), '4')
    bot.set(qn('w:space'), '1')
    bot.set(qn('w:color'), 'B8964A')
    pBdr.append(bot)
    pPr.append(pBdr)
    return p

# ── Refinement #4: Detect and bold company name + date range in experience lines ──
_EXP_LINE_RE = re.compile(
    r'^([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(.+)$'  # Company | Title | Dates
)
_DATE_RE = re.compile(
    r'(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{2,4}'
     r'|\b\d{4}\s*[-–—]\s*(?:\d{4}|Present|Current|Till Date|Now)\b'
     r'|\b\d{4}\b)',
    re.IGNORECASE
)

def _add_experience_line_docx(doc, line: str):
    """
    Renders a 'Company | Title | Dates' line with Company and Dates in bold.
    Falls back to a regular paragraph if pattern doesn't match.
    """
    m = _EXP_LINE_RE.match(line)
    if m:
        company, title, dates = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after  = Pt(1)
        # Bold company
        r1 = p.add_run(company)
        r1.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0x1A, 0x35, 0x6B)
        # Separator + title
        r2 = p.add_run(f" | {title} | ")
        r2.font.size = Pt(9.5)
        # Bold dates
        r3 = p.add_run(dates)
        r3.bold = True
        r3.font.size = Pt(9.5)
        r3.font.color.rgb = RGBColor(0x44, 0x44, 0x44)
    else:
        # Fallback: just check if line contains a date range, bold that part
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(1)
        dm = _DATE_RE.search(line)
        if dm:
            before = line[:dm.start()]
            date_part = dm.group(0)
            after  = line[dm.end():]
            if before:
                rb = p.add_run(before)
                rb.font.size = Pt(9.5)
            rd = p.add_run(date_part)
            rd.bold = True
            rd.font.size = Pt(9.5)
            if after:
                ra = p.add_run(after)
                ra.font.size = Pt(9.5)
        else:
            r = p.add_run(line)
            r.font.size = Pt(9.5)

def generate_docx(cv_text: str) -> bytes:
    doc = Document()
    for sec in doc.sections:
        sec.top_margin    = Inches(0.80)
        sec.bottom_margin = Inches(0.80)
        sec.left_margin   = Inches(0.95)
        sec.right_margin  = Inches(0.95)

    name, contact = _parse_header(cv_text)

    # ── Name — huge, centred ──
    np_ = doc.add_paragraph()
    np_.alignment = WD_ALIGN_PARAGRAPH.CENTER
    nr = np_.add_run(name.upper())
    nr.bold = True
    nr.font.size = Pt(20)
    nr.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    np_.paragraph_format.space_before = Pt(0)
    np_.paragraph_format.space_after  = Pt(1)

    # ── Contact — centred ──
    if contact:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cr = cp.add_run(contact)
        cr.font.size = Pt(9)
        cr.font.color.rgb = RGBColor(0x44, 0x44, 0x44)
        cp.paragraph_format.space_before = Pt(0)
        cp.paragraph_format.space_after  = Pt(3)

    _add_hr_docx(doc)

    lines = cv_text.split("\n")
    in_header = True
    body_start = 0
    for i, line in enumerate(lines):
        s = line.strip()
        if in_header and s in (name, contact, ""):
            body_start = i + 1
        else:
            in_header = False

    in_experience_section = False

    for line in lines[body_start:]:
        s = line.strip()
        if not s:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(0)
            continue

        is_heading = s.isupper() and len(s) < 55 and not s.startswith("•")

        if is_heading:
            _add_hr_docx(doc)
            p = doc.add_paragraph()
            r = p.add_run(s)
            r.bold = True
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(0x1A, 0x35, 0x6B)
            p.paragraph_format.space_before = Pt(5)
            p.paragraph_format.space_after  = Pt(1)
            # Track whether we're in the experience section
            in_experience_section = "EXPERIENCE" in s.upper()

        elif s.startswith("•") or s.startswith("-"):
            p = doc.add_paragraph(style="List Bullet")
            r = p.add_run(s.lstrip("•- ").strip())
            r.font.size = Pt(9.5)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY   # Refinement #4
            p.paragraph_format.left_indent  = Inches(0.22)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after  = Pt(1)

        elif in_experience_section and "|" in s:
            # Refinement #4: Bold company name + dates in experience lines
            _add_experience_line_docx(doc, s)

        else:
            p = doc.add_paragraph()
            r = p.add_run(s)
            r.font.size = Pt(9.5)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY   # Refinement #4
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after  = Pt(1)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf.read()


def generate_pdf(cv_text: str) -> bytes:
    if not REPORTLAB_OK:
        return b""
    buf    = io.BytesIO()
    doc_rl = SimpleDocTemplate(buf, pagesize=A4,
        topMargin=2.4*cm, bottomMargin=2.0*cm,
        leftMargin=2.2*cm, rightMargin=2.2*cm)

    NAVY = colors.HexColor("#1A2340")
    GOLD = colors.HexColor("#B8964A")
    DARK = colors.HexColor("#222222")
    GREY = colors.HexColor("#555555")
    BOLD_BLUE = colors.HexColor("#1A356B")

    name_sty = ParagraphStyle("N", fontName="Helvetica-Bold",
        fontSize=19, textColor=NAVY, alignment=TA_CENTER,
        spaceAfter=3, spaceBefore=0, leading=22)
    cont_sty = ParagraphStyle("C", fontName="Helvetica",
        fontSize=9, textColor=GREY, alignment=TA_CENTER,
        spaceAfter=8, spaceBefore=0, leading=13)
    sec_sty  = ParagraphStyle("S", fontName="Helvetica-Bold",
        fontSize=9.5, textColor=NAVY, spaceBefore=9,
        spaceAfter=2, leading=12)
    # Refinement #4: Justified body text
    body_sty = ParagraphStyle("B", fontName="Helvetica",
        fontSize=9.5, textColor=DARK, spaceAfter=1,
        spaceBefore=0, leading=13, alignment=TA_JUSTIFY)
    bull_sty = ParagraphStyle("Bul", fontName="Helvetica",
        fontSize=9.5, textColor=DARK, leftIndent=12,
        spaceAfter=1, spaceBefore=0, leading=13,
        alignment=TA_JUSTIFY)  # Refinement #4

    name, contact = _parse_header(cv_text)
    story = []

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(name.upper(), name_sty))
    if contact:
        story.append(Paragraph(contact, cont_sty))
    story.append(HRFlowable(width="100%", thickness=1,
                             color=GOLD, spaceBefore=2, spaceAfter=8))

    lines = cv_text.split("\n")
    in_header = True
    body_start = 0
    for i, line in enumerate(lines):
        s = line.strip()
        if in_header and s in (name, contact, ""):
            body_start = i + 1
        else:
            in_header = False

    in_experience_section = False

    for line in lines[body_start:]:
        s = line.strip()
        if not s:
            story.append(Spacer(1, 2))
            continue

        if s.isupper() and len(s) < 55 and not s.startswith("•"):
            story.append(HRFlowable(width="100%", thickness=0.4,
                                    color=GOLD, spaceBefore=5, spaceAfter=2))
            story.append(Paragraph(s, sec_sty))
            in_experience_section = "EXPERIENCE" in s.upper()

        elif s.startswith("•") or s.startswith("-"):
            story.append(Paragraph(f"• {s.lstrip('•- ').strip()}", bull_sty))

        elif in_experience_section and "|" in s:
            # Refinement #4: Bold company + dates in experience header lines
            m = _EXP_LINE_RE.match(s)
            if m:
                company, title, dates = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
                exp_html = (
                    f'<b><font color="#1A356B">{company}</font></b>'
                    f' | {title} | '
                    f'<b>{dates}</b>'
                )
                exp_sty = ParagraphStyle("Exp", fontName="Helvetica",
                    fontSize=9.5, textColor=DARK,
                    spaceBefore=4, spaceAfter=1, leading=13)
                story.append(Paragraph(exp_html, exp_sty))
            else:
                story.append(Paragraph(s, body_sty))
        else:
            story.append(Paragraph(s, body_sty))

    doc_rl.build(story)
    buf.seek(0)
    return buf.read()


# ════════════════════════════════════════════════════════════
#  RAZORPAY
# ════════════════════════════════════════════════════════════
def razorpay_link():
    try:
        return st.secrets["RAZORPAY_PAYMENT_LINK"]
    except Exception:
        return os.environ.get("RAZORPAY_PAYMENT_LINK", "https://rzp.io/l/tailormycv-demo")


# ════════════════════════════════════════════════════════════
#  UI COMPONENTS
# ════════════════════════════════════════════════════════════
def render_masthead():
    st.markdown("""
    <div class="masthead">
      <div class="masthead-logo">Tailor<span class="accent">My</span>CV</div>
      <div class="masthead-sub">AI-Powered Resume Intelligence for Success-Driven Professionals</div>
      <div class="masthead-badges">
        <span class="mbadge">Claude AI</span>
        <span class="mbadge">ATS-Scored</span>
        <span class="mbadge">100% Truthful</span>
        <span class="mbadge">₹20 / Download</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_step_bar(current):
    steps = ["Upload CV", "Job Description", "Your Details", "Choose Mode", "Results"]
    pills = ""
    for i, label in enumerate(steps, 1):
        cls  = "done" if i < current else ("active" if i == current else "")
        icon = "✓" if i < current else str(i)
        pills += f'<div class="step-pill {cls}">{icon} {label}</div>'
        if i < len(steps):
            pills += '<div class="step-connector"></div>'
    st.markdown(f'<div class="step-bar">{pills}</div>', unsafe_allow_html=True)


def render_ats(score, color, bar_color, gap):
    """Refinement #3: Gap text rendered as icon-prefixed bullet list."""
    gap_html = _gap_to_bullets_html(gap)
    st.markdown(f"""
    <div class="ats-wrap">
      <div class="ats-header">
        <div class="ats-label">ATS Compatibility Score</div>
        <div class="ats-num {color}">{score}%</div>
      </div>
      <div class="ats-track">
        <div class="ats-fill" style="width:{score}%;background:{bar_color};"></div>
      </div>
      <div class="ats-gap">
        <strong>What's missing for this role?</strong>
        {gap_html}
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Refinement #6: Social Sharing component ──────────────────
def render_social_sharing():
    wa_msg  = f"I just tailored my CV with AI on TailorMyCV — try it for ₹20! {APP_URL}"
    wa_url  = f"https://wa.me/?text={wa_msg.replace(' ', '%20').replace('!', '%21')}"
    ig_url  = "https://www.instagram.com/"  # Replace with your IG profile handle URL

    copy_js = f"""
    <script>
    function copyAppUrl() {{
      navigator.clipboard.writeText('{APP_URL}').then(function() {{
        var btn = document.getElementById('copy-btn');
        var orig = btn.innerHTML;
        btn.innerHTML = '✅ Copied!';
        setTimeout(function(){{ btn.innerHTML = orig; }}, 2000);
      }});
    }}
    </script>
    """
    st.markdown(copy_js, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="share-row">
      <div class="share-title">🤝 Share TailorMyCV with Friends</div>
      <div class="share-btns">
        <button id="copy-btn" class="share-btn share-btn-copy" onclick="copyAppUrl()">
          🔗 Copy URL
        </button>
        <a href="{wa_url}" target="_blank" class="share-btn share-btn-wa">
          💬 WhatsApp
        </a>
        <a href="{ig_url}" target="_blank" class="share-btn share-btn-ig">
          📸 Instagram
        </a>
      </div>
    </div>
    """, unsafe_allow_html=True)


CONFETTI_JS = """
<canvas id="confetti-canvas"></canvas>
<script>
(function(){
  var canvas = document.getElementById('confetti-canvas');
  var ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  var pieces = [];
  var colors = ['#C9A84C','#34D399','#3B82F6','#F87171','#E8C97A','#2DD4BF','#ffffff'];
  for(var i=0;i<160;i++){
    pieces.push({
      x: Math.random()*canvas.width,
      y: Math.random()*canvas.height - canvas.height,
      r: Math.random()*6+3,
      d: Math.random()*160+40,
      color: colors[Math.floor(Math.random()*colors.length)],
      tilt: Math.floor(Math.random()*10)-10,
      tiltAngle: 0, tiltAngleInc: Math.random()*0.07+0.05,
      alpha: 1
    });
  }
  var angle = 0, tick = 0;
  function draw(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    angle += 0.01;
    tick++;
    for(var i=0;i<pieces.length;i++){
      var p = pieces[i];
      p.tiltAngle += p.tiltAngleInc;
      p.y += (Math.cos(angle+p.d)+1+p.r/6)*1.4;
      p.x += Math.sin(angle)*1.5;
      p.tilt = Math.sin(p.tiltAngle)*12;
      if(tick > 200) p.alpha -= 0.008;
      ctx.globalAlpha = Math.max(0, p.alpha);
      ctx.beginPath();
      ctx.lineWidth = p.r/2;
      ctx.strokeStyle = p.color;
      ctx.moveTo(p.x+p.tilt+p.r/4, p.y);
      ctx.lineTo(p.x+p.tilt, p.y+p.tilt+p.r/4);
      ctx.stroke();
      if(p.y > canvas.height+20){ p.y=-10; p.x=Math.random()*canvas.width; p.alpha=1; }
    }
    ctx.globalAlpha = 1;
    if(tick < 280) requestAnimationFrame(draw);
    else ctx.clearRect(0,0,canvas.width,canvas.height);
  }
  draw();
})();
</script>
"""


# ════════════════════════════════════════════════════════════
#  STEPS
# ════════════════════════════════════════════════════════════

# ── Step 1: Upload CV + Auto-Fill (Refinement #1) ────────────
def page_step1():
    st.markdown('<div class="card"><div class="card-title">📄 Upload or Paste Your CV</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">Upload a PDF or DOCX, or paste your text below. Your Name and Email will be auto-detected.</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload CV (PDF or DOCX)", type=["pdf","docx"], label_visibility="collapsed")
    if uploaded:
        raw = uploaded.read()
        txt = extract_pdf(raw) if uploaded.name.lower().endswith(".pdf") else extract_docx_text(raw)
        if txt.strip():
            st.session_state.cv_text = txt
            st.success(f"✅ Extracted **{len(txt.split())}** words from `{uploaded.name}`")
        else:
            st.warning("Could not auto-extract — please paste your CV below.")

    cv_in = st.text_area("Or paste your CV text here:",
        value=st.session_state.cv_text, height=200,
        placeholder="Paste your full CV — name, contact, experience, education, skills…")
    st.session_state.cv_text = cv_in
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Continue → Paste Job Description", use_container_width=True):
        if len(st.session_state.cv_text.strip()) < 50:
            st.error("Please provide your CV (minimum 50 characters).")
        else:
            # ── Refinement #1: Auto-extract name and email from CV ──
            extracted_name  = _extract_name_from_cv(st.session_state.cv_text)
            extracted_email = _extract_email_from_cv(st.session_state.cv_text)
            # Pre-fill session state (user can override in Step 3)
            if extracted_name and not st.session_state.lead_name:
                st.session_state.lead_name  = extracted_name
            if extracted_email and not st.session_state.lead_email:
                st.session_state.lead_email = extracted_email
            st.session_state.step = 2
            st.rerun()


# ── Step 2: Job Description ────────────────────────────────
def page_step2():
    st.markdown('<div class="card"><div class="card-title">🎯 Paste the Job Description</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">Copy the full JD from LinkedIn, Naukri, or any job portal. More detail = better match.</div>', unsafe_allow_html=True)

    jd_in = st.text_area("Job Description:",
        value=st.session_state.jd_text, height=220,
        placeholder="Paste the complete job description — role summary, responsibilities, required skills…")
    st.session_state.jd_text = jd_in
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = 1; st.rerun()
    with c2:
        if st.button("Continue → Your Details", use_container_width=True):
            if len(st.session_state.jd_text.strip()) < 50:
                st.error("Please paste the job description (minimum 50 characters).")
            else:
                # ── Refinement #1: silently extract role + company from JD ──
                st.session_state.jd_role    = _guess_role(st.session_state.jd_text)
                st.session_state.jd_company = _guess_company(st.session_state.jd_text)
                st.session_state.step = 3
                st.rerun()


# ── Step 3: Lead Capture + Confirm Details (Refinement #1) ───
def page_step3():
    st.markdown('<div class="card"><div class="card-title">✉️ Confirm Your Details</div>', unsafe_allow_html=True)

    # ── Refinement #1: Show auto-filled badge if we pre-populated ──
    has_autofill = bool(st.session_state.lead_name or st.session_state.lead_email)
    if has_autofill and not st.session_state.details_confirmed:
        st.markdown(
            '<div class="info-box">✨ <strong>Auto-filled from your CV!</strong> '
            'Please review and confirm these details before continuing.</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="info-box">Enter your details below — we\'ll personalise your experience.</div>',
            unsafe_allow_html=True
        )

    name_in  = st.text_input(
        "Full Name *",
        value=st.session_state.lead_name,
        placeholder="e.g. Priya Sharma",
    )
    email_in = st.text_input(
        "Email Address *",
        value=st.session_state.lead_email,
        placeholder="e.g. priya@gmail.com",
    )

    st.session_state.lead_name  = name_in.strip()
    st.session_state.lead_email = email_in.strip()

    # Show what we extracted silently from the JD
    if st.session_state.jd_role and st.session_state.jd_role != "Professional":
        st.markdown(f"""
        <div class="gold-box" style="margin-top:0.6rem; font-size:0.78rem;">
          🎯 <strong>Target Role detected:</strong> {st.session_state.jd_role}
          {(' &nbsp;·&nbsp; 🏢 <strong>Company:</strong> ' + st.session_state.jd_company) if st.session_state.jd_company else ''}
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = 2; st.rerun()
    with c2:
        btn_label = "✅ Confirm & Continue" if has_autofill else "Continue → Choose Mode"
        if st.button(btn_label, use_container_width=True):
            if not st.session_state.lead_name:
                st.error("Please enter your full name."); return
            email_pat = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
            if not re.match(email_pat, st.session_state.lead_email):
                st.error("Please enter a valid email address."); return
            st.session_state.lead_captured    = True
            st.session_state.details_confirmed = True
            st.session_state.step = 4
            st.rerun()

    if st.session_state.lead_captured:
        st.markdown(f"""
        <div class="lead-box">
          ✅ Lead Captured: <strong>{st.session_state.lead_name}</strong>
          — {st.session_state.lead_email}
        </div>
        """, unsafe_allow_html=True)


# ── Step 4: Tailoring Mode ─────────────────────────────────
def page_step4():
    st.markdown('<div class="card"><div class="card-title">⚙️ Select Your Tailoring Strategy</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for idx, (key, meta) in enumerate(MODE_META.items()):
        with cols[idx]:
            sel = st.session_state.mode == key
            st.markdown(f"""
            <div class="mode-card {'sel' if sel else ''}">
              <div class="mode-icon">{meta['icon']}</div>
              <div class="mode-label">{key}</div>
              <div class="mode-desc">{meta['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✓ Selected" if sel else "Select", key=f"m_{key}", use_container_width=True):
                st.session_state.mode = key; st.rerun()

    st.markdown(f"""
    <div class="gold-box" style="margin-top:0.9rem;">
      ◆ &nbsp;<strong>{st.session_state.mode}</strong> — {MODE_META[st.session_state.mode]['desc']}
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = 3; st.rerun()
    with c2:
        if st.button("◆ Generate My Tailored CV", use_container_width=True):
            with st.spinner("🤖 Analysing your CV against the job description…"):
                try:
                    result = call_claude(
                        st.session_state.cv_text,
                        st.session_state.jd_text,
                        st.session_state.mode,
                    )
                    st.session_state.tailored_cv   = result["cv_text"]
                    st.session_state.ats_score     = result["score"]
                    st.session_state.ats_color     = result["color"]
                    st.session_state.ats_bar_color = result["bar_color"]
                    st.session_state.gap_analysis  = result["gap"]
                    st.session_state.step          = 5
                    st.rerun()
                except anthropic.AuthenticationError:
                    st.error("❌ Invalid API key — check Streamlit Secrets → ANTHROPIC_API_KEY.")
                except anthropic.NotFoundError:
                    st.error(f"❌ Model '{CLAUDE_MODEL}' unavailable. Check your Anthropic account.")
                except Exception as e:
                    st.error(f"❌ Generation failed: {e}")


# ── Step 5: Results & Payment Gate ────────────────────────
def page_step5():
    # Confetti on first load
    if not st.session_state.confetti_fired:
        st.markdown(CONFETTI_JS, unsafe_allow_html=True)
        st.session_state.confetti_fired = True

    # ATS Score — always visible (Refinement #3 applied inside render_ats)
    if st.session_state.ats_score is not None:
        render_ats(
            st.session_state.ats_score,
            st.session_state.ats_color,
            st.session_state.ats_bar_color,
            st.session_state.gap_analysis,
        )

    st.markdown(f"""
    <div class="card" style="margin-bottom:0.5rem;">
      <div class="card-title">
        📋 Your Tailored CV
        <span class="badge">{st.session_state.mode}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PAYMENT GATE ──────────────────────────────────────
    if not st.session_state.payment_verified:
        preview = st.session_state.tailored_cv[:300] + "\n\n… [Full content locked — unlock below]"
        st.text_area("Preview (locked):", value=preview, height=130,
                     disabled=True, label_visibility="collapsed")

        st.markdown("""
        <div class="warn-box">
          🔒 Your CV is ready and ATS-scored. Pay <strong>₹20</strong> to unlock
          the full editable content + Word &amp; PDF downloads.
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="pay-btn-wrap">
          <a href="{razorpay_link()}" target="_blank" class="pay-btn">
            💳 &nbsp; Pay ₹20 — Unlock Full CV + Downloads
          </a>
        </div>
        <p style="text-align:center;font-size:0.75rem;color:#566D84;margin-top:0.55rem;">
          Secure · Razorpay · UPI · Cards · Net Banking · Wallets
        </p>
        """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("**Already paid?** Confirm below to unlock your files.")
        _, mid, _ = st.columns([1, 2, 1])
        with mid:
            if st.button("✅ I've Paid — Unlock Now", use_container_width=True):
                st.session_state.payment_verified = True; st.rerun()

    else:
        # ════ UNLOCKED ════════════════════════════════════
        st.markdown(
            f'<div class="success-box">✅ Unlocked, {st.session_state.lead_name}! '
            f'Edit below, then download your tailored CV.</div>',
            unsafe_allow_html=True
        )

        edited = st.text_area("Fine-tune your CV if needed:",
                               value=st.session_state.tailored_cv, height=400)
        st.session_state.tailored_cv = edited

        st.markdown(
            '<span class="badge">✓ ATS-Optimised</span>'
            '<span class="badge">✓ Truthful to Original</span>'
            '<span class="badge">✓ Action Verbs</span>'
            '<span class="badge">✓ Quantified Impact</span>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="warn-box">
          💡 <strong>Tip:</strong> Use the <strong>Word (.docx)</strong> file
          for application portals. Use PDF for email or direct submissions.
        </div>
        """, unsafe_allow_html=True)

        # ── Download buttons — Refinement #2: Icons + Teal/Red ───
        fname = st.session_state.mode.replace(" ", "-")
        c_docx, c_pdf = st.columns(2)

        with c_docx:
            st.markdown('<div class="dl-word">', unsafe_allow_html=True)
            docx_bytes = generate_docx(st.session_state.tailored_cv)
            if st.download_button(
                "📄  Download Word (.docx)",       # Refinement #2: 📄 icon
                data=docx_bytes,
                file_name=f"TailorMyCV_{fname}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            ):
                st.session_state.downloaded = True
            st.markdown('</div>', unsafe_allow_html=True)

        with c_pdf:
            st.markdown('<div class="dl-pdf">', unsafe_allow_html=True)
            if REPORTLAB_OK:
                pdf_bytes = generate_pdf(st.session_state.tailored_cv)
                if st.download_button(
                    "📥  Download PDF",             # Refinement #2: 📥 icon
                    data=pdf_bytes,
                    file_name=f"TailorMyCV_{fname}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                ):
                    st.session_state.downloaded = True
            else:
                st.markdown('<div class="info-box">Add <code>reportlab</code> to requirements.txt for PDF export.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Morale Booster — Refinement #5: name + role personalised ──
        if st.session_state.downloaded:
            if st.session_state.morale_msg is None:
                icon, tpl = random.choice(MORALE_TEMPLATES)
                name = st.session_state.lead_name or "Candidate"
                role = st.session_state.jd_role   or "Professional"
                st.session_state.morale_msg = (icon, tpl.format(name=name, role=role))
            icon, msg = st.session_state.morale_msg
            st.markdown(f"""
            <div class="morale-card">
              <div class="morale-icon">{icon}</div>
              <div class="morale-text">"{msg}"</div>
            </div>
            """, unsafe_allow_html=True)

            # Referral box
            st.markdown("""
            <div class="referral-box">
              Know someone who deserves a job they love? 🤝<br>
              <strong>Share TailorMyCV</strong> with a friend, colleague, or batchmate —
              help them land their next role for just ₹20.
            </div>
            """, unsafe_allow_html=True)

            # ── Social Sharing — Refinement #6 ──
            render_social_sharing()

    # ── Navigation ─────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        if st.button("← Regenerate", use_container_width=True):
            for k in ("tailored_cv","payment_verified","downloaded",
                      "morale_msg","confetti_fired","ats_score"):
                st.session_state[k] = DEFAULTS[k]
            st.session_state.step = 4; st.rerun()
    with c2:
        if st.button("◆ Start Fresh (New CV)", use_container_width=True):
            for k, v in DEFAULTS.items():
                st.session_state[k] = v
            st.rerun()


# ════════════════════════════════════════════════════════════
#  MAIN ROUTER
# ════════════════════════════════════════════════════════════
def main():
    render_masthead()
    render_step_bar(st.session_state.step)

    if   st.session_state.step == 1: page_step1()
    elif st.session_state.step == 2: page_step2()
    elif st.session_state.step == 3: page_step3()
    elif st.session_state.step == 4: page_step4()
    elif st.session_state.step == 5: page_step5()

if __name__ == "__main__":
    main()
