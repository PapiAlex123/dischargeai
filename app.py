# app.py  —  Discharge Planning Coordinator  |  Streamlit UI
# Run: streamlit run app.py
import os, json
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DischargeAI — Discharge Planning Coordinator",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

/* Background — clean white */
.stApp { background: #f8f9fb; }
section[data-testid="stSidebar"] { background: #ffffff !important; border-right: 1px solid #e5e7eb; }

/* Hero banner */
.hero {
    background: linear-gradient(135deg, #1e40af 0%, #2563eb 40%, #1d4ed8 100%);
    border: none;
    border-radius: 20px;
    padding: 40px 48px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(37,99,235,0.25);
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(255,255,255,0.08) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.4em;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
}
.hero-sub {
    font-size: 1.05em;
    color: rgba(255,255,255,0.8);
    margin: 0;
}
.hero-badges {
    margin-top: 16px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}
.badge {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    color: #ffffff;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78em;
    font-weight: 500;
}

/* Agent status cards */
.agent-grid { display: flex; gap: 10px; flex-wrap: wrap; margin: 16px 0; }
.agent-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 12px 16px;
    flex: 1;
    min-width: 120px;
    text-align: center;
    transition: all 0.3s;
}
.agent-card.active {
    border-color: #2563eb;
    background: #eff6ff;
    box-shadow: 0 0 16px rgba(37,99,235,0.15);
}
.agent-card.done {
    border-color: #16a34a;
    background: #f0fdf4;
}
.agent-icon { font-size: 1.6em; margin-bottom: 4px; }
.agent-name { font-size: 0.7em; color: #6b7280; font-weight: 500; }

/* Input area */
.stTextArea textarea {
    background: #ffffff !important;
    border: 1px solid #d1d5db !important;
    border-radius: 12px !important;
    color: #111827 !important;
    font-size: 0.9em !important;
    line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95em !important;
    padding: 12px 24px !important;
    transition: all 0.2s !important;
    width: 100% !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.25) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(37,99,235,0.35) !important;
}

/* Metrics */
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
[data-testid="metric-container"] label { color: #6b7280 !important; font-size: 0.78em !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #1d4ed8 !important;
    font-size: 1.3em !important;
    font-weight: 600 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #f3f4f6;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #e5e7eb;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #6b7280;
    font-weight: 500;
    font-size: 0.85em;
    padding: 8px 16px;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: #2563eb !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.3) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 24px;
    margin-top: 8px;
}

/* Content display */
.content-box {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 20px;
    color: #111827;
    line-height: 1.75;
    font-size: 0.9em;
}

/* Progress bar */
.stProgress > div > div { background: #2563eb !important; border-radius: 4px !important; }

/* Selectbox, text_input */
.stSelectbox select, .stTextInput input {
    background: #ffffff !important;
    border: 1px solid #d1d5db !important;
    color: #111827 !important;
    border-radius: 8px !important;
}

/* Checkbox */
.stCheckbox { color: #374151; }

/* Divider */
hr { border-color: #e5e7eb !important; }

/* Sidebar labels */
.stSidebar .stMarkdown { color: #374151; }

/* Final plan special */
.final-plan {
    background: linear-gradient(135deg, #eff6ff, #f8faff);
    border: 1px solid #bfdbfe;
    border-radius: 16px;
    padding: 28px;
    color: #111827;
    line-height: 1.8;
}

/* Download buttons */
.stDownloadButton > button {
    background: #ffffff !important;
    color: #2563eb !important;
    border: 1px solid #d1d5db !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}
.stDownloadButton > button:hover {
    border-color: #2563eb !important;
    background: #eff6ff !important;
}

/* Warning alert */
.warning-box {
    background: #fffbeb;
    border: 1px solid #fcd34d;
    border-radius: 10px;
    padding: 12px 16px;
    color: #92400e;
    font-size: 0.85em;
    margin-bottom: 12px;
}

/* Success box */
.success-box {
    background: #f0fdf4;
    border: 1px solid #86efac;
    border-radius: 10px;
    padding: 12px 16px;
    color: #166534;
    font-size: 0.85em;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ── Hero Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">🏥 DischargeAI</div>
  <div style="font-size:1.3em;color:#ffffff;font-weight:600;margin-bottom:4px;">
    Discharge Planning Coordinator
  </div>
  <div class="hero-sub">
    Multi-Agent Healthcare AI · 7 Specialist Agents · FHIR R4 · MCP Compatible · Prompt Opinion Ready
  </div>
  <div class="hero-badges">
    <span class="badge">🤖 Groq LLaMA 3.3 70B</span>
    <span class="badge">🔌 FHIR R4</span>
    <span class="badge">🔧 MCP Server</span>
    <span class="badge">🏆 Agents Assemble Hackathon</span>
    <span class="badge">⚡ Real-time Multi-Agent</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔑 API Configuration")
    groq_key = st.text_input(
        "Groq API Key",
        value=os.getenv("GROQ_API_KEY", ""),
        type="password",
        help="Get free at console.groq.com",
    )
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key

    st.divider()
    st.markdown("## 🔌 FHIR Integration")
    use_fhir = st.checkbox("Connect to FHIR Server", value=False)
    fhir_patient_id = ""
    fhir_base_url   = "https://hapi.fhir.org/baseR4"
    fhir_token      = ""

    if use_fhir:
        fhir_patient_id = st.text_input("Patient ID", value="592442",
            help="Browse patients: hapi.fhir.org/baseR4/Patient")
        fhir_base_url   = st.text_input("FHIR Server URL", value="https://hapi.fhir.org/baseR4")
        fhir_token      = st.text_input("Auth Token (optional)", type="password")

    st.divider()
    st.markdown("## 💳 Patient Insurance")
    insurance_type = st.selectbox("Insurance Type", [
        "Medicare", "Medicaid", "Medicare + Medicaid (Dual Eligible)",
        "Commercial / Private", "VA / Tricare", "Self-Pay / Uninsured",
    ])

    st.divider()
    st.markdown("## 🤖 Active Agents")
    AGENTS = [
        ("💊", "Medication"),
        ("🚨", "Warning Signs"),
        ("📅", "Follow-Up"),
        ("📚", "Education"),
        ("🏥", "Facility"),
        ("💳", "Insurance"),
        ("📊", "Risk"),
        ("🧠", "Coordinator"),
    ]
    for icon, name in AGENTS:
        st.markdown(f"&nbsp;&nbsp;{icon} **{name} Agent**", unsafe_allow_html=True)

    st.divider()
    st.caption("Built for **Agents Assemble** Hackathon  \nPowered by Groq · FHIR · MCP")

# ── Sample Note ────────────────────────────────────────────────────────────────
SAMPLE_NOTE = """Patient: Robert Johnson, 72-year-old male.
Admitted for acute exacerbation of congestive heart failure (CHF) with reduced ejection fraction (EF 30%).

Hospital Course: Presented with 3-day dyspnea, bilateral lower extremity edema (2+ pitting), and 6-lb weight gain. BNP 1,450 pg/mL. CXR: bilateral pleural effusions, pulmonary vascular congestion. Treated with IV furosemide 40mg BID — 4.8L net diuresis over 3 days. Transitioned to oral furosemide. Lisinopril increased from 5mg to 10mg. Carvedilol continued.

Discharge Medications:
- Furosemide (Lasix) 40mg PO daily
- Lisinopril 10mg PO daily (DOSE INCREASED — was 5mg, watch for dizziness)
- Carvedilol 12.5mg PO BID
- Spironolactone 25mg PO daily
- Atorvastatin 40mg PO nightly
- Aspirin 81mg PO daily
- Potassium Chloride 20mEq PO daily

Discharge to: Skilled Nursing Facility (SNF) for cardiac monitoring, PT/OT, and medication optimization.

Follow-Up: Cardiology in 1 week. PCP in 3 days. BMP in 5 days. Daily weights at SNF.

Warning Signs — Return to ED if: weight gain >2 lbs overnight or >5 lbs/week, worsening shortness of breath, chest pain, O2 sat <92%, new confusion.

Diet: Low-sodium <2g/day. Fluid restriction 1.5L/day. Activity: light ambulation only.
Allergies: Penicillin (rash)."""

# ── Main Input Area ────────────────────────────────────────────────────────────
col_title, col_btn = st.columns([3, 1])
with col_title:
    st.markdown("### 📋 Discharge Summary Input")
with col_btn:
    if st.button("📄 Load CHF Sample", use_container_width=True):
        st.session_state["note"] = SAMPLE_NOTE

discharge_note = st.text_area(
    "Paste the hospital discharge summary below",
    value=st.session_state.get("note", ""),
    height=200,
    placeholder="Paste any hospital discharge summary here — medications, follow-up instructions, warning signs, disposition...",
    label_visibility="collapsed",
)

# ── Run Button ─────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
run_col, _, _ = st.columns([1, 1, 1])
with run_col:
    run = st.button("🚀 Generate Discharge Intelligence Plan", use_container_width=True)

# ── Processing ─────────────────────────────────────────────────────────────────
if run:
    if not os.getenv("GROQ_API_KEY"):
        st.error("❌ Enter your Groq API Key in the sidebar first.")
        st.stop()
    if not discharge_note.strip():
        st.warning("⚠️ Paste a discharge note or click 'Load CHF Sample'.")
        st.stop()

    from agents.coordinator_agent import DischargePlanningCoordinator

    # FHIR context
    patient_ctx = {}
    if use_fhir and fhir_patient_id:
        with st.spinner("🔌 Fetching patient data from FHIR server..."):
            try:
                from fhir_utils import build_patient_context
                patient_ctx = build_patient_context(
                    fhir_patient_id, fhir_base_url, fhir_token or None)
                st.markdown(f"""<div class="success-box">
                ✅ FHIR data loaded — Patient: <strong>{patient_ctx.get('name','Unknown')}</strong>
                 | Conditions: {len(patient_ctx.get('conditions',[]))} 
                 | Medications: {len(patient_ctx.get('medications',[]))}
                </div>""", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="warning-box">⚠️ FHIR fetch failed — running on note only. ({e})</div>',
                           unsafe_allow_html=True)

    # Progress UI
    st.markdown("---")
    st.markdown("### ⚙️ Agent Pipeline Running")
    progress  = st.progress(0)
    status    = st.empty()
    agent_status = st.empty()

    agent_states = {a: "waiting" for _, a in AGENTS}

    def update(label: str, pct: int):
        progress.progress(pct / 100)
        status.markdown(f"**{label}**")
        # Update agent state display
        icons = {"waiting": "⏳", "active": "🔵", "done": "✅"}
        names = [n for _, n in AGENTS]
        done_count = int(pct / (100 / len(names)))
        cols_html = ""
        for i, (icon, aname) in enumerate(AGENTS):
            if i < done_count:
                state = "done"; si = "✅"
            elif i == done_count:
                state = "active"; si = "🔵"
            else:
                state = "waiting"; si = "⏳"
            cols_html += f"""
            <div class="agent-card {state}">
                <div class="agent-icon">{icon}</div>
                <div class="agent-name">{aname}</div>
                <div style="font-size:1.1em">{si}</div>
            </div>"""
        agent_status.markdown(
            f'<div class="agent-grid">{cols_html}</div>', unsafe_allow_html=True)

    coordinator = DischargePlanningCoordinator()
    results = coordinator.run(
        discharge_note=discharge_note,
        patient_context=patient_ctx,
        insurance_type=insurance_type,
        progress_callback=update,
    )

    progress.progress(1.0)
    status.markdown("**✅ All 7 agents complete — Discharge Intelligence Plan ready!**")
    st.session_state["results"] = results
    st.balloons()

# ── Results ────────────────────────────────────────────────────────────────────
if "results" in st.session_state:
    res  = st.session_state["results"]
    meta = res.get("metadata", {})

    st.markdown("---")
    st.markdown("### 📊 Session Overview")

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Patient",      meta.get("patient_name", "—"))
    m2.metric("Patient ID",   meta.get("patient_id", "—"))
    m3.metric("Insurance",    meta.get("insurance", "—"))
    m4.metric("Agents Run",   meta.get("agents_run", "—"))
    m5.metric("Conditions",   meta.get("conditions_count", "—"))
    m6.metric("Time",         meta.get("processing_time", "—"))

    st.markdown("---")
    st.markdown("### 📋 Discharge Intelligence Report")

    tabs = st.tabs([
        "🧠 Final Plan",
        "💊 Medications",
        "🚨 Warning Signs",
        "📅 Follow-Up",
        "📚 Caregiver Guide",
        "🏥 Facilities",
        "💳 Insurance",
        "📊 Risk Assessment",
    ])

    # Final plan gets special styling
    with tabs[0]:
        st.markdown("#### 🧠 Discharge Intelligence Plan — Coordinator Synthesis")
        st.markdown(
            f'<div class="final-plan">{res.get("final_plan","").replace(chr(10),"<br>")}</div>',
            unsafe_allow_html=True)

    sections = [
        (1, "💊 Medication Analysis",         "medications"),
        (2, "🚨 Warning Signs & Safety Alerts","warnings"),
        (3, "📅 Follow-Up & Recovery Plan",    "followup"),
        (4, "📚 Caregiver Education Guide",    "education"),
        (5, "🏥 Facility Recommendations",     "facilities"),
        (6, "💳 Insurance Coverage",           "insurance"),
        (7, "📊 Readmission Risk Assessment",  "risk"),
    ]

    for idx, title, key in sections:
        with tabs[idx]:
            st.markdown(f"#### {title}")
            st.markdown(res.get(key, "No output available."))

    # ── Downloads ──────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📥 Export Discharge Plan")

    full_report = f"""DISCHARGE INTELLIGENCE PLAN
Generated by DischargeAI — Discharge Planning Coordinator
Patient: {meta.get('patient_name','N/A')}  |  Insurance: {meta.get('insurance','N/A')}
FHIR Source: {meta.get('fhir_source','Manual input')}
{'='*80}

{res.get('final_plan','')}

{'='*80}
MEDICATIONS
{'='*80}
{res.get('medications','')}

{'='*80}
WARNING SIGNS
{'='*80}
{res.get('warnings','')}

{'='*80}
FOLLOW-UP PLAN
{'='*80}
{res.get('followup','')}

{'='*80}
CAREGIVER EDUCATION
{'='*80}
{res.get('education','')}

{'='*80}
FACILITY RECOMMENDATIONS
{'='*80}
{res.get('facilities','')}

{'='*80}
INSURANCE COVERAGE
{'='*80}
{res.get('insurance','')}

{'='*80}
READMISSION RISK ASSESSMENT
{'='*80}
{res.get('risk','')}
"""

    dl1, dl2 = st.columns(2)
    pname = meta.get("patient_name","patient").replace(" ","_")
    with dl1:
        st.download_button(
            "📄 Download Full Report (.txt)",
            data=full_report,
            file_name=f"discharge_plan_{pname}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with dl2:
        st.download_button(
            "📊 Download Raw Data (.json)",
            data=json.dumps(
                {k: v for k, v in res.items() if k != "metadata"}, indent=2),
            file_name=f"discharge_data_{pname}.json",
            mime="application/json",
            use_container_width=True,
        )

    st.markdown("""
<div style="background:#fffbeb;border:1px solid #fcd34d;border-radius:10px;padding:12px 16px;margin-top:16px;color:#92400e;font-size:0.82em;">
⚕️ <strong>Clinical Disclaimer:</strong> This AI-generated plan is for decision support only. 
All outputs require physician review and clinical judgment before implementation. 
Not a substitute for professional medical advice. Uses synthetic/test data only — not for use with real PHI.
</div>""", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#9ca3af;font-size:0.8em;padding:16px;">
  🏥 DischargeAI — Discharge Planning Coordinator &nbsp;|&nbsp;
  Built for Agents Assemble Healthcare AI Hackathon &nbsp;|&nbsp;
  Groq LLaMA 3.3 70B · FHIR R4 · MCP · Prompt Opinion
</div>
""", unsafe_allow_html=True)
