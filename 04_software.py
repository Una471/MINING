"""
KGOSI MINING SOLUTIONS — MAINTENANCE MANAGEMENT SYSTEM
The software that solves the problem.
Fleet Manager uses this daily to: check machines, log jobs, track repairs, manage alerts.
Run: streamlit run 04_software.py --server.port 8502
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib, json
from datetime import datetime, date, timedelta

st.set_page_config(page_title="Kgosi Mining | Maintenance System", page_icon="🛠️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#0f172a;color:#e2e8f0;}
h1,h2,h3{font-weight:700;}
.topbar{background:linear-gradient(135deg,#1e293b,#0f172a);padding:1.2rem 1.5rem;
         border-radius:12px;margin-bottom:1.2rem;border:1px solid #1e293b;}
.topbar h1{margin:0;font-size:1.4rem;color:#f1f5f9;}
.topbar p{margin:.2rem 0 0;opacity:.55;font-size:.82rem;}
.kcard{background:#1e293b;border-radius:10px;padding:1.1rem 1.3rem;
        border:1px solid #2d3748;margin-bottom:.3rem;}
.kcard.red   {border-top:3px solid #ef4444;}
.kcard.orange{border-top:3px solid #f97316;}
.kcard.green {border-top:3px solid #22c55e;}
.kcard.blue  {border-top:3px solid #3b82f6;}
.kval{font-size:1.8rem;font-weight:700;line-height:1.1;color:#f1f5f9;}
.klbl{font-size:.7rem;text-transform:uppercase;letter-spacing:1.5px;color:#94a3b8;margin-top:.3rem;}
.ksub{font-size:.76rem;color:#64748b;margin-top:.3rem;}

/* Alert boxes */
.alert-critical{background:#450a0a;border:1px solid #991b1b;border-radius:10px;padding:1.2rem;margin:.5rem 0;}
.alert-high    {background:#431407;border:1px solid #9a3412;border-radius:10px;padding:1.2rem;margin:.5rem 0;}
.alert-medium  {background:#422006;border:1px solid #92400e;border-radius:10px;padding:1.2rem;margin:.5rem 0;}
.alert-ok      {background:#052e16;border:1px solid #166534;border-radius:10px;padding:1.2rem;margin:.5rem 0;}

/* Machine check result */
.result-box{border-radius:12px;padding:1.8rem;margin:1rem 0;text-align:center;}

/* Job cards */
.job-card{background:#1e293b;border-radius:10px;padding:1rem 1.2rem;
           border-left:4px solid #3b82f6;margin:.5rem 0;}
.job-card.urgent{border-left-color:#ef4444;}
.job-card.done  {border-left-color:#22c55e;opacity:.7;}

/* Sidebar */
section[data-testid="stSidebar"]{background:#0f172a!important;border-right:1px solid #1e293b;}
section[data-testid="stSidebar"] *{color:#e2e8f0!important;}

/* Inputs */
.stTextInput input,.stNumberInput input,.stSelectbox select{
    background:#1e293b!important;color:#f1f5f9!important;border:1px solid #334155!important;}
.stButton>button{background:#3b82f6;color:white;border:none;border-radius:8px;
                  padding:.6rem 1.5rem;font-weight:600;width:100%;}
.stButton>button:hover{background:#2563eb;}
.stButton>button.secondary{background:#1e293b;border:1px solid #334155;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── LOAD ──────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    m  = joblib.load("model.pkl")
    lt = joblib.load("le_type.pkl")
    ls = joblib.load("le_site.pkl")
    with open("features.json") as f: feat = json.load(f)
    return m, lt, ls, feat

@st.cache_data
def load_data():
    df   = pd.read_csv("equipment_data.csv", parse_dates=["date"])
    risk = pd.read_csv("risk_scores.csv")
    return df, risk

model, le_type, le_site, FEATURES = load_model()
df, risk_df = load_data()

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
    fig.update_layout(plot_bgcolor="#0f172a",paper_bgcolor="#0f172a",
                      font_color="#e2e8f0",height=h,margin=dict(t=15,b=15,l=5,r=5))
    return fig

# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛠️ Maintenance System")
    st.markdown("*Kgosi Mining Solutions*")
    st.markdown("---")
    nav = st.radio("Go to", [
        "🚨  Machine Check",
        "📋  Job Board",
        "🔧  Log a Service",
        "📊  Fleet Health",
        "📁  Machine Records",
    ])
    st.markdown("---")
    pending_jobs = len([j for j in st.session_state.jobs if j["status"] == "Pending"])
    critical_now = (risk_df["risk_level"] == "Critical").sum()
    st.markdown(f"🔴 **Critical machines:** {critical_now}")
    st.markdown(f"📋 **Pending jobs:** {pending_jobs}")

# ════════════════════════════════════════════════════════════════
# PAGE 1 — MACHINE CHECK (Core tool: type in readings, get risk + action)
# ════════════════════════════════════════════════════════════════
if nav == "🚨  Machine Check":

    st.markdown('<div class="topbar"><h1>🚨 Machine Health Check</h1><p>Enter the machine\'s sensor readings from today\'s inspection to get an instant health assessment and action plan</p></div>', unsafe_allow_html=True)

    # Optionally pre-fill from existing machine
    machine_ids = ["— Type readings manually —"] + sorted(df["machine_id"].unique().tolist())
    chosen = st.selectbox("📎 Pre-fill from a machine's last recorded readings:", machine_ids)
    default = df[df["machine_id"] == chosen].sort_values("date").iloc[-1].to_dict() if chosen != "— Type readings manually —" else {}

    st.markdown("---")
    st.markdown("### 📝 Enter Today's Inspection Readings")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Machine Details**")
        machine_type = st.selectbox("Machine Type", MACHINE_TYPES,
            index=MACHINE_TYPES.index(default.get("machine_type", MACHINE_TYPES[0])) if "machine_type" in default else 0)
        machine_site = st.selectbox("Site", SITES,
            index=SITES.index(default.get("site", SITES[0])) if "site" in default else 0)
        machine_id_input = st.text_input("Machine ID (optional)", value=chosen if chosen != "— Type readings manually —" else "")
        age_years        = st.number_input("Age of Machine (years)", 1, 20, int(default.get("age_years", 5)))
        cumulative_hours = st.number_input("Total Hours on Engine",  100, 15000, int(default.get("cumulative_hours", 2500)))

    with col2:
        st.markdown("**Sensor Readings from Inspection**")
        temperature   = st.number_input("🌡️ Engine Temperature (°C)",   50.0, 160.0, float(default.get("engine_temp_c",   78.0)), 0.5,
                                         help="Normal: below 90°C  |  Warning: 90–105°C  |  Critical: above 105°C")
        vibration     = st.number_input("📳 Vibration Level",            0.5,  12.0, float(default.get("vibration",       2.5)),  0.1,
                                         help="Normal: below 4.0  |  Warning: 4.0–5.0  |  Critical: above 5.0")
        oil_pressure  = st.number_input("🛢️ Oil Pressure (PSI)",         10.0, 100.0, float(default.get("oil_pressure_psi", 65.0)), 0.5,
                                         help="Normal: above 60 PSI  |  Warning: 45–60  |  Critical: below 45")
        oil_contam    = st.number_input("🔬 Oil Contamination (ppm)",    0.0,  15.0, float(default.get("oil_contamination_ppm", 1.5)), 0.1,
                                         help="Normal: below 3.0  |  Warning: 3.0–5.0  |  Critical: above 5.0")
        battery       = st.number_input("🔋 Battery Voltage (V)",        9.0,  16.0, float(default.get("battery_voltage",   13.5)), 0.1,
                                         help="Normal: 13.0–14.5V")

    with col3:
        st.markdown("**Operation Details**")
        hours_today  = st.number_input("⏱️ Hours Operated Today",       0.0, 24.0, float(default.get("hours_today", 8.0)), 0.5)
        idle_hours   = st.number_input("😴 Idle Hours Today",           0.0, 12.0, float(default.get("idle_hours",  1.0)), 0.1)
        days_maint   = st.number_input("🔧 Days Since Last Serviced",   0,   500,  int(default.get("days_since_maintenance", 90)))
        operator_on  = st.text_input("👷 Operator on Duty", value=default.get("operator_id", ""))
        is_night     = st.checkbox("🌙 Night Shift?")

    st.markdown("---")

    if st.button("🔍  CHECK THIS MACHINE NOW"):

        # Feature engineering — must exactly match training
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
            icon   = "🔴"
            colour = "#fca5a5"
        elif prob >= 35:
            level  = "HIGH RISK"
            bg     = "#431407"
            border = "#f97316"
            icon   = "🟠"
            colour = "#fed7aa"
        elif prob >= 15:
            level  = "CAUTION"
            bg     = "#422006"
            border = "#f59e0b"
            icon   = "🟡"
            colour = "#fde68a"
        else:
            level  = "HEALTHY"
            bg     = "#052e16"
            border = "#22c55e"
            icon   = "🟢"
            colour = "#86efac"

        # ── Result banner ─────────────────────────────────────────
        mid_label = machine_id_input if machine_id_input else machine_type
        st.markdown(f"""
        <div style="background:{bg};border:2px solid {border};border-radius:14px;
                    padding:2rem;margin:1rem 0;text-align:center;">
          <div style="font-size:3rem;margin-bottom:.5rem">{icon}</div>
          <div style="font-size:2.5rem;font-weight:800;color:{colour};
                      font-family:Inter,sans-serif">{level}</div>
          <div style="font-size:1rem;color:#94a3b8;margin-top:.5rem">
            {mid_label} &nbsp;·&nbsp; {prob:.0f}% chance of breakdown in next 7 days
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── What's wrong ──────────────────────────────────────────
        st.markdown("### ⚡ Issues Found")
        issues_found = False
        cols_warn = st.columns(2)
        warn_list  = []

        if temperature > 105:  warn_list.append(("🔴 Engine Too Hot",        f"Temperature is {temperature}°C — safe limit is 90°C. Risk of seizure."))
        elif temperature > 90: warn_list.append(("🟠 Engine Running Warm",   f"Temperature {temperature}°C is above the 90°C safe mark. Monitor closely."))
        if vibration > 5.0:    warn_list.append(("🔴 Severe Shaking",        f"Vibration at {vibration} — safe limit is 4.0. Bearing or shaft damage likely."))
        elif vibration > 4.0:  warn_list.append(("🟠 Elevated Shaking",      f"Vibration at {vibration} — just above the safe limit of 4.0."))
        if oil_pressure < 45:  warn_list.append(("🔴 Oil Pressure Critical",  f"Only {oil_pressure} PSI — minimum safe is 60 PSI. Shut down immediately."))
        elif oil_pressure < 60:warn_list.append(("🟠 Oil Pressure Low",       f"Oil pressure {oil_pressure} PSI is below the 60 PSI safe threshold."))
        if oil_contam > 5:     warn_list.append(("🔴 Oil Very Dirty",         f"Contamination at {oil_contam} ppm — oil needs immediate change."))
        elif oil_contam > 3:   warn_list.append(("🟠 Oil Getting Dirty",      f"Contamination at {oil_contam} ppm — above the 3.0 ppm safe limit."))
        if days_maint > 200:   warn_list.append(("🔴 Severely Overdue",       f"{days_maint} days since last service — limit is 150 days."))
        elif days_maint > 150: warn_list.append(("🟠 Overdue for Service",    f"{days_maint} days since last service — past the 150 day limit."))
        if battery < 11.5:     warn_list.append(("🟡 Battery Low",            f"Battery at {battery}V — should be 13.0–14.5V."))
        if idle_hours > 3:     warn_list.append(("🟡 High Idle Time",         f"{idle_hours} hrs idle today — fuel being wasted."))

        if not warn_list:
            st.success("✅ All readings are within normal limits. Machine is healthy.")
        else:
            issues_found = True
            for i, (title, desc) in enumerate(warn_list):
                col = cols_warn[i % 2]
                with col:
                    color = "#ef4444" if "🔴" in title else "#f97316" if "🟠" in title else "#f59e0b"
                    st.markdown(f"""
                    <div style="background:#1e293b;border-left:4px solid {color};
                                border-radius:8px;padding:.9rem;margin:.4rem 0;">
                      <b style="color:{color}">{title}</b><br>
                      <span style="font-size:.85rem;color:#94a3b8">{desc}</span>
                    </div>
                    """, unsafe_allow_html=True)

        # ── Action plan ───────────────────────────────────────────
        st.markdown("### 📋 What To Do")

        if level == "CRITICAL":
            st.markdown("""
            <div class="alert-critical">
            <h3 style="color:#fca5a5;margin-top:0">⛔ STOP THIS MACHINE NOW</h3>
            <p><b>Step 1:</b> Radio the operator immediately — do NOT wait for end of shift</p>
            <p><b>Step 2:</b> Ground the machine — no more operation until cleared by a technician</p>
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
            <h3 style="color:#fed7aa;margin-top:0">⚠️ SERVICE THIS MACHINE WITHIN 48 HOURS</h3>
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
            <h3 style="color:#fde68a;margin-top:0">📌 SCHEDULE A SERVICE THIS WEEK</h3>
            <p><b>Step 1:</b> Continue normal operations but check readings every shift</p>
            <p><b>Step 2:</b> Book routine maintenance within the next 7 days</p>
            <p><b>Step 3:</b> Flag for technician check at the start of tomorrow's shift</p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="alert-ok">
            <h3 style="color:#86efac;margin-top:0">✅ MACHINE IS HEALTHY — NO ACTION NEEDED</h3>
            <p>All readings are within safe limits. Continue normal operations.</p>
            <p>Re-check at the next scheduled inspection or in 7 days.</p>
            </div>
            """, unsafe_allow_html=True)

        # ── Quick log to job board ─────────────────────────────────
        if level in ("CRITICAL", "HIGH RISK", "CAUTION"):
            st.markdown("---")
            st.markdown("### ➕ Log This to the Job Board")
            priority_map = {"CRITICAL":"🔴 Emergency","HIGH RISK":"🟠 Urgent","CAUTION":"🟡 Scheduled"}
            jcol1, jcol2 = st.columns(2)
            with jcol1:
                job_notes = st.text_area("Notes for maintenance team", placeholder="e.g. Engine overheating, oil change needed, check bearings...")
            with jcol2:
                job_due   = st.date_input("Job due by", value=date.today() + timedelta(days=(1 if level=="CRITICAL" else 2 if level=="HIGH RISK" else 7)))
                job_tech  = st.text_input("Assign to technician", placeholder="Technician name")

            if st.button("📋 Log This Job", key="log_job"):
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
                st.success(f"✅ Job logged! Go to the **Job Board** to track it.")

