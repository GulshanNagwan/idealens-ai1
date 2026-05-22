import streamlit as st
import google.genai as genai
import plotly.graph_objects as go
import json
import sqlite3
import re
from datetime import datetime

# ==============================================================================
# 1. DATA LAYER: RELATIONAL PERSISTENCE (SQLite3 Architecture)
# ==============================================================================
def init_db():
    """Initializes the structural SQL tracking framework table nodes."""
    conn = sqlite3.connect("idealens_bi.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venture_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            venture_name TEXT,
            industry TEXT,
            region TEXT,
            description TEXT,
            keyword_density REAL,
            algo_viability_score REAL,
            llm_payload TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_analysis(name, industry, region, desc, density, algo_score, payload_dict):
    """Persists real-time platform telemetry safely into relational tables."""
    conn = sqlite3.connect("idealens_bi.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO venture_logs 
        (timestamp, venture_name, industry, region, description, keyword_density, algo_viability_score, llm_payload)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        name, industry, region, desc, density, algo_score, json.dumps(payload_dict)
    ))
    conn.commit()
    conn.close()

def fetch_history():
    """Queries persistent tables to yield system execution history records."""
    conn = sqlite3.connect("idealens_bi.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, venture_name, industry, algo_viability_score FROM venture_logs ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    return records

def fetch_record_by_id(record_id):
    """Pulls a single precise raw evaluation payload dataset for deep indexing."""
    conn = sqlite3.connect("idealens_bi.db")
    cursor = conn.cursor()
    cursor.execute("SELECT venture_name, industry, region, description, keyword_density, algo_viability_score, llm_payload FROM venture_logs WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    return row

# Fire up database tables upon execution bootstrap sequence
init_db()

# ==============================================================================
# 2. COMPUTATION NODES: LOCAL METRIC SCORING & TEXT NLP PROCESSING
# ==============================================================================
def local_nlp_processor(text_input):
    """Performs static string scanning mapping key enterprise vocabulary weights."""
    business_keywords = [
        "platform", "scale", "market", "app", "service", "customer", "revenue", 
        "b2b", "saas", "user", "technology", "ai", "automation", "online", "digital"
    ]
    tokens = re.findall(r'\b\w+\b', text_input.lower())
    if not tokens:
        return 0.0
    matched_keywords = [t for t in tokens if t in business_keywords]
    density = (len(matched_keywords) / len(tokens)) * 100
    return round(density, 2)

def algorithmic_viability_matrix(budget_tier, team_capacity, keyword_density):
    """Computes a fixed base viability percentage matrix using static local code."""
    budget_score = {"Low (Bootstrap)": 65, "Medium (Angel/Seed)": 85, "High (VC Ready)": 95}.get(budget_tier, 50)
    team_score = {"1-2 Solo/Duet": 60, "3-5 Core Team": 85, "5+ Expanded Node": 95}.get(team_capacity, 50)
    
    # Mathematical compilation formulation
    base_score = (budget_score * 0.4) + (team_score * 0.4) + (min(keyword_density * 5, 100) * 0.2)
    return round(base_score, 1)

# ==============================================================================
# 3. INTERFACE WORKSPACE: HIGH-CONTRAST NEON CYBER-TERMINAL SPECIFICATION
# ==============================================================================
st.set_page_config(page_title="IdeaLens AI // Command Center", layout="wide")

st.markdown("""
    <style>
        .stApp {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: 'Courier New', Courier, monospace;
        }
        section[data-testid="stSidebar"] {
            background-color: #161b22 !important;
            border-right: 2px solid #00f2ff !important;
        }
        .terminal-card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-left: 4px solid #00f2ff;
            padding: 20px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .risk-card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-left: 4px solid #ff3e3e;
            padding: 20px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .neon-text {
            color: #00f2ff;
            text-shadow: 0 0 8px rgba(0, 242, 255, 0.3);
            font-weight: bold;
        }
        div[data-baseweb="textarea"], div[data-baseweb="input"], div[data-baseweb="select"] {
            background-color: #0d1117 !important;
            border: 1px solid #30363d !important;
        }
        textarea, input {
            color: #00f2ff !important;
            font-family: 'Courier New', Courier, monospace !important;
        }
        .stButton>button {
            background-color: #0d1117 !important;
            color: #00f2ff !important;
            border: 1px solid #00f2ff !important;
            width: 100%;
            font-weight: bold !important;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #00f2ff !important;
            color: #0d1117 !important;
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.5);
        }
    </style>
""", unsafe_allow_html=True)

# Secure Environment Configuration for Global API Client Engine
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not API_KEY:
    API_KEY = st.sidebar.text_input("SYSTEM: Input Gemini Key manually:", type="password")
client = genai.Client(api_key=API_KEY) if API_KEY else None

with st.sidebar:
    st.markdown("<h2 class='neon-text'>// IDEALENS AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem; color:#8b949e;'>CORE TELEMETRY ENGINE // v3.0</p>", unsafe_allow_html=True)
    st.markdown("---")
    workspace = st.radio("EXAMINER CONTROL NODES", ["🚀 Engine Diagnostics", "📂 Database Log Registry"])
    st.markdown("---")
    st.markdown("<div style='font-size:0.8rem; color:#8b949e;'>SYS STAT: <span style='color:#56d364;'>● ONLINE</span></div>", unsafe_allow_html=True)

# ==============================================================================
# PIPELINE CHANNEL 1: PROCESSING TELEMETRY ENGINE
# ==============================================================================
if workspace == "🚀 Engine Diagnostics":
    st.markdown("<h1 class='neon-text'>[ HYBRID SYSTEM INFERENCE ENGINE ]</h1>", unsafe_allow_html=True)
    
    with st.form("telemetry_input"):
        col1, col2 = st.columns(2)
        with col1:
            startup_name = st.text_input("Venture Code Identifier", value="Project_Alpha")
            industry = st.selectbox("Industry Node Segment", ["SaaS", "FinTech", "EdTech", "IoT/Hardware", "CleanTech"])
            budget = st.selectbox("Financial Resource Allocation", ["Low (Bootstrap)", "Medium (Angel/Seed)", "High (VC Ready)"])
        with col2:
            target_audience = st.text_input("Target Consumer Profile", value="Developers")
            region = st.text_input("Geographic Jurisdiction Node", value="India")
            team = st.selectbox("Human Capital Resource Capacity", ["1-2 Solo/Duet", "3-5 Core Team", "5+ Expanded Node"])
            
        idea_description = st.text_area("Venture Conceptual Manifest Text")
        submit_btn = st.form_submit_button("RUN DISTRIBUTED PROCESSING PIPELINE")

    if submit_btn:
        if not client:
            st.error("Exception Failure: Active Inference Engine API Connection Key context is null.")
        elif len(idea_description.strip()) < 15:
            st.error("Processing Terminated: Conceptual text validation constraints failed (String payload too short).")
        else:
            with st.spinner("Executing Local Token NLP Pipelines and Distributing Cloud Core Inference..."):
                try:
                    # Execute mathematical algorithms locally 
                    local_density = local_nlp_processor(idea_description)
                    calculated_viability = algorithmic_viability_matrix(budget, team, local_density)
                    
                    # Package structured query configuration logic prompt payload
                    master_prompt = f"""
                    You are the multi-agent analytics vector for the IdeaLens AI business intelligence platform.
                    Analyze this enterprise parameters payload:
                    Name: {startup_name} | Industry: {industry} | Region: {region} | Target: {target_audience}
                    Concept Context: {idea_description}
                    Local Algorithmic Score Calculated: {calculated_viability}%

                    Respond with a raw valid JSON object matching this structural constraint precisely. Do not include markdown ticks.
                    {{
                        "market_demand_score": 75,
                        "scalability_score": 80,
                        "market_demand_analysis": "Comprehensive textual market data breakdown.",
                        "competitor_analysis": "Deep evaluation of competitors.",
                        "strengths": ["Strategic Strength 1", "Strategic Strength 2"],
                        "weaknesses": ["Risk Factor 1", "Risk Factor 2"],
                        "opportunities": ["Growth Vector 1", "Growth Vector 2"],
                        "threats": ["Market Threat 1", "Market Threat 2"],
                        "monetization": ["Revenue Model 1", "Revenue Model 2"],
                        "technical_risks": "Local infrastructure operational system vulnerabilities analysis.",
                        "market_risks": "Competitive market performance pressure indicators.",
                        "elevator_pitch": "Structural highly-compelling 30-second venture presentation pitch."
                    }}
                    """
                    
                    # Fire query downstream to cloud api endpoint
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=master_prompt)
                    raw_json = response.text.strip().replace("```json", "").replace("```", "")
                    llm_data = json.loads(raw_json)
                    
                    # Commit and write execution logs directly to database 
                    save_analysis(startup_name, industry, region, idea_description, local_density, calculated_viability, llm_data)
                    
                    # Write dataset to active running session framework tracking state
                    st.session_state['active_analysis'] = (startup_name, industry, region, idea_description, local_density, calculated_viability, llm_data)
                    st.success("Distributed pipeline data transaction complete. Synchronization verified.")
                    
                except Exception as e:
                    st.error(f"Inference Architecture Failure Node: {str(e)}")

    # Interactive Dashboard Visualization Block
    if 'active_analysis' in st.session_state:
        name, ind, reg, desc, dens, algo_score, payload = st.session_state['active_analysis']
        st.markdown("---")
        st.markdown(f"<h2 class='neon-text'>// EVALUATION ANALYSIS TELEMETRY REPORT: {name}</h2>", unsafe_allow_html=True)
        
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.metric(label="[Local Code] NLP Keyword Density", value=f"{dens}%")
        with col_c2:
            st.metric(label="[Local Logic] Algorithmic Viability Index", value=f"{algo_score}%")
        with col_c3:
            st.metric(label="[Cloud Engine] Market Scalability Matrix", value=f"{payload.get('scalability_score', 50)}%")

        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("<div class='terminal-card'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#00f2ff;margin-top:0;'>[ COMPUTATIONAL SCORING GEOMETRY PROFILE ]</h4>", unsafe_allow_html=True)
            fig = go.Figure(data=go.Scatterpolar(
                r=[algo_score, payload.get('market_demand_score', 50), payload.get('scalability_score', 50)],
                theta=['Local Algorithmic Matrix', 'Market Capacity Index', 'Scalability Performance'],
                fill='toself', line_color='#00f2ff', fillcolor='rgba(0,242,255,0.1)'
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#30363d"), angularaxis=dict(gridcolor="#30363d")),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=30,r=30,t=30,b=30))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='terminal-card' style='height:294px;'><b>[ ELEVATOR PITCH DATA RECOVERY ]</b><br><br><p style='font-style: italic; color:#e1e4e8; line-height:1.6;'>\"{payload.get('elevator_pitch')}\"</p></div>", unsafe_allow_html=True)

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown(f"<div class='terminal-card'><b>[ TARGET OPERATIONS FIELD ]</b><br><br>{payload.get('market_demand_analysis')}</div>", unsafe_allow_html=True)
        with col_d2:
            st.markdown(f"<div class='terminal-card'><b>[ COMPETITIVE VECTOR SHIELD ]</b><br><br>{payload.get('competitor_analysis')}</div>", unsafe_allow_html=True)

        st.markdown("<h3 class='neon-text'>[ ARCHITECTURAL SWOT STRATEGIC EVALUATION GRID ]</h3>", unsafe_allow_html=True)
        s1, s2, s3, s4 = st.columns(4)
        s1.markdown("<div class='terminal-card' style='border-left-color:#56d364; height: 180px;'><b>STRENGTH CORE</b><br><br>" + "<br>".join([f"• {x}" for x in payload.get('strengths', [])]) + "</div>", unsafe_allow_html=True)
        s2.markdown("<div class='risk-card' style='height: 180px;'><b>WEAKNESS CHANNELS</b><br><br>" + "<br>".join([f"• {x}" for x in payload.get('weaknesses', [])]) + "</div>", unsafe_allow_html=True)
        s3.markdown("<div class='terminal-card' style='border-left-color:#e3b341; height: 180px;'><b>OPPORTUNITY MARGINS</b><br><br>" + "<br>".join([f"• {x}" for x in payload.get('opportunities', [])]) + "</div>", unsafe_allow_html=True)
        s4.markdown("<div class='risk-card' style='height: 180px;'><b>THREAT COMPILATION</b><br><br>" + "<br>".join([f"• {x}" for x in payload.get('threats', [])]) + "</div>", unsafe_allow_html=True)

        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown("<div class='terminal-card'>", unsafe_allow_html=True)
            st.markdown("<b style='color:#ff3e3e;'>[ CRITICAL DEPENDENCY & RISK PROFILE ]</b><br><br>", unsafe_allow_html=True)
            st.write(f"<b>System Technical Risk Factor:</b> {payload.get('technical_risks')}", unsafe_allow_html=True)
            st.write(f"<b>Market Friction Risk Factor:</b> {payload.get('market_risks')}", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col_r2:
            st.markdown("<div class='terminal-card' style='height: 138px;'>", unsafe_allow_html=True)
            st.markdown("<b>[ SUGGESTED STRATEGIC INCOME CHANNELS ]</b><br><br>", unsafe_allow_html=True)
            st.write(", ".join([f"⚙️ {x}" for x in payload.get('monetization', [])]))
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        export_payload_text = f"""IDEALENS AI - INTELLIGENCE DIAGNOSTIC MANIFEST
====================================================
VENTURE CORE LOG INDEX: {name}
INDUSTRY NODE DOMAIN: {ind}
GEOGRAPHIC BOUNDARY: {reg}

[LOCAL PROCESSOR EVALUATION STATISTICS]
- Token Keyword Density Factor: {dens}%
- Code-Driven Viability Aggregation Vector: {algo_score}%

[COMPUTED VENTURE ELEVATOR PITCH]
{payload.get('elevator_pitch')}

[TARGET CONTEXT APPRAISAL]
{payload.get('market_demand_analysis')}
"""
        st.download_button(
            label="▼ DOWNLOAD INTEL SYSTEM MANIFEST DATA (TXT)",
            data=export_payload_text,
            file_name=f"idealens_telemetry_report_{name.lower()}.txt",
            mime="text/plain"
        )

# ==============================================================================
# PIPELINE CHANNEL 2: PERSISTENT INTERNAL STORAGE REGISTRY
# ==============================================================================
else:
    st.markdown("<h1 class='neon-text'>[ DATABASE REGISTRY INTERROGATION PANELS ]</h1>", unsafe_allow_html=True)
    st.write("Verifiable physical ledger queries tracking system transactional milestones.")
    
    logs = fetch_history()
    if not logs:
        st.info("System storage registry tracks zero metrics. Run processing loops to populate structural schemas.")
    else:
        st.markdown("### Verifiable SQLite Relational Table Matrix Rows")
        for log_id, timestamp, v_name, ind, a_score in logs:
            with st.expander(f"ROW ENGINE KEY: {log_id} | TIMESTAMP: {timestamp} -> CODENAME: {v_name} ({ind}) | ALGO SCORE VECTOR: {a_score}%"):
                row_dataset = fetch_record_by_id(log_id)
                if row_dataset:
                    r_name, r_ind, r_reg, r_desc, r_dens, r_ascore, r_payload = row_dataset
                    parsed_object = json.loads(r_payload)
                    
                    st.write(f"**Conceptual Model Prompt Summary:** {r_desc}")
                    st.write(f"**Physical Matrix Metrics Calculated:** Keyword Density Node: {r_dens}% | Balanced Math Formula Index Score: {r_ascore}%")
                    st.write(f"**Saved AI Business Intelligence Analysis:** {parsed_object.get('market_demand_analysis')}")
