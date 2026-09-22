"""
KGOSI MINING SOLUTIONS - MAINTENANCE MANAGEMENT SYSTEM
The software that solves the problem.
Fleet Manager uses this daily to: check machines, log jobs, track repairs, manage alerts.
Run: streamlit run 04_software.py --server.port 8502
"""

import streamlit as st

# Respect report links even when Streamlit Cloud starts this file directly.
if st.query_params.get("view") == "dashboard":
    import runpy
    from pathlib import Path
    runpy.run_path(str(Path(__file__).resolve().parent / "03_dashboard.py"), run_name="__main__")
    st.stop()
with st.columns([5, 1])[1]:
    st.link_button("Dashboard", "?view=dashboard", use_container_width=True)
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib, json
import base64
from pathlib import Path
from datetime import datetime, date, timedelta

BASE_DIR = Path(__file__).resolve().parent


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Momo+Trust+Display&family=Red+Hat+Display:wght@500;600;700;800&family=Stack+Sans+Text:wght@400;500;600;700&display=swap');
:root{--coal:#0c0b0a;--graphite:#191715;--iron:#312c27;--copper:#b44e2b;--gold:#d69b32;--sand:#eee8de;--paper:#f8f5ef;--ink:#171411;--muted:#6b6259;--line:#d9d0c4;}
html,body,[class*="css"],input,button,textarea,select{font-family:'IBM Plex Sans',sans-serif!important;color:var(--ink)}.stApp{background:var(--paper)}.block-container{max-width:1180px;padding:1.2rem 2.5rem 3rem}h1,h2,h3,h4{font-family:'Barlow Condensed',sans-serif!important;font-weight:600;letter-spacing:.005em}p,label{color:var(--ink)}
.brandbar{display:flex;align-items:center;justify-content:space-between;background:var(--coal);padding:1.05rem 1.4rem;border-bottom:1px solid #3b3027}.brand{display:flex;gap:.85rem;align-items:center}.brandmark{position:relative;width:44px;height:34px;border-left:3px solid var(--copper);transform:skewX(-12deg)}.brandmark i{position:absolute;left:5px;height:3px;background:var(--gold)}.brandmark i:nth-child(1){top:5px;width:31px}.brandmark i:nth-child(2){top:15px;width:24px}.brandmark i:nth-child(3){top:25px;width:16px}.brand strong{display:block;font-family:'Barlow Condensed',sans-serif;font-size:1.42rem;line-height:.9;letter-spacing:.12em;color:#fff}.brand small{display:block;font-family:'IBM Plex Sans',sans-serif;font-size:.55rem;letter-spacing:.18em;text-transform:uppercase;color:#b7aa9d;margin-top:.35rem}.brandmeta{font-family:'IBM Plex Sans',sans-serif;font-size:.57rem;letter-spacing:.18em;text-transform:uppercase;color:#b7aa9d;font-weight:600}.brandmeta span{color:var(--gold);margin-left:.8rem}
.mine-hero{height:430px;background-size:cover;background-position:center;border-radius:0 0 2px 2px;display:flex;align-items:center;padding:3.5rem;margin-bottom:1.5rem;box-shadow:0 24px 60px rgba(20,12,8,.18)}.hero-copy{max-width:650px}.hero-copy .eyebrow{font-family:'IBM Plex Sans',sans-serif;font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:#e3b45e;font-weight:600}.hero-copy h1{font-size:4.55rem;line-height:.88;letter-spacing:.01em;color:#fff;margin:.8rem 0 1.2rem;text-transform:uppercase}.hero-copy p{max-width:450px;color:#e4ddd5;font-size:.82rem;line-height:1.75}.hero-cta{display:inline-block;border-left:3px solid var(--copper);color:#fff!important;padding:.55rem .85rem;font-size:.58rem;letter-spacing:.18em;text-transform:uppercase;font-weight:600;margin-top:.6rem;text-decoration:none!important;cursor:pointer;transition:background .18s ease,transform .18s ease}.hero-cta:hover{background:rgba(187,75,39,.22);transform:translateX(3px)}.hero-cta:focus{outline:3px solid rgba(214,128,60,.38);outline-offset:3px}html{scroll-behavior:smooth}.workspace-anchor{scroll-margin-top:88px}
.about-panel{display:grid;grid-template-columns:.88fr 1.12fr;gap:2.5rem;align-items:center;background:#fff;padding:2.3rem 2.5rem;margin:0 0 1.5rem}.about-copy .eyebrow{font-size:.58rem;letter-spacing:.18em;color:#9f3e20!important;font-weight:600;text-transform:uppercase}.about-copy h2{font-size:2.65rem;line-height:.95;margin:.7rem 0 .9rem;text-transform:uppercase;color:#171411!important}.about-copy p{font-size:.76rem;color:#51483f!important;line-height:1.75}.about-photo{height:220px;background-size:cover;background-position:center;border-radius:2px}.contact-strip{grid-column:1/-1;background:linear-gradient(90deg,var(--coal),#32140d);color:#fff;padding:.9rem 1.2rem;text-align:center;font-weight:600;font-size:.76rem;letter-spacing:.04em}.contact-strip span{color:#e36a43;margin-left:.7rem}
.nav-label{text-align:center;font-size:.62rem;letter-spacing:.15em;text-transform:uppercase;font-weight:700;color:#796c61;margin:.7rem 0 .45rem}div[data-testid="stRadio"]>div{justify-content:center;gap:.25rem;background:var(--coal);padding:.35rem;margin-bottom:1.4rem}div[data-testid="stRadio"] label{padding:.62rem 1rem;margin:0!important}div[data-testid="stRadio"] label:has(input:checked){background:var(--copper)}div[data-testid="stRadio"] label p{color:#e8e1d9!important;font-size:.74rem;font-weight:600;white-space:nowrap}div[data-testid="stRadio"] label:has(input:checked) p{color:#fff!important}div[data-testid="stRadio"] div[role="radiogroup"]>label>div:first-child{display:none}
.topbar{background:var(--coal);padding:1.7rem 2rem;border-radius:2px;margin-bottom:1.2rem;border-left:5px solid var(--copper)}.topbar h1{margin:0;font-size:2.35rem;color:#fff;text-transform:uppercase}.topbar p{margin:.35rem 0 0;color:#bbb0a5;font-size:.76rem}.kcard{background:#fff;padding:1.15rem 1.3rem;border:1px solid var(--line);margin-bottom:.3rem;min-height:125px}.kcard.red{border-top:4px solid #9f3323}.kcard.orange{border-top:4px solid var(--copper)}.kcard.green{border-top:4px solid #557047}.kcard.blue{border-top:4px solid #6f6256}.kval{font-family:'Barlow Condensed',sans-serif;font-size:2.15rem;font-weight:600;line-height:1;color:var(--coal)}.klbl{font-size:.61rem;text-transform:uppercase;letter-spacing:1.6px;color:#493e35;margin-top:.45rem;font-weight:600}.ksub{font-size:.7rem;color:var(--muted);margin-top:.3rem}
.alert-critical,.alert-high,.alert-medium,.alert-ok{border-radius:2px;padding:1.2rem;margin:.5rem 0;color:#fff}.alert-critical{background:#5b1d16;border-left:5px solid #e26b50}.alert-high{background:#672815;border-left:5px solid #db7a41}.alert-medium{background:#614510;border-left:5px solid #d9a73d}.alert-ok{background:#283424;border-left:5px solid #6c9860}.result-box{border-radius:2px;padding:1.8rem;margin:1rem 0;text-align:center}.job-card{background:#fff;padding:1rem 1.2rem;border:1px solid var(--line);border-left:5px solid #77695c;margin:.5rem 0}.job-card.urgent{border-left-color:#a93b2b}.job-card.done{border-left-color:#557047;opacity:.75}
section[data-testid="stSidebar"]{display:none!important}.stTextInput input,.stNumberInput input,.stTextArea textarea{background:#fff!important;color:var(--ink)!important;border:1px solid #cfc4b7!important;border-radius:2px!important}.stSelectbox div[data-baseweb="select"]>div{background:#fff!important;color:var(--ink)!important;border-color:#cfc4b7!important;border-radius:2px!important}.stButton>button{background:var(--copper);color:#fff;border:0;border-radius:2px;padding:.68rem 1.5rem;font-weight:700;width:100%}.stButton>button *{color:#fff!important}.stButton>button:hover{background:var(--coal);color:#fff}div[data-testid="stDataFrame"]{border:1px solid var(--line)}hr{border-color:var(--line)!important}#MainMenu,footer,header{visibility:hidden}
@media(max-width:850px){.block-container{padding:1rem}.mine-hero{padding:2rem 1.3rem;height:350px}.hero-copy h1{font-size:2.25rem}.about-panel{grid-template-columns:1fr;gap:1rem}.brandmeta{display:none}div[data-testid="stRadio"]>div{justify-content:flex-start;overflow-x:auto}}
#MainMenu,footer,header{visibility:hidden;}
/* Portfolio typography: expressive brand, editorial headings, highly legible UI. */
html,body,[class*="css"],p,label,input,button,select,textarea{font-family:'Stack Sans Text','Segoe UI',sans-serif!important}
h1,h2,h3,h4,.topbar h1{font-family:'Red Hat Display','Segoe UI',sans-serif!important;letter-spacing:-.035em}
.brand strong{font-family:'Momo Trust Display','Red Hat Display',sans-serif!important;letter-spacing:.08em}
.hero-copy h1{font-family:'Red Hat Display','Segoe UI',sans-serif!important;font-weight:700;letter-spacing:-.045em}
.kval{font-family:'Red Hat Display','Segoe UI',sans-serif!important;font-variant-numeric:tabular-nums}
button,div[data-testid="stRadio"] label p,.eyebrow,.brandmeta,.klbl{font-family:'Stack Sans Text','Segoe UI',sans-serif!important}
.brandbar{position:relative;z-index:2}.mine-hero{height:390px;padding:2.7rem 3.5rem;align-items:center;margin-bottom:.8rem}.mine-hero .hero-copy{max-width:570px}.mine-hero .hero-copy h1{font-size:3.55rem!important;line-height:.93!important;margin:.7rem 0 1rem!important;max-width:560px}.mine-hero .hero-copy p{font-size:.82rem;max-width:470px;margin-bottom:0}.about-panel{display:grid!important;grid-template-columns:.9fr 1.1fr;gap:1.2rem;padding:1rem 1.3rem;margin:.7rem 0}.about-panel .about-copy h2{font-size:1.9rem;line-height:1;margin:.45rem 0}.about-panel .about-copy p{font-size:.72rem;line-height:1.5}.about-panel .about-photo{min-height:170px}.about-panel .contact-strip{grid-column:1/-1;margin-top:.2rem;padding:.65rem 1rem}.nav-label{margin-top:.45rem}.workspace-note{display:flex;justify-content:space-between;gap:1.2rem;align-items:center;background:#f2e9df;border-left:4px solid var(--copper);padding:.8rem 1rem;margin:.2rem 0 .85rem}.workspace-note b{font-size:.78rem}.workspace-note span{font-size:.72rem;color:var(--muted)}div[data-testid="stRadio"]{position:sticky;top:0;z-index:50;background:rgba(245,240,233,.96);padding:.35rem 0;backdrop-filter:blur(10px)}input:focus,button:focus,[data-baseweb="select"]:focus-within{outline:3px solid rgba(187,75,39,.23)!important;outline-offset:2px}.stButton>button{min-height:44px}.data-hint{font-size:.72rem;color:var(--muted);margin:.2rem 0 .8rem}@media(max-width:850px){.mine-hero{height:360px!important;padding:2rem 1.3rem!important}.mine-hero .hero-copy h1{font-size:2.35rem!important;line-height:.98!important}.about-panel{grid-template-columns:1fr!important}.about-panel .about-photo{min-height:150px}}
.topbar p{max-width:720px!important;font-size:.84rem!important;line-height:1.55!important;color:#f0e7dc!important}.kcard *,.workspace-note *{opacity:1!important}.stAlert,.stAlert *{color:#231c17!important}.stTextInput label p,.stNumberInput label p,.stSelectbox label p,.stTextArea label p,.stCheckbox label p,.stMultiSelect label p,.stDateInput label p{color:#30271f!important;font-size:.82rem!important}.composition{display:grid;grid-template-columns:170px 1fr;gap:1rem;padding:1rem 1.2rem;background:#efe7dd;border-left:4px solid var(--copper);margin:.8rem 0}.composition b{font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;color:#8b331e}.composition p{margin:0;max-width:760px;color:#4f4339;line-height:1.55;font-size:.82rem}@media(max-width:700px){.composition,.workspace-note{grid-template-columns:1fr;display:grid}}
.workspace-note b{color:#542416!important;opacity:1!important;font-weight:700!important}.workspace-note span{color:#40514c!important;opacity:1!important}
.cross-app-link{position:fixed;top:1rem;right:1.7rem;z-index:9999;display:inline-flex;align-items:center;justify-content:center;padding:.62rem 1rem;background:#11131a;color:#fff!important;border:1px solid rgba(255,255,255,.18);border-radius:5px;font:650 .78rem "Stack Sans Text","Segoe UI",sans-serif;text-decoration:none!important;box-shadow:0 3px 12px rgba(0,0,0,.18)}.cross-app-link:hover{filter:brightness(1.12)}</style>
""", unsafe_allow_html=True)

# ── LOAD ──────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    m  = joblib.load(BASE_DIR / "model.pkl")
    lt = joblib.load(BASE_DIR / "le_type.pkl")
    ls = joblib.load(BASE_DIR / "le_site.pkl")
    with open(BASE_DIR / "features.json") as f: feat = json.load(f)
    return m, lt, ls, feat

@st.cache_data
def load_data():
    df   = pd.read_csv(BASE_DIR / "equipment_data.csv", parse_dates=["date"])
    risk = pd.read_csv(BASE_DIR / "risk_scores.csv")
    return df, risk

@st.cache_data(show_spinner=False)
def load_image_b64(filename):
    image_path = Path(__file__).parent / "assets" / filename
    return base64.b64encode(image_path.read_bytes()).decode("ascii")

model, le_type, le_site, FEATURES = load_model()
df, risk_df = load_data()
hero_b64 = load_image_b64("mining-hero.webp")
team_b64 = load_image_b64("maintenance-team.webp")

MACHINE_TYPES = sorted(le_type.classes_.tolist())
SITES         = sorted(le_site.classes_.tolist())
TYPE_MAX      = {"Excavator":5000,"Haul Truck":8000,"Drill Rig":4000,"Loader":6000,
                 "Crusher":7000,"Dozer":5500,"Grader":5000,"Water Truck":6000,
                 "Compressor":4500,"Conveyor Belt":9000}

# Persistent in-session storage for logged jobs and service records
if "jobs"     not in st.session_state: st.session_state.jobs     = []
if "services" not in st.session_state: st.session_state.services = []
if "alerts"   not in st.session_state: st.session_state.alerts   = []

def kcard(color, val, lbl, sub=""):
    return f'<div class="kcard {color}"><div class="kval">{val}</div><div class="klbl">{lbl}</div>{"<div class=ksub>"+sub+"</div>" if sub else ""}</div>'

def dchart(fig, h=320):
    fig.update_layout(plot_bgcolor="#f8f5ef",paper_bgcolor="#f8f5ef",
                      font_color="#171411",font_family="IBM Plex Sans",height=h,
                      margin=dict(t=15,b=15,l=5,r=5),colorway=["#b44e2b","#d69b32","#312c27","#6f6256"])
    fig.update_xaxes(gridcolor="#ded6cc",zerolinecolor="#ded6cc")
    fig.update_yaxes(gridcolor="#ded6cc",zerolinecolor="#ded6cc")
    return fig

# ── INDUSTRIAL HEADER + NAVIGATION ────────────────────────────────
pending_jobs = len([j for j in st.session_state.jobs if j["status"] == "Pending"])
critical_now = (risk_df["risk_level"] == "Critical").sum()

st.markdown(f"""
<div class="brandbar">
  <div class="brand"><div class="brandmark"><i></i><i></i><i></i></div><div><strong>KGOSI MINING</strong><small>Fleet intelligence & maintenance</small></div></div>
  <div class="brandmeta">BOTSWANA <span>OPERATIONS / 2026</span></div>
</div>
<div class="mine-hero" style="background-image:linear-gradient(90deg,rgba(7,6,5,.88) 0%,rgba(7,6,5,.58) 42%,rgba(7,6,5,.08) 72%),url('data:image/webp;base64,{hero_b64}')">
  <div class="hero-copy"><div class="eyebrow">Finding value beneath every operating hour</div><h1>Stronger Fleets.<br>Safer Production.</h1><p>Turn inspection readings, maintenance history and equipment risk into decisive action across every mining site.</p><a class="hero-cta" href="#mining-workspace">Open operations workspace &nbsp;→</a></div>
</div>
<div class="about-panel">
  <div class="about-copy"><div class="eyebrow">ABOUT FLEET INTELLIGENCE</div><h2>Maintenance decisions backed by data</h2><p>Kgosi connects equipment condition, sensor readings and work history so fleet teams can identify risk earlier, prioritise the right jobs and protect production uptime.</p></div>
  <div class="about-photo" style="background-image:url('data:image/webp;base64,{team_b64}')"></div>
  <div class="contact-strip">Critical machines: {critical_now}<span>Pending maintenance jobs: {pending_jobs}</span></div>
</div>
<div class="nav-label">Mining operations</div>
""", unsafe_allow_html=True)

st.markdown('<div id="mining-workspace" class="workspace-anchor"></div><div class="workspace-note"><b>Fleet operations workspace</b><span>Assess equipment, create work orders and record completed service here. Use the separate dashboard for fleet-wide trends.</span></div>', unsafe_allow_html=True)
nav = st.radio("Mining operations", [
    "Machine check",
    "Job board",
    "Log service",
    "Fleet health",
    "Machine records",
], horizontal=True, label_visibility="collapsed")

# ════════════════════════════════════════════════════════════════
# PAGE 1 - MACHINE CHECK (Core tool: type in readings, get risk + action)
# ════════════════════════════════════════════════════════════════
if nav == "Machine check":

    st.markdown(f'<div class="topbar"><h1>Machine Condition Check</h1><p>Use today\'s inspection readings to assess equipment risk and generate a clear maintenance response. Assessment time: {datetime.now():%d %b %Y, %H:%M}.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="composition"><b>How to use it</b><p>Select the latest machine reading or enter an inspection manually. The result explains which readings crossed safe limits before offering a maintenance action.</p></div>', unsafe_allow_html=True)

    # Optionally pre-fill from existing machine
    machine_ids = ["Type readings manually"] + sorted(df["machine_id"].unique().tolist())
    chosen = st.selectbox("Pre-fill from the latest machine reading", machine_ids)
    default = df[df["machine_id"] == chosen].sort_values("date").iloc[-1].to_dict() if chosen != "Type readings manually" else {}

    st.markdown("---")
    st.markdown("### Today’s Inspection Readings")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Machine Details**")
        machine_type = st.selectbox("Machine Type", MACHINE_TYPES,
            index=MACHINE_TYPES.index(default.get("machine_type", MACHINE_TYPES[0])) if "machine_type" in default else 0)
        machine_site = st.selectbox("Site", SITES,
            index=SITES.index(default.get("site", SITES[0])) if "site" in default else 0)
        machine_id_input = st.text_input("Machine ID (optional)", value=chosen if chosen != "Type readings manually" else "")
        age_years        = st.number_input("Age of Machine (years)", 1, 20, int(default.get("age_years", 5)))
        cumulative_hours = st.number_input("Total Hours on Engine",  100, 15000, int(default.get("cumulative_hours", 2500)))

    with col2:
        st.markdown("**Sensor Readings from Inspection**")
        temperature   = st.number_input("Engine Temperature (°C)",   50.0, 160.0, float(default.get("engine_temp_c",   78.0)), 0.5,
                                         help="Normal: below 90°C  |  Warning: 90–105°C  |  Critical: above 105°C")
        vibration     = st.number_input("Vibration Level",            0.5,  12.0, float(default.get("vibration",       2.5)),  0.1,
                                         help="Normal: below 4.0  |  Warning: 4.0–5.0  |  Critical: above 5.0")
        oil_pressure  = st.number_input("Oil Pressure (PSI)",         10.0, 100.0, float(default.get("oil_pressure_psi", 65.0)), 0.5,
                                         help="Normal: above 60 PSI  |  Warning: 45–60  |  Critical: below 45")
        oil_contam    = st.number_input("Oil Contamination (ppm)",    0.0,  15.0, float(default.get("oil_contamination_ppm", 1.5)), 0.1,
                                         help="Normal: below 3.0  |  Warning: 3.0–5.0  |  Critical: above 5.0")
        battery       = st.number_input("Battery Voltage (V)",        9.0,  16.0, float(default.get("battery_voltage",   13.5)), 0.1,
                                         help="Normal: 13.0–14.5V")

    with col3:
        st.markdown("**Operation Details**")
        hours_today  = st.number_input("Hours Operated Today",       0.0, 24.0, float(default.get("hours_today", 8.0)), 0.5)
        idle_hours   = st.number_input("Idle Hours Today",           0.0, 12.0, float(default.get("idle_hours",  1.0)), 0.1)
        days_maint   = st.number_input("Days Since Last Service",   0,   500,  int(default.get("days_since_maintenance", 90)))
        operator_on  = st.text_input("Operator on Duty", value=default.get("operator_id", ""))
        is_night     = st.checkbox("Night Shift")

    st.markdown("---")

    if st.button("Assess machine condition"):

        # Feature engineering - must exactly match training
        usage_ratio = min(cumulative_hours / TYPE_MAX.get(machine_type, 6000), 1.0)
        temp_over   = max(temperature - 90,   0)
        vibe_over   = max(vibration   - 4.0,  0)
        oil_deficit = max(60 - oil_pressure,  0)
        contam_flag = 1 if oil_contam > 3.0 else 0
        maint_due   = 1 if days_maint > 150  else 0
        type_enc    = le_type.transform([machine_type])[0]
        site_enc    = le_site.transform([machine_site])[0]
        now         = datetime.now()

        row = np.array([[
            age_years, hours_today, cumulative_hours, days_maint,
            temperature, vibration, oil_pressure, oil_contam,
            battery, idle_hours, maint_due,
            type_enc, site_enc,
            now.weekday(), now.month, int(is_night),
            temp_over, vibe_over, oil_deficit,
            contam_flag, usage_ratio
        ]])

        prob = model.predict_proba(row)[0][1] * 100

        # Determine level
        if prob >= 60:
            level  = "CRITICAL"
            bg     = "#450a0a"
            border = "#ef4444"
            icon   = "CRITICAL"
            colour = "#fca5a5"
        elif prob >= 35:
            level  = "HIGH RISK"
            bg     = "#431407"
            border = "#f97316"
            icon   = "HIGH"
            colour = "#fed7aa"
        elif prob >= 15:
            level  = "CAUTION"
            bg     = "#422006"
            border = "#f59e0b"
            icon   = "CAUTION"
            colour = "#fde68a"
        else:
            level  = "HEALTHY"
            bg     = "#052e16"
            border = "#22c55e"
            icon   = "NORMAL"
            colour = "#86efac"

        # ── Result banner ─────────────────────────────────────────
        mid_label = machine_id_input if machine_id_input else machine_type
        st.markdown(f"""
        <div style="background:{bg};border:2px solid {border};border-radius:14px;
                    padding:2rem;margin:1rem 0;text-align:center;">
          <div style="font-size:2.5rem;font-weight:800;color:{colour};
                      font-family:'Barlow Condensed',sans-serif;letter-spacing:.04em">{level}</div>
          <div style="font-size:1rem;color:#d5cbc1;margin-top:.5rem">
            {mid_label} &nbsp;·&nbsp; {prob:.0f}% chance of breakdown in next 7 days
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── What's wrong ──────────────────────────────────────────
        st.markdown("### Inspection Findings")
        issues_found = False
        cols_warn = st.columns(2)
        warn_list  = []

        if temperature > 105:  warn_list.append(("CRITICAL · Engine Too Hot",        f"Temperature is {temperature}°C: safe limit is 90°C. Risk of seizure."))
        elif temperature > 90: warn_list.append(("HIGH · Engine Running Warm",   f"Temperature {temperature}°C is above the 90°C safe mark. Monitor closely."))
        if vibration > 5.0:    warn_list.append(("CRITICAL · Severe Shaking",        f"Vibration at {vibration}: safe limit is 4.0. Bearing or shaft damage likely."))
        elif vibration > 4.0:  warn_list.append(("HIGH · Elevated Shaking",      f"Vibration at {vibration}: just above the safe limit of 4.0."))
        if oil_pressure < 45:  warn_list.append(("CRITICAL · Oil Pressure",  f"Only {oil_pressure} PSI: minimum safe is 60 PSI. Shut down immediately."))
        elif oil_pressure < 60:warn_list.append(("HIGH · Oil Pressure Low",       f"Oil pressure {oil_pressure} PSI is below the 60 PSI safe threshold."))
        if oil_contam > 5:     warn_list.append(("CRITICAL · Oil Contamination",         f"Contamination at {oil_contam} ppm: oil needs immediate change."))
        elif oil_contam > 3:   warn_list.append(("HIGH · Oil Contamination",      f"Contamination at {oil_contam} ppm: above the 3.0 ppm safe limit."))
        if days_maint > 200:   warn_list.append(("CRITICAL · Service Severely Overdue",       f"{days_maint} days since last service: limit is 150 days."))
        elif days_maint > 150: warn_list.append(("HIGH · Service Overdue",    f"{days_maint} days since last service: past the 150 day limit."))
        if battery < 11.5:     warn_list.append(("CAUTION · Battery Low",            f"Battery at {battery}V: should be 13.0–14.5V."))
        if idle_hours > 3:     warn_list.append(("CAUTION · High Idle Time",         f"{idle_hours} hrs idle today: fuel being wasted."))

        if not warn_list:
            st.success("All readings are within normal limits. Machine condition is healthy.")
        else:
            issues_found = True
            for i, (title, desc) in enumerate(warn_list):
                col = cols_warn[i % 2]
                with col:
                    color = "#ef4444" if "CRITICAL" in title else "#f97316" if "HIGH" in title else "#f59e0b"
                    st.markdown(f"""
                    <div style="background:#fff;border:1px solid #d9d0c4;border-left:5px solid {color};
                                border-radius:2px;padding:.9rem;margin:.4rem 0;">
                      <b style="color:{color}">{title}</b><br>
                      <span style="font-size:.85rem;color:#5f554c">{desc}</span>
                    </div>
                    """, unsafe_allow_html=True)

        # ── Action plan ───────────────────────────────────────────
        st.markdown("### Required Response")

        if level == "CRITICAL":
            st.markdown("""
            <div class="alert-critical">
            <h3 style="color:#fca5a5;margin-top:0">STOP THIS MACHINE NOW</h3>
            <p><b>Step 1:</b> Radio the operator immediately: do NOT wait for end of shift</p>
            <p><b>Step 2:</b> Ground the machine: no more operation until cleared by a technician</p>
            <p><b>Step 3:</b> Contact the Maintenance Supervisor to schedule an emergency inspection</p>
            <p><b>Step 4:</b> Log this job in the Job Board below so it is tracked</p>
            <p><b>Step 5:</b> Do not reassign this machine to any shift until it receives the all-clear</p>
            <hr style="border-color:#7f1d1d;margin:.8rem 0">
            <p style="margin:0"><b>If you act now:</b> ~P80,000 service cost</p>
            <p style="margin:0"><b>If you ignore it:</b> P450,000–P600,000 emergency repair + production halt</p>
            </div>
            """, unsafe_allow_html=True)

        elif level == "HIGH RISK":
            st.markdown("""
            <div class="alert-high">
            <h3 style="color:#fed7aa;margin-top:0">SERVICE THIS MACHINE WITHIN 48 HOURS</h3>
            <p><b>Step 1:</b> Do not schedule this machine for overtime or double shifts</p>
            <p><b>Step 2:</b> Assign only experienced operators until it is serviced</p>
            <p><b>Step 3:</b> Book maintenance for within the next 2 days</p>
            <p><b>Step 4:</b> Check and top up oil and coolant at the start of tomorrow's shift</p>
            <p><b>Step 5:</b> Log this in the Job Board to track it</p>
            </div>
            """, unsafe_allow_html=True)

        elif level == "CAUTION":
            st.markdown("""
            <div class="alert-medium">
            <h3 style="color:#fde68a;margin-top:0">SCHEDULE A SERVICE THIS WEEK</h3>
            <p><b>Step 1:</b> Continue normal operations but check readings every shift</p>
            <p><b>Step 2:</b> Book routine maintenance within the next 7 days</p>
            <p><b>Step 3:</b> Flag for technician check at the start of tomorrow's shift</p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="alert-ok">
            <h3 style="color:#b9d7af;margin-top:0">MACHINE IS HEALTHY: NO ACTION NEEDED</h3>
            <p>All readings are within safe limits. Continue normal operations.</p>
            <p>Re-check at the next scheduled inspection or in 7 days.</p>
            </div>
            """, unsafe_allow_html=True)

        # ── Quick log to job board ─────────────────────────────────
        if level in ("CRITICAL", "HIGH RISK", "CAUTION"):
            st.markdown("---")
            st.markdown("### Create a Maintenance Job")
            priority_map = {"CRITICAL":"Emergency","HIGH RISK":"Urgent","CAUTION":"Scheduled"}
            jcol1, jcol2 = st.columns(2)
            with jcol1:
                job_notes = st.text_area("Notes for maintenance team", placeholder="e.g. Engine overheating, oil change needed, check bearings...")
            with jcol2:
                job_due   = st.date_input("Job due by", value=date.today() + timedelta(days=(1 if level=="CRITICAL" else 2 if level=="HIGH RISK" else 7)))
                job_tech  = st.text_input("Assign to technician", placeholder="Technician name")

            if st.button("Create maintenance job", key="log_job"):
                st.session_state.jobs.append({
                    "id":         f"JOB-{len(st.session_state.jobs)+1:04d}",
                    "machine":    mid_label,
                    "type":       machine_type,
                    "site":       machine_site,
                    "priority":   priority_map[level],
                    "issue":      level,
                    "notes":      job_notes,
                    "due":        str(job_due),
                    "technician": job_tech,
                    "logged_by":  "Fleet Manager",
                    "logged_at":  datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "status":     "Pending",
                })
                st.success("Maintenance job created. Open the Job Board to track it.")

# ════════════════════════════════════════════════════════════════
# PAGE 2 - JOB BOARD (Track all pending maintenance jobs)
# ════════════════════════════════════════════════════════════════
elif nav == "Job board":

    st.markdown('<div class="topbar"><h1>Maintenance Job Board</h1><p>Plan, assign and close every fleet maintenance work order.</p></div>', unsafe_allow_html=True)

    # Auto-populate from risk scores on first load
    if len(st.session_state.jobs) == 0:
        for _, row in risk_df[risk_df["risk_level"].isin(["Critical","High"])].iterrows():
            st.session_state.jobs.append({
                "id":         f"JOB-{len(st.session_state.jobs)+1:04d}",
                "machine":    row["machine_id"],
                "type":       row["machine_type"],
                "site":       row["site"],
                "priority":   "Emergency" if row["risk_level"] == "Critical" else "Urgent",
                "issue":      row["risk_level"],
                "notes":      f"Auto-flagged: risk score {row['fail_prob']*100:.0f}%",
                "due":        str(date.today() + timedelta(days=1)),
                "technician": "Unassigned",
                "logged_by":  "System",
                "logged_at":  datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status":     "Pending",
            })

    jobs = st.session_state.jobs
    f1, f2, f3 = st.columns([1.4, 1, 1])
    with f1:
        job_search = st.text_input("Find a work order", placeholder="Job ID or machine ID", key="job_search")
    with f2:
        site_filter = st.multiselect("Site", sorted({j["site"] for j in jobs}), key="job_site")
    with f3:
        priority_filter = st.multiselect("Priority", sorted({j["priority"] for j in jobs}), key="job_priority")
    visible_jobs = jobs
    if job_search:
        term = job_search.lower()
        visible_jobs = [j for j in visible_jobs if term in str(j.get("id", "")).lower() or term in str(j.get("machine", "")).lower()]
    if site_filter:
        visible_jobs = [j for j in visible_jobs if j["site"] in site_filter]
    if priority_filter:
        visible_jobs = [j for j in visible_jobs if j["priority"] in priority_filter]
    pending   = [j for j in visible_jobs if j["status"] == "Pending"]
    in_prog   = [j for j in visible_jobs if j["status"] == "In Progress"]
    completed = [j for j in visible_jobs if j["status"] == "Completed"]
    st.markdown(f'<div class="data-hint">Showing {len(visible_jobs)} of {len(jobs)} work orders. Change status directly from the board as work progresses.</div>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("red",    f"{len(pending)}",   "Pending Jobs",     "Waiting to be done"), unsafe_allow_html=True)
    c2.markdown(kcard("orange", f"{len(in_prog)}",   "In Progress",      "Being worked on now"), unsafe_allow_html=True)
    c3.markdown(kcard("green",  f"{len(completed)}", "Completed",        "Jobs done"), unsafe_allow_html=True)
    c4.markdown(kcard("blue",   f"{len(visible_jobs)}", "Matching Jobs", "Current filters"), unsafe_allow_html=True)

    st.markdown("---")

    # ── Add new job manually ──────────────────────────────────────
    with st.expander("➕ Add a New Job Manually"):
        nc1,nc2,nc3 = st.columns(3)
        with nc1:
            nj_machine  = st.text_input("Machine ID")
            nj_type     = st.selectbox("Machine Type", MACHINE_TYPES, key="nj_type")
            nj_site     = st.selectbox("Site", SITES, key="nj_site")
        with nc2:
            nj_priority = st.selectbox("Priority", ["Emergency","Urgent","Scheduled","Routine"])
            nj_due      = st.date_input("Due By", key="nj_due")
            nj_tech     = st.text_input("Assign To", key="nj_tech")
        with nc3:
            nj_notes    = st.text_area("Job Description", key="nj_notes", height=100)

        if st.button("Add Job to Board", key="add_job"):
            if nj_machine and nj_notes:
                st.session_state.jobs.append({
                    "id":         f"JOB-{len(st.session_state.jobs)+1:04d}",
                    "machine":    nj_machine,
                    "type":       nj_type,
                    "site":       nj_site,
                    "priority":   nj_priority,
                    "issue":      "Manual",
                    "notes":      nj_notes,
                    "due":        str(nj_due),
                    "technician": nj_tech,
                    "logged_by":  "Fleet Manager",
                    "logged_at":  datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "status":     "Pending",
                })
                st.success("✅ Job added!"); st.rerun()
            else:
                st.error("Fill in machine ID and job description.")

    st.markdown("---")

    # ── Pending jobs ──────────────────────────────────────────────
    st.markdown("### Pending Jobs")
    if not pending:
        st.success("✅ No pending jobs right now!")
    else:
        for i, job in enumerate(visible_jobs):
            if job["status"] != "Pending": continue
            j_idx = jobs.index(job)
            with st.container():
                jc1,jc2,jc3,jc4 = st.columns([3,2,2,1])
                with jc1:
                    st.markdown(f"**{job['id']}** · {job['machine']} ({job['type']}) · {job['site']}")
                    st.markdown(f"{job['priority']}  ·  Due: **{job['due']}**")
                    st.caption(job['notes'][:120])
                with jc2:
                    st.markdown(f"Technician: {job['technician'] or 'Unassigned'}")
                    st.caption(f"Logged: {job['logged_at']}")
                with jc3:
                    new_status = st.selectbox("Update Status", ["Pending","In Progress","Completed"],
                                              key=f"status_{j_idx}")
                    if new_status != job["status"]:
                        st.session_state.jobs[j_idx]["status"] = new_status
                        st.rerun()
                with jc4:
                    if st.button("Remove", key=f"del_{j_idx}"):
                        st.session_state[f"confirm_del_{j_idx}"] = True
                if st.session_state.get(f"confirm_del_{j_idx}"):
                    st.warning(f"Remove {job['id']} from the job board? This cannot be undone in the current session.")
                    confirm_col, cancel_col = st.columns(2)
                    if confirm_col.button("Confirm removal", key=f"confirm_{j_idx}"):
                        st.session_state.jobs.pop(j_idx)
                        st.session_state.pop(f"confirm_del_{j_idx}", None)
                        st.rerun()
                    if cancel_col.button("Keep job", key=f"cancel_{j_idx}"):
                        st.session_state.pop(f"confirm_del_{j_idx}", None)
                        st.rerun()
                st.markdown("---")

    # ── In progress ───────────────────────────────────────────────
    if in_prog:
        st.markdown("### In Progress")
        for job in in_prog:
            j_idx = jobs.index(job)
            jc1,jc2,jc3 = st.columns([4,2,2])
            with jc1:
                st.markdown(f"**{job['id']}** · {job['machine']} · {job['priority']}")
                st.caption(job['notes'][:120])
            with jc2:
                st.markdown(f"Technician: {job['technician']}")
            with jc3:
                completion_note = st.text_input("Completion evidence", placeholder="Work completed or reference", key=f"completion_{j_idx}")
                if st.button("Mark complete", key=f"done_{j_idx}", disabled=not completion_note.strip()):
                    st.session_state.jobs[j_idx]["status"] = "Completed"
                    st.session_state.jobs[j_idx]["completion_note"] = completion_note
                    st.session_state.jobs[j_idx]["completed_at"] = datetime.now().strftime("%d %b %Y, %H:%M")
                    st.rerun()

    # ── Completed ─────────────────────────────────────────────────
    if completed:
        with st.expander(f"✅ Completed Jobs ({len(completed)})"):
            for job in completed:
                st.markdown(f"✅ **{job['id']}** · {job['machine']} · {job['notes'][:80]}")

    # ── Export ────────────────────────────────────────────────────
    if jobs:
        csv = pd.DataFrame(jobs).to_csv(index=False).encode()
        st.download_button("Export job list", csv, "job_board.csv", "text/csv")

# ════════════════════════════════════════════════════════════════
# PAGE 3 - LOG A SERVICE (Record completed maintenance)
# ════════════════════════════════════════════════════════════════
elif nav == "Log service":

    st.markdown('<div class="topbar"><h1>Log a Completed Service</h1><p>Maintain a reliable service history for every asset in the fleet.</p></div>', unsafe_allow_html=True)

    st.markdown("### Service Record")
    col1, col2 = st.columns(2)

    with col1:
        s_machine   = st.selectbox("Machine ID", sorted(df["machine_id"].unique()))
        s_type      = st.text_input("Machine Type", value=df[df["machine_id"]==s_machine]["machine_type"].iloc[-1])
        s_site      = st.text_input("Site", value=df[df["machine_id"]==s_machine]["site"].iloc[-1])
        s_date      = st.date_input("Date of Service", value=date.today())
        s_tech      = st.text_input("Technician Name")

    with col2:
        s_type_work = st.multiselect("Work Done", [
            "Oil & Filter Change", "Engine Tune-Up", "Brake Service",
            "Hydraulic Check", "Tyre Rotation/Replacement", "Cooling System Flush",
            "Bearing Replacement", "Belt/Chain Service", "Electrical Check",
            "Full Inspection", "Emergency Repair", "Other"
        ])
        s_parts     = st.text_area("Parts Replaced (list them)", height=80, placeholder="e.g. Oil filter x1, Drive belt x2...")
        s_cost      = st.number_input("Service Cost (BWP)", 0, 2000000, 80000, 1000)
        s_hours     = st.number_input("Hours Worked", 0.5, 48.0, 4.0, 0.5)
        s_notes     = st.text_area("Additional Notes", height=80, placeholder="Any issues found, recommendations...")

    st.markdown("---")
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("Save service record"):
            if s_tech and s_type_work:
                st.session_state.services.append({
                    "machine_id":   s_machine,
                    "machine_type": s_type,
                    "site":         s_site,
                    "date":         str(s_date),
                    "technician":   s_tech,
                    "work_done":    ", ".join(s_type_work),
                    "parts":        s_parts,
                    "cost_bwp":     s_cost,
                    "hours_worked": s_hours,
                    "notes":        s_notes,
                    "logged_at":    datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
                st.success(f"✅ Service record saved for {s_machine}!")
            else:
                st.error("Fill in at least the technician name and work done.")

    st.markdown("---")
    st.markdown("### Service History")
    if st.session_state.services:
        sdf = pd.DataFrame(st.session_state.services)
        sf1, sf2 = st.columns([1.4, 1])
        with sf1:
            service_search = st.text_input("Find a service record", placeholder="Machine ID or technician", key="service_search")
        with sf2:
            service_site = st.multiselect("Service site", sorted(sdf["site"].dropna().unique()), key="service_site")
        if service_search:
            smask = sdf["machine_id"].astype(str).str.contains(service_search, case=False, na=False) | sdf["technician"].astype(str).str.contains(service_search, case=False, na=False)
            sdf = sdf[smask]
        if service_site:
            sdf = sdf[sdf["site"].isin(service_site)]
        st.markdown(f'<div class="data-hint">Showing {len(sdf)} service records.</div>', unsafe_allow_html=True)
        sdf["cost_bwp"] = sdf["cost_bwp"].apply(lambda x: f"P{x:,.0f}")
        sdf.columns     = ["Machine","Type","Site","Date","Technician",
                           "Work Done","Parts","Cost","Hrs Worked","Notes","Logged"]
        st.dataframe(sdf, use_container_width=True)
        csv = pd.DataFrame(st.session_state.services).to_csv(index=False).encode()
        st.download_button("Export service records", csv, "service_history.csv", "text/csv")
    else:
        st.info("No service records logged yet. Use the form above to log completed work.")

# ════════════════════════════════════════════════════════════════
# PAGE 4 - FLEET HEALTH (Simple summary of all 80 machines)
# ════════════════════════════════════════════════════════════════
elif nav == "Fleet health":

    st.markdown('<div class="topbar"><h1>Fleet Condition Summary</h1><p>Current equipment risk based on the latest available sensor readings.</p></div>', unsafe_allow_html=True)

    rc = risk_df["risk_level"].value_counts()
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("red",    f"{rc.get('Critical',0)}",  "Need Immediate Action", "Critical risk"), unsafe_allow_html=True)
    c2.markdown(kcard("orange", f"{rc.get('High',0)}",      "Service Within 48 Hrs", "High risk"), unsafe_allow_html=True)
    c3.markdown(kcard("blue",   f"{rc.get('Medium',0)}",    "Service This Week",     "Medium risk"), unsafe_allow_html=True)
    c4.markdown(kcard("green",  f"{rc.get('Low',0)}",       "Healthy: No Action",   "Good condition"), unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("#### All 80 Machines: Sorted by Risk")
        display = risk_df[[
            "machine_id","machine_type","site","risk_level",
            "days_since_maintenance","engine_temp_c","vibration"
        ]].copy().sort_values(
            "risk_level",
            key=lambda x: x.map({"Critical":0,"High":1,"Medium":2,"Low":3})
        ).reset_index(drop=True)
        display["engine_temp_c"] = display["engine_temp_c"].apply(lambda x: f"{x:.1f}°C")
        display["vibration"]     = display["vibration"].apply(lambda x: f"{x:.2f}")
        display["days_since_maintenance"] = display["days_since_maintenance"].apply(lambda x: f"{x} days")

        def row_color(val):
            return {"Critical":"background-color:#f5d9d2;color:#7d2115;font-weight:bold",
                    "High":    "background-color:#f5e0cf;color:#743113;font-weight:bold",
                    "Medium":  "background-color:#f4e9c8;color:#684b0c",
                    "Low":     "background-color:#dfe9da;color:#294a25"}.get(val,"")

        display.columns = ["Machine","Type","Site","Status","Days Since Service","Temp","Vibration"]
        st.dataframe(display.style.applymap(row_color, subset=["Status"]),
                     use_container_width=True, height=500)

    with col2:
        st.markdown("#### Fleet Condition Breakdown")
        fig = px.pie(names=rc.index, values=rc.values, hole=0.5,
                     color=rc.index,
                     color_discrete_map={"Critical":"#ef4444","High":"#f97316",
                                         "Medium":"#f59e0b","Low":"#22c55e"})
        fig.update_layout(paper_bgcolor="#f8f5ef",plot_bgcolor="#f8f5ef",
                          font_color="#171411",font_family="IBM Plex Sans",height=280,margin=dict(t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Machines Most Overdue for Service")
        overdue = risk_df[risk_df["days_since_maintenance"] > 150].sort_values(
            "days_since_maintenance", ascending=False).head(8)
        if len(overdue):
            for _, r in overdue.iterrows():
                st.markdown(f"`{r['machine_id']}`: **{r['days_since_maintenance']:.0f} days** since service", unsafe_allow_html=True)
        else:
            st.success("All machines up to date!")

# ════════════════════════════════════════════════════════════════
# PAGE 5 - MACHINE RECORDS (Full sensor history for one machine)
# ════════════════════════════════════════════════════════════════
elif nav == "Machine records":

    st.markdown('<div class="topbar"><h1>Machine Records</h1><p>Review sensor history, condition trends and completed services for any asset.</p></div>', unsafe_allow_html=True)

    machine_id = st.selectbox("Select a Machine", sorted(df["machine_id"].unique()))
    mdata      = df[df["machine_id"] == machine_id].sort_values("date")
    last       = mdata.iloc[-1]

    # Machine info bar
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("blue",  last["machine_type"],             "Machine Type",      ""), unsafe_allow_html=True)
    c2.markdown(kcard("blue",  last["site"],                     "Location",          ""), unsafe_allow_html=True)
    c3.markdown(kcard("blue",  f"{last['cumulative_hours']:,.0f} hrs","Engine Hours",  "Total lifetime"), unsafe_allow_html=True)
    c4.markdown(kcard("orange" if last["days_since_maintenance"]>150 else "green",
                      f"{last['days_since_maintenance']} days","Since Last Service",
                      "Overdue" if last["days_since_maintenance"]>150 else "Up to date"), unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    def line_chart(x, y, colour, warning_val=None, warning_label="", crit_val=None):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=colour, width=2)))
        if warning_val:
            fig.add_hline(y=warning_val, line_dash="dot", line_color="#f97316",
                          annotation_text=warning_label, annotation_position="bottom right")
        if crit_val:
            fig.add_hline(y=crit_val, line_dash="dot", line_color="#ef4444",
                          annotation_text="Critical", annotation_position="bottom right")
        fig.update_layout(plot_bgcolor="#f8f5ef",paper_bgcolor="#f8f5ef",
                          font_color="#171411",font_family="IBM Plex Sans",height=260,
                          margin=dict(t=10,b=10,l=5,r=5),showlegend=False)
        fig.update_xaxes(gridcolor="#ded6cc")
        fig.update_yaxes(gridcolor="#ded6cc")
        return fig

    with col1:
        st.markdown("**Engine Temperature Over Time**")
        st.plotly_chart(line_chart(mdata["date"], mdata["engine_temp_c"], "#f87171",
                                   warning_val=90, warning_label="Warning (90°C)",
                                   crit_val=105), use_container_width=True)

        st.markdown("**Oil Pressure Over Time**")
        st.plotly_chart(line_chart(mdata["date"], mdata["oil_pressure_psi"], "#34d399",
                                   warning_val=60, warning_label="Min safe (60 PSI)"),
                        use_container_width=True)

    with col2:
        st.markdown("**Vibration Level Over Time**")
        st.plotly_chart(line_chart(mdata["date"], mdata["vibration"], "#fb923c",
                                   warning_val=4.0, warning_label="Warning (4.0)",
                                   crit_val=5.0), use_container_width=True)

        st.markdown("**Daily Fuel Cost**")
        fig_fuel = go.Figure()
        fig_fuel.add_trace(go.Bar(x=mdata["date"], y=mdata["fuel_cost_bwp"],
                                  marker_color="#b44e2b"))
        fig_fuel.update_layout(plot_bgcolor="#f8f5ef",paper_bgcolor="#f8f5ef",
                                font_color="#171411",font_family="IBM Plex Sans",height=260,
                                margin=dict(t=10,b=10,l=5,r=5),showlegend=False)
        st.plotly_chart(fig_fuel, use_container_width=True)

    # Breakdown history
    bds = mdata[mdata["breakdown"] == 1]
    st.markdown("---")
    if len(bds):
        st.markdown(f"### Breakdown History: {len(bds)} incident(s) on record")
        show = bds[["date","shift","operator_id","engine_temp_c","vibration","repair_cost_bwp"]].copy()
        show["repair_cost_bwp"] = show["repair_cost_bwp"].apply(lambda x: f"P{x:,.0f}")
        show.columns = ["Date","Shift","Operator","Temp at Breakdown","Vibration","Repair Cost"]
        st.dataframe(show.reset_index(drop=True), use_container_width=True)
    else:
        st.success(f"No breakdowns on record for {machine_id}.")

    # Service records for this machine
    if st.session_state.services:
        mach_services = [s for s in st.session_state.services if s["machine_id"] == machine_id]
        if mach_services:
            st.markdown(f"### Service Records: {len(mach_services)} logged")
            st.dataframe(pd.DataFrame(mach_services), use_container_width=True)

# ── FOOTER ────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<div style='text-align:center;color:#475569;font-size:.78rem'>Kgosi Mining Solutions · Maintenance Management System · Unaswi Leonard · 2026</div>", unsafe_allow_html=True)