# ════════════════════════════════════════════════════════════════
# PAGE 2 — JOB BOARD (Track all pending maintenance jobs)
# ════════════════════════════════════════════════════════════════
elif nav == "📋  Job Board":

    st.markdown('<div class="topbar"><h1>📋 Maintenance Job Board</h1><p>All open and completed maintenance jobs — log, track, and close work orders</p></div>', unsafe_allow_html=True)

    # Auto-populate from risk scores on first load
    if len(st.session_state.jobs) == 0:
        for _, row in risk_df[risk_df["risk_level"].isin(["Critical","High"])].iterrows():
            st.session_state.jobs.append({
                "id":         f"JOB-{len(st.session_state.jobs)+1:04d}",
                "machine":    row["machine_id"],
                "type":       row["machine_type"],
                "site":       row["site"],
                "priority":   "🔴 Emergency" if row["risk_level"] == "Critical" else "🟠 Urgent",
                "issue":      row["risk_level"],
                "notes":      f"Auto-flagged: risk score {row['fail_prob']*100:.0f}%",
                "due":        str(date.today() + timedelta(days=1)),
                "technician": "Unassigned",
                "logged_by":  "System",
                "logged_at":  datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status":     "Pending",
            })

    jobs = st.session_state.jobs

    pending   = [j for j in jobs if j["status"] == "Pending"]
    in_prog   = [j for j in jobs if j["status"] == "In Progress"]
    completed = [j for j in jobs if j["status"] == "Completed"]

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("red",    f"{len(pending)}",   "Pending Jobs",     "Waiting to be done"), unsafe_allow_html=True)
    c2.markdown(kcard("orange", f"{len(in_prog)}",   "In Progress",      "Being worked on now"), unsafe_allow_html=True)
    c3.markdown(kcard("green",  f"{len(completed)}", "Completed",        "Jobs done"), unsafe_allow_html=True)
    c4.markdown(kcard("blue",   f"{len(jobs)}",      "Total Jobs Logged","All time"), unsafe_allow_html=True)

    st.markdown("---")

    # ── Add new job manually ──────────────────────────────────────
    with st.expander("➕ Add a New Job Manually"):
        nc1,nc2,nc3 = st.columns(3)
        with nc1:
            nj_machine  = st.text_input("Machine ID")
            nj_type     = st.selectbox("Machine Type", MACHINE_TYPES, key="nj_type")
            nj_site     = st.selectbox("Site", SITES, key="nj_site")
        with nc2:
            nj_priority = st.selectbox("Priority", ["🔴 Emergency","🟠 Urgent","🟡 Scheduled","⚪ Routine"])
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
    st.markdown("### 🔴 Pending Jobs")
    if not pending:
        st.success("✅ No pending jobs right now!")
    else:
        for i, job in enumerate(jobs):
            if job["status"] != "Pending": continue
            j_idx = jobs.index(job)
            with st.container():
                jc1,jc2,jc3,jc4 = st.columns([3,2,2,1])
                with jc1:
                    st.markdown(f"**{job['id']}** · {job['machine']} ({job['type']}) · {job['site']}")
                    st.markdown(f"{job['priority']}  ·  Due: **{job['due']}**")
                    st.caption(job['notes'][:120])
                with jc2:
                    st.markdown(f"👷 {job['technician'] or 'Unassigned'}")
                    st.caption(f"Logged: {job['logged_at']}")
                with jc3:
                    new_status = st.selectbox("Update Status", ["Pending","In Progress","Completed"],
                                              key=f"status_{j_idx}")
                    if new_status != job["status"]:
                        st.session_state.jobs[j_idx]["status"] = new_status
                        st.rerun()
                with jc4:
                    if st.button("🗑️", key=f"del_{j_idx}"):
                        st.session_state.jobs.pop(j_idx); st.rerun()
                st.markdown("---")

    # ── In progress ───────────────────────────────────────────────
    if in_prog:
        st.markdown("### 🟠 In Progress")
        for job in in_prog:
            j_idx = jobs.index(job)
            jc1,jc2,jc3 = st.columns([4,2,2])
            with jc1:
                st.markdown(f"**{job['id']}** · {job['machine']} · {job['priority']}")
                st.caption(job['notes'][:120])
            with jc2:
                st.markdown(f"👷 {job['technician']}")
            with jc3:
                if st.button("✅ Mark Done", key=f"done_{j_idx}"):
                    st.session_state.jobs[j_idx]["status"] = "Completed"; st.rerun()

    # ── Completed ─────────────────────────────────────────────────
    if completed:
        with st.expander(f"✅ Completed Jobs ({len(completed)})"):
            for job in completed:
                st.markdown(f"✅ **{job['id']}** · {job['machine']} · {job['notes'][:80]}")

    # ── Export ────────────────────────────────────────────────────
    if jobs:
        csv = pd.DataFrame(jobs).to_csv(index=False).encode()
        st.download_button("📥 Export Job List as CSV", csv, "job_board.csv", "text/csv")

