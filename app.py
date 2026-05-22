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
# 3. INTERFACE WORKSPACE: PREMIUM SLATE CORPORATE ANALYTICS THEME
# ==============================================================================
st.set_page_config(page_title="IdeaLens AI - Business Intelligence Dashboard", layout="wide")

# Global UI Style Layout Enhancements
st.markdown("""
    <style>
        .stApp {
            background-color: #0f172a;
            color: #f8fafc;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        section[data-testid="stSidebar"] {
            background-color: #1e293b !important;
            border-right: 1px solid #334155 !important;
        }
        div[data-baseweb="textarea"], div[data-baseweb="input"], div[data-baseweb="select"] {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
        }
        textarea, input {
            color: #f8fafc !important;
        }
        .stButton>button {
            background-color: #2563eb !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            width: 100%;
            transition: background-color 0.2s;
        }
        .stButton>button:hover {
            background-color: #1d4ed8 !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

# Secure Environment Configuration for Global API Client Engine
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not API_KEY:
    API_KEY = st.sidebar.text_input("Enter Gemini API Key:", type="password")
client = genai.Client(api_key=API_KEY) if API_KEY else None

with st.sidebar:
    st.title("📊 IdeaLens AI")
    st.caption("Business Validation & Analytics Platform")
    st.markdown("---")
    workspace = st.radio("Navigation Panel", ["🚀 Idea Analysis Board", "📂 Historical Report Logs"])
    st.markdown("---")
    st.success("System Status: Active")

# ==============================================================================
# WORKSPACE PANEL 1: MAIN IDEA INPUT AND REPORT GENERATION
# ==============================================================================
if workspace == "🚀 Idea Analysis Board":
    st.title("💡 Startup Idea Diagnostics")
    st.write("Fill out the business profile form below to generate a deep cloud-computed market feasibility report.")
    
    with st.form("startup_form"):
        col1, col2 = st.columns(2)
        with col1:
            startup_name = st.text_input("Startup / Venture Name", value="OmniRoute-Mesh")
            industry = st.selectbox("Industry Node Segment", ["SaaS", "FinTech", "EdTech", "IoT/Hardware", "CleanTech"])
            budget = st.selectbox("Financial Resource Allocation", ["Low (Bootstrap)", "Medium (Angel/Seed)", "High (VC Ready)"])
        with col2:
            target_audience = st.text_input("Target Consumer Profile", value="Urban Freelancers & Students")
            region = st.text_input("Geographic Jurisdiction Node", value="India")
            team = st.selectbox("Human Capital Resource Capacity", ["1-2 Solo/Duet", "3-5 Core Team", "5+ Expanded Node"])
            
        idea_description = st.text_area("Venture Description (Explain your idea here)", height=150)
        submit_btn = st.form_submit_button("Generate Full Validation Report")

    if submit_btn:
        if not client:
            st.error("Authentication Error: Active Gemini API Validation Key missing in environment settings.")
        elif len(idea_description.strip()) < 15:
            st.error("Validation Error: Please write a longer description of your startup concept.")
        else:
            with st.spinner("Processing local calculations and compiling cloud business data..."):
                try:
                    # Execute mathematical algorithms locally 
                    local_density = local_nlp_processor(idea_description)
                    calculated_viability = algorithmic_viability_matrix(budget, team, local_density)
                    
                    # Package structured validation instructions
                    master_prompt = f"""
                    You are an expert enterprise business intelligence platform analyzing a new startup concept.
                    Analyze these details:
                    Name: {startup_name} | Industry: {industry} | Region: {region} | Target: {target_audience}
                    Concept Context: {idea_description}
                    Local Algorithmic Score Calculated: {calculated_viability}%

                    Respond with a raw valid JSON object matching this structural constraint precisely. Do not include markdown ticks.
                    {{
                        "market_demand_score": 75,
                        "scalability_score": 80,
                        "market_demand_analysis": "Comprehensive market data and demand overview text here.",
                        "competitor_analysis": "Deep evaluation of competitors text here.",
                        "strengths": ["Strategic Strength 1", "Strategic Strength 2"],
                        "weaknesses": ["Risk Factor 1", "Risk Factor 2"],
                        "opportunities": ["Growth Vector 1", "Growth Vector 2"],
                        "threats": ["Market Threat 1", "Market Threat 2"],
                        "monetization": ["Revenue Model 1", "Revenue Model 2"],
                        "technical_risks": "Infrastructure operational system failure risks text.",
                        "market_risks": "Competitive market entry pressure metrics text.",
                        "elevator_pitch": "Structural 30-second investor presentation pitch line."
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
                    st.success("Report Generation Successful. Data synchronized.")
                    
                except Exception as e:
                    st.error(f"Inference Failure: {str(e)}")

    # Clean Output Dashboard Display
    if 'active_analysis' in st.session_state:
        name, ind, reg, desc, dens, algo_score, payload = st.session_state['active_analysis']
        st.markdown("---")
        st.header(f"📈 Business Intelligence Report: {name}")
        
        # High Impact Analytics Cards
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(label="Local NLP Keyword Density", value=f"{dens}%")
        with col_m2:
            st.metric(label="Local Algorithmic Base Score", value=f"{algo_score}%")
        with col_m3:
            st.metric(label="AI Market Scalability Index", value=f"{payload.get('scalability_score', 50)}%")

        # Interactive Charts Section
        col_g1, col_g2 = st.columns([1, 1])
        with col_g1:
            with st.container(border=True):
                st.subheader("Statistical Performance Chart")
                fig = go.Figure(data=go.Scatterpolar(
                    r=[algo_score, payload.get('market_demand_score', 50), payload.get('scalability_score', 50)],
                    theta=['Local Code Algorithm', 'Market Demand Score', 'Scalability Vector'],
                    fill='toself', line_color='#3b82f6', fillcolor='rgba(59, 130, 246, 0.2)'
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#334155"), angularaxis=dict(gridcolor="#334155")),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=260, margin=dict(l=30,r=30,t=30,b=30)
                )
                st.plotly_chart(fig, use_container_width=True)
        with col_g2:
            with st.container(border=True):
                st.subheader("Professional Elevator Pitch")
                st.write("")
                st.info(f"\"{payload.get('elevator_pitch')}\"")
                st.write("")

        # Deep Market Analysis Text Blocks (Using clean native containers to completely avoid overlaps)
        st.markdown("---")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            with st.container(border=True):
                st.subheader("Market Demand Analysis")
                st.write(payload.get('market_demand_analysis'))
        with col_t2:
            with st.container(border=True):
                st.subheader("Competitor Analysis")
                st.write(payload.get('competitor_analysis'))

        # Strategic SWOT Matrix Component Blocks
        st.markdown("---")
        st.subheader("Strategic SWOT Assessment")
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.success("**STRENGTHS (Core Advantages)**\n\n" + "\n\n".join([f"• {x}" for x in payload.get('strengths', [])]))
        with s2:
            st.error("**WEAKNESSES (Internal Vulnerabilities)**\n\n" + "\n\n".join([f"• {x}" for x in payload.get('weaknesses', [])]))
        with s3:
            st.warning("**OPPORTUNITIES (Growth Fields)**\n\n" + "\n\n".join([f"• {x}" for x in payload.get('opportunities', [])]))
        with s4:
            st.info("**THREATS (Market Risks)**\n\n" + "\n\n".join([f"• {x}" for x in payload.get('threats', [])]))

        # Final Operational Context
        st.markdown("---")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            with st.container(border=True):
                st.subheader("Risk Evaluation Matrix")
                st.write(f"**Technical Risk Analysis:** {payload.get('technical_risks')}")
                st.write(f"**Market Friction Analysis:** {payload.get('market_risks')}")
        with col_r2:
            with st.container(border=True):
                st.subheader("Suggested Revenue Streams")
                st.write(", ".join([f"⚙️ {x}" for x in payload.get('monetization', [])]))

        # Download Deliverable Button Node
        st.markdown("---")
        export_text = f"IDEALENS AI SYSTEM ANALYSIS REPORT\n====================================\nVENTURE: {name}\nINDUSTRY: {ind}\nREGION: {reg}\nLOCAL ALGO VIABILITY SCORE: {algo_score}%"
        st.download_button(
            label="Download Complete Business Report (TXT)",
            data=export_text,
            file_name=f"idealens_analytics_report_{name.lower()}.txt",
            mime="text/plain"
        )

# ==============================================================================
# WORKSPACE PANEL 2: SAVED LOGS FROM DATABASE PERSISTENCE LAYER
# ==============================================================================
else:
    st.title("📂 Database Records Ledger")
    st.write("Browse historical venture evaluations stored permanently inside the local relational SQLite database system.")
    
    logs = fetch_history()
    if not logs:
        st.info("The persistent SQL database is currently empty. Run an evaluation to store metrics data.")
    else:
        st.markdown("### Verifiable Database Log Registry Entries")
        for log_id, timestamp, v_name, ind, a_score in logs:
            with st.expander(f"Record #{log_id} | {timestamp} -> VENTURE: {v_name} ({ind}) | LOCAL ALGO SCORE: {a_score}%"):
                row_dataset = fetch_record_by_id(log_id)
                if row_dataset:
                    r_name, r_ind, r_reg, r_desc, r_dens, r_ascore, r_payload = row_dataset
                    parsed_object = json.loads(r_payload)
                    
                    st.write(f"**Venture Concept Summary:** {r_desc}")
                    st.write(f"**Computed Local Data:** Keyword Density Node: {r_dens}% | Formula Baseline Score: {r_ascore}%")
                    st.write(f"**Preserved Cloud Demand Analysis:** {parsed_object.get('market_demand_analysis')}")
