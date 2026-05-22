import streamlit as st
import google.genai as genai
import plotly.graph_objects as go
import json
import sqlite3
import re
from datetime import datetime

# ==============================================================================
# 1. DATABASE MANAGEMENT LAYER (SQLite3 Relational Storage)
# ==============================================================================
def init_db():
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
    conn = sqlite3.connect("idealens_bi.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, venture_name, industry, algo_viability_score FROM venture_logs ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    return records

def fetch_record_by_id(record_id):
    conn = sqlite3.connect("idealens_bi.db")
    cursor = conn.cursor()
    cursor.execute("SELECT venture_name, industry, region, description, keyword_density, algo_viability_score, llm_payload FROM venture_logs WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    return row

init_db()

# ==============================================================================
# 2. COMPUTATION NODES: LOCAL METRIC SCORING & TEXT NLP PROCESSING
# ==============================================================================
def local_nlp_processor(text_input):
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
    budget_score = {"Low (Bootstrap)": 65, "Medium (Angel/Seed)": 85, "High (VC Ready)": 95}.get(budget_tier, 50)
    team_score = {"1-2 Solo/Duet": 60, "3-5 Core Team": 85, "5+ Expanded Node": 95}.get(team_capacity, 50)
    base_score = (budget_score * 0.4) + (team_score * 0.4) + (min(keyword_density * 5, 100) * 0.2)
    return round(base_score, 1)

# ==============================================================================
# 3. INTERFACE WORKSPACE: ULTRA HIGH-CONTRAST PROFESSIONAL EXECUTIVE THEME
# ==============================================================================
st.set_page_config(page_title="IdeaLens AI - Business Intelligence Dashboard", layout="wide")

# High contrast design fixing visibility bugs entirely
st.markdown("""
    <style>
        /* Main background and global crisp text color */
        .stApp {
            background-color: #0b0f19;
            color: #ffffff !important;
        }
        
        /* Fix visibility for all input field titles and sidebar texts */
        label, p, span, .stMarkdown, [data-testid="stMarkdownContainer"] p {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        /* Sidebar layout visibility settings */
        section[data-testid="stSidebar"] {
            background-color: #111827 !important;
            border-right: 2px solid #2563eb !important;
        }
        section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] label {
            color: #ffffff !important;
        }
        
        /* Custom input fields contrast styles */
        div[data-baseweb="textarea"], div[data-baseweb="input"], div[data-baseweb="select"] {
            background-color: #1f2937 !important;
            border: 2px solid #4b5563 !important;
            border-radius: 8px !important;
        }
        textarea, input, select {
            color: #ffffff !important;
            background-color: #1f2937 !important;
        }
        
        /* High visibility main trigger button styling */
        .stButton>button {
            background-color: #2563eb !important;
            color: #ffffff !important;
            border: 2px solid #3b82f6 !important;
            border-radius: 8px !important;
            padding: 14px 28px !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            width: 100%;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
        }
        .stButton>button:hover {
            background-color: #1d4ed8 !important;
            border-color: #2563eb !important;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6) !important;
        }
        
        /* Custom styles for native containers to ensure neat grid structure */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #111827 !important;
            border: 1px solid #374151 !important;
            padding: 15px !important;
            border-radius: 8px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Secure API Key Check - Checks Secrets first, then fallback to manual entry
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not API_KEY:
    API_KEY = st.sidebar.text_input("Enter Gemini API Key (Fallback):", type="password")
client = genai.Client(api_key=API_KEY) if API_KEY else None

with st.sidebar:
    st.markdown("<h1 style='color: white; margin-bottom: 0;'>📊 IdeaLens AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9ca3af; margin-top: 0;'>Business Analytics Engine</p>", unsafe_allow_html=True)
    st.markdown("---")
    workspace = st.radio("Navigation Menu", ["🚀 Idea Analysis Board", "📂 Historical Report Logs"])
    st.markdown("---")
    if client:
        st.success("API Connected Successfully")
    else:
        st.warning("Awaiting API Connection Key")

# ==============================================================================
# WORKSPACE PANEL 1: MAIN IDEA INPUT AND REPORT GENERATION
# ==============================================================================
if workspace == "🚀 Idea Analysis Board":
    st.title("💡 Startup Idea Valuation Panel")
    st.write("Input your business concept telemetry data to run our local analytics algorithms and cloud models.")
    
    with st.form("startup_form"):
        col1, col2 = st.columns(2)
        with col1:
            startup_name = st.text_input("Startup / Venture Name", value="OmniRoute-Mesh")
            industry = st.selectbox("Industry Segment", ["SaaS", "FinTech", "EdTech", "IoT/Hardware", "CleanTech"])
            budget = st.selectbox("Funding Allotment Tier", ["Low (Bootstrap)", "Medium (Angel/Seed)", "High (VC Ready)"])
        with col2:
            target_audience = st.text_input("Target Customer Group", value="Urban Freelancers & Students")
            region = st.text_input("Target Geographical Region", value="India")
            team = st.selectbox("Current Team Size", ["1-2 Solo/Duet", "3-5 Core Team", "5+ Expanded Node"])
            
        idea_description = st.text_area("Venture Description (Explain your concept clearly)", height=150)
        submit_btn = st.form_submit_button("Generate Full Validation Report")

    if submit_btn:
        if not client:
            st.error("Authentication Error: Missing active Gemini API Key. Please add it to your Streamlit App secrets.")
        elif len(idea_description.strip()) < 15:
            st.error("Validation Error: Please write a longer concept description for deep analysis.")
        else:
            with st.spinner("Processing local calculations and compiling cloud business data..."):
                try:
                    local_density = local_nlp_processor(idea_description)
                    calculated_viability = algorithmic_viability_matrix(budget, team, local_density)
                    
                    master_prompt = f"""
                    You are an expert enterprise valuation business intelligence platform.
                    Analyze these details:
                    Name: {startup_name} | Industry: {industry} | Region: {region} | Target: {target_audience}
                    Concept Context: {idea_description}
                    Local Algorithmic Score Calculated: {calculated_viability}%

                    Respond with a raw valid JSON object matching this structural constraint precisely. Do not include markdown ticks.
                    {{
                        "market_demand_score": 75,
                        "scalability_score": 80,
                        "market_demand_analysis": "Write a deep detailed overview of market demand.",
                        "competitor_analysis": "Write a deep detailed breakdown of market competitors.",
                        "strengths": ["s1", "s2", "s3", "s4"],
                        "weaknesses": ["w1", "w2", "w3", "w4"],
                        "opportunities": ["o1", "o2", "o3", "o4"],
                        "threats": ["t1", "t2", "t3", "t4"],
                        "monetization": ["m1", "m2", "m3"],
                        "technical_risks": "Deep details regarding software infrastructure system failure risks.",
                        "market_risks": "Deep details regarding competitive pressure and friction.",
                        "elevator_pitch": "A professional 30-second presentation line."
                    }}
                    """
                    
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=master_prompt)
                    raw_json = response.text.strip().replace("```json", "").replace("```", "")
                    llm_data = json.loads(raw_json)
                    
                    save_analysis(startup_name, industry, region, idea_description, local_density, calculated_viability, llm_data)
                    st.session_state['active_analysis'] = (startup_name, industry, region, idea_description, local_density, calculated_viability, llm_data)
                    st.success("Report Generation Successful.")
                    
                except Exception as e:
                    st.error(f"Inference Failure: {str(e)}")

    # High-Performance Dashboard Rendering
    if 'active_analysis' in st.session_state:
        name, ind, reg, desc, dens, algo_score, payload = st.session_state['active_analysis']
        st.markdown("---")
        st.header(f"📈 Strategic Feasibility Report: {name}")
        
        # Performance Analytics Cards
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(label="Local NLP Keyword Density", value=f"{dens}%")
        with col_m2:
            st.metric(label="Local Algorithmic Score", value=f"{algo_score}%")
        with col_m3:
            st.metric(label="Cloud Market Scalability Index", value=f"{payload.get('scalability_score', 50)}%")

        col_g1, col_g2 = st.columns([1, 1])
        with col_g1:
            with st.container(border=True):
                st.subheader("Performance Target Profile")
                fig = go.Figure(data=go.Scatterpolar(
                    r=[algo_score, payload.get('market_demand_score', 50), payload.get('scalability_score', 50)],
                    theta=['Local Code Logic', 'Market Demand Index', 'Scalability Factor'],
                    fill='toself', line_color='#3b82f6', fillcolor='rgba(59, 130, 246, 0.2)'
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#4b5563"), angularaxis=dict(gridcolor="#4b5563")),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=30,r=30,t=30,b=30)
                )
                st.plotly_chart(fig, use_container_width=True)
        with col_g2:
            with st.container(border=True):
                st.subheader("Professional Elevator Pitch")
                st.info(f"\"{payload.get('elevator_pitch')}\"")

        st.markdown("---")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            with st.container(border=True):
                st.subheader("Market Demand Analysis")
                st.write(payload.get('market_demand_analysis'))
        with col_t2:
            with st.container(border=True):
                st.subheader("Competitor Shield Breakdown")
                st.write(payload.get('competitor_analysis'))

        st.markdown("---")
        st.subheader("Strategic SWOT Evaluation Matrix")
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.success("**STRENGTHS**\n\n" + "\n\n".join([f"• {x}" for x in payload.get('strengths', [])]))
        with s2:
            st.error("**WEAKNESSES**\n\n" + "\n\n".join([f"• {x}" for x in payload.get('weaknesses', [])]))
        with s3:
            st.warning("**OPPORTUNITIES**\n\n" + "\n\n".join([f"• {x}" for x in payload.get('opportunities', [])]))
        with s4:
            st.info("**THREATS**\n\n" + "\n\n".join([f"• {x}" for x in payload.get('threats', [])]))

        st.markdown("---")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            with st.container(border=True):
                st.subheader("Risk Metrics Profile")
                st.write(f"**Technical System Risks:** {payload.get('technical_risks')}")
                st.write(f"**Market Entry Risks:** {payload.get('market_risks')}")
        with col_r2:
            with st.container(border=True):
                st.subheader("Suggested Revenue Generation Models")
                st.write(", ".join([f"⚙️ {x}" for x in payload.get('monetization', [])]))

        # Enhanced High-Content Report Generation Engine (Solves the basic bullet point issue)
        st.markdown("---")
        full_executive_report = f"""======================================================================
                  IDEALENS AI - EXECUTIVE ASSESSMENT REPORT
======================================================================
GENERATION TIMESTAMP: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
VENTURE CODE IDENTITY: {name}
TARGET INDUSTRY SEGMENT: {ind}
GEOGRAPHICAL JURISDICTION NODE: {reg}
======================================================================

1. LOCAL SYSTEM COMPUTATION STATISTICS
----------------------------------------------------------------------
* Local Token NLP Keyword Density: {dens}%
* Code-Driven Local Algorithmic Score: {algo_score}%
* AI Core Cloud Market Scalability Index: {payload.get('scalability_score', 50)}%

2. CORE CONCEPT STATEMENT & ELEVATOR PITCH
----------------------------------------------------------------------
"{payload.get('elevator_pitch')}"

3. COMPREHENSIVE MARKET AND COMPETITIVE OVERVIEW
----------------------------------------------------------------------
* MARKET DEMAND REPORT:
{payload.get('market_demand_analysis')}

* COMPETITIVE LANDSCAPE ANALYSIS:
{payload.get('competitor_analysis')}

4. STRATEGIC SWOT MATRIX SPECIFICATION
----------------------------------------------------------------------
STRENGTHS:
{chr(10).join(['  - ' + x for x in payload.get('strengths', [])])}

WEAKNESSES:
{chr(10).join(['  - ' + x for x in payload.get('weaknesses', [])])}

OPPORTUNITIES:
{chr(10).join(['  - ' + x for x in payload.get('opportunities', [])])}

THREATS:
{chr(10).join(['  - ' + x for x in payload.get('threats', [])])}

5. RISK APPRAISAL AND MONETIZATION FRAMEWORK
----------------------------------------------------------------------
* TECHNICAL INFRASTRUCTURE RISKS: 
  {payload.get('technical_risks')}

* MARKET FRICTION FACTORS: 
  {payload.get('market_risks')}

* RECOMMENDED ECONOMIC MODEL CHANNELS:
  {', '.join([x for x in payload.get('monetization', [])])}

======================================================================
              END OF DATA TRANSACTION LOG DELIVERY
======================================================================
"""
        st.download_button(
            label="📥 Download Complete Executive Report (Full Document)",
            data=full_executive_report,
            file_name=f"idealens_executive_report_{name.lower()}.txt",
            mime="text/plain"
        )

# ==============================================================================
# WORKSPACE PANEL 2: SAVED LOGS FROM DATABASE PERSISTENCE LAYER
# ==============================================================================
else:
    st.title("📂 System Database Registry Logs")
    st.write("Browse historical venture evaluations stored permanently inside the relational SQLite system.")
    
    logs = fetch_history()
    if not logs:
        st.info("The local database ledger contains zero saved analytics metrics rows.")
    else:
        for log_id, timestamp, v_name, ind, a_score in logs:
            with st.expander(f"Record ID: {log_id} | {timestamp} -> VENTURE: {v_name} | LOCAL ALGO SCORE: {a_score}%"):
                row_dataset = fetch_record_by_id(log_id)
                if row_dataset:
                    r_name, r_ind, r_reg, r_desc, r_dens, r_ascore, r_payload = row_dataset
                    parsed_object = json.loads(r_payload)
                    
                    st.write(f"**Venture Concept Narrative text:** {r_desc}")
                    st.write(f"**Relational Local Telemetry:** Keyword Density: {r_dens}% | Balanced Scoring Index: {r_ascore}%")
                    st.write(f"**Saved Cloud Business Intelligence Data:** {parsed_object.get('market_demand_analysis')}")