# ════════════════════════════════════════════════════════════════
# PAGE 3 — LOG A SERVICE (Record completed maintenance)
# ════════════════════════════════════════════════════════════════
elif nav == "🔧  Log a Service":

    st.markdown('<div class="topbar"><h1>🔧 Log a Completed Service</h1><p>Record every maintenance job done — keeps a full history of all work on the fleet</p></div>', unsafe_allow_html=True)

    st.markdown("### 📝 Service Record Form")
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
        if st.button("💾  Save Service Record"):
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
    st.markdown("### 📋 Service History Log")
    if st.session_state.services:
        sdf = pd.DataFrame(st.session_state.services)
        sdf["cost_bwp"] = sdf["cost_bwp"].apply(lambda x: f"P{x:,.0f}")
        sdf.columns     = ["Machine","Type","Site","Date","Technician",
                           "Work Done","Parts","Cost","Hrs Worked","Notes","Logged"]
        st.dataframe(sdf, use_container_width=True)
        csv = pd.DataFrame(st.session_state.services).to_csv(index=False).encode()
        st.download_button("📥 Export Service Records", csv, "service_history.csv", "text/csv")
    else:
        st.info("No service records logged yet. Use the form above to log completed work.")

# ════════════════════════════════════════════════════════════════
# PAGE 4 — FLEET HEALTH (Simple summary of all 80 machines)
# ════════════════════════════════════════════════════════════════
elif nav == "📊  Fleet Health":

    st.markdown('<div class="topbar"><h1>📊 Fleet Health Summary</h1><p>Current health status of all 80 machines based on latest sensor readings</p></div>', unsafe_allow_html=True)

    rc = risk_df["risk_level"].value_counts()
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("red",    f"{rc.get('Critical',0)}",  "Need Immediate Action", "Critical risk"), unsafe_allow_html=True)
    c2.markdown(kcard("orange", f"{rc.get('High',0)}",      "Service Within 48 Hrs", "High risk"), unsafe_allow_html=True)
    c3.markdown(kcard("blue",   f"{rc.get('Medium',0)}",    "Service This Week",     "Medium risk"), unsafe_allow_html=True)
    c4.markdown(kcard("green",  f"{rc.get('Low',0)}",       "Healthy — No Action",   "Good condition"), unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("#### All 80 Machines — Sorted by Risk")
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
            return {"Critical":"background-color:#450a0a;color:#fca5a5;font-weight:bold",
                    "High":    "background-color:#431407;color:#fed7aa;font-weight:bold",
                    "Medium":  "background-color:#422006;color:#fde68a",
                    "Low":     "background-color:#052e16;color:#86efac"}.get(val,"")

        display.columns = ["Machine","Type","Site","Status","Days Since Service","Temp","Vibration"]
        st.dataframe(display.style.applymap(row_color, subset=["Status"]),
                     use_container_width=True, height=500)

    with col2:
        st.markdown("#### Fleet Condition Breakdown")
        fig = px.pie(names=rc.index, values=rc.values, hole=0.5,
                     color=rc.index,
                     color_discrete_map={"Critical":"#ef4444","High":"#f97316",
                                         "Medium":"#f59e0b","Low":"#22c55e"})
        fig.update_layout(paper_bgcolor="#0f172a",plot_bgcolor="#0f172a",
                          font_color="#e2e8f0",height=280,margin=dict(t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Machines Most Overdue for Service")
        overdue = risk_df[risk_df["days_since_maintenance"] > 150].sort_values(
            "days_since_maintenance", ascending=False).head(8)
        if len(overdue):
            for _, r in overdue.iterrows():
                st.markdown(f"`{r['machine_id']}` — **{r['days_since_maintenance']:.0f} days** since service", unsafe_allow_html=True)
        else:
            st.success("All machines up to date!")

# ════════════════════════════════════════════════════════════════
# PAGE 5 — MACHINE RECORDS (Full sensor history for one machine)
# ════════════════════════════════════════════════════════════════
elif nav == "📁  Machine Records":

    st.markdown('<div class="topbar"><h1>📁 Machine Records</h1><p>Full sensor history for any machine — see trends over time</p></div>', unsafe_allow_html=True)

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
                      "⚠️ Overdue!" if last["days_since_maintenance"]>150 else "✅ Up to date"), unsafe_allow_html=True)

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
        fig.update_layout(plot_bgcolor="#0f172a",paper_bgcolor="#1e293b",
                          font_color="#e2e8f0",height=260,
                          margin=dict(t=10,b=10,l=5,r=5),showlegend=False)
        return fig

    with col1:
        st.markdown("**🌡️ Engine Temperature Over Time**")
        st.plotly_chart(line_chart(mdata["date"], mdata["engine_temp_c"], "#f87171",
                                   warning_val=90, warning_label="Warning (90°C)",
                                   crit_val=105), use_container_width=True)

        st.markdown("**🛢️ Oil Pressure Over Time**")
        st.plotly_chart(line_chart(mdata["date"], mdata["oil_pressure_psi"], "#34d399",
                                   warning_val=60, warning_label="Min safe (60 PSI)"),
                        use_container_width=True)

    with col2:
        st.markdown("**📳 Vibration Level Over Time**")
        st.plotly_chart(line_chart(mdata["date"], mdata["vibration"], "#fb923c",
                                   warning_val=4.0, warning_label="Warning (4.0)",
                                   crit_val=5.0), use_container_width=True)

        st.markdown("**⛽ Daily Fuel Cost**")
        fig_fuel = go.Figure()
        fig_fuel.add_trace(go.Bar(x=mdata["date"], y=mdata["fuel_cost_bwp"],
                                  marker_color="#60a5fa"))
        fig_fuel.update_layout(plot_bgcolor="#0f172a",paper_bgcolor="#1e293b",
                                font_color="#e2e8f0",height=260,
                                margin=dict(t=10,b=10,l=5,r=5),showlegend=False)
        st.plotly_chart(fig_fuel, use_container_width=True)

    # Breakdown history
    bds = mdata[mdata["breakdown"] == 1]
    st.markdown("---")
    if len(bds):
        st.markdown(f"### ⚠️ Breakdown History — {len(bds)} incident(s) on record")
        show = bds[["date","shift","operator_id","engine_temp_c","vibration","repair_cost_bwp"]].copy()
        show["repair_cost_bwp"] = show["repair_cost_bwp"].apply(lambda x: f"P{x:,.0f}")
        show.columns = ["Date","Shift","Operator","Temp at Breakdown","Vibration","Repair Cost"]
        st.dataframe(show.reset_index(drop=True), use_container_width=True)
    else:
        st.success(f"✅ No breakdowns on record for {machine_id}")

    # Service records for this machine
    if st.session_state.services:
        mach_services = [s for s in st.session_state.services if s["machine_id"] == machine_id]
        if mach_services:
            st.markdown(f"### 🔧 Service Records — {len(mach_services)} logged")
            st.dataframe(pd.DataFrame(mach_services), use_container_width=True)

# ── FOOTER ────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<div style='text-align:center;color:#475569;font-size:.78rem'>Kgosi Mining Solutions · Maintenance Management System · Unaswi Leonard · 2026</div>", unsafe_allow_html=True)