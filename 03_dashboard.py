"""
KGOSI MINING SOLUTIONS — OPERATIONS DASHBOARD
Simple, clear report for management staff. No technical jargon.
Run: streamlit run 03_dashboard.py --server.port 8501
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Kgosi Mining | Dashboard", page_icon="⛏️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#f5f6fa;color:#1a1a2e;}
.topbar{background:linear-gradient(135deg,#1a1a2e,#16213e);color:white;padding:1.4rem 2rem;border-radius:12px;margin-bottom:1.5rem;}
.topbar h1{margin:0;font-size:1.5rem;font-weight:700;}
.topbar p{margin:.3rem 0 0 0;opacity:.6;font-size:.85rem;}
.kcard{background:white;border-radius:12px;padding:1.2rem 1.4rem;box-shadow:0 2px 8px rgba(0,0,0,.07);border-left:5px solid #e0e0e0;}
.kcard.red{border-left-color:#e74c3c;} .kcard.orange{border-left-color:#e67e22;}
.kcard.green{border-left-color:#27ae60;} .kcard.blue{border-left-color:#2980b9;}
.kval{font-size:1.9rem;font-weight:700;line-height:1.1;}
.klbl{font-size:.72rem;text-transform:uppercase;letter-spacing:1.5px;color:#888;margin-top:.3rem;}
.ksub{font-size:.78rem;color:#666;margin-top:.3rem;}
.ccard{background:white;border-radius:12px;padding:1.2rem 1.4rem;box-shadow:0 2px 8px rgba(0,0,0,.07);margin-bottom:1rem;}
.ctitle{font-size:.95rem;font-weight:600;color:#1a1a2e;margin-bottom:.2rem;}
.csub{font-size:.78rem;color:#888;margin-bottom:.7rem;}
.ar{background:#fdf2f2;border:1px solid #f5c6cb;border-radius:8px;padding:.9rem;margin-bottom:.5rem;}
.ao{background:#fff8f0;border:1px solid #fcd5a5;border-radius:8px;padding:.9rem;margin-bottom:.5rem;}
.ag{background:#f0faf4;border:1px solid #b7dfca;border-radius:8px;padding:.9rem;margin-bottom:.5rem;}
section[data-testid="stSidebar"]{background:#1a1a2e!important;}
section[data-testid="stSidebar"] *{color:white!important;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load():
    df   = pd.read_csv("equipment_data.csv", parse_dates=["date"])
    risk = pd.read_csv("risk_scores.csv")
    return df, risk

df, risk = load()

with st.sidebar:
    st.markdown("### ⛏️ Kgosi Mining")
    st.markdown("Operations Dashboard")
    st.markdown("---")
    page = st.radio("Go to", [
        "📋  Overview",
        "💸  Costs & Repairs",
        "⛽  Fuel Usage",
        "⚠️  Safety Alerts",
        "👷  Staff Report",
    ])
    st.markdown("---")
    sel_t = st.selectbox("Filter: Machine Type", ["All Types"] + sorted(df["machine_type"].unique().tolist()))
    sel_s = st.selectbox("Filter: Site",         ["All Sites"] + sorted(df["site"].unique().tolist()))
    st.markdown("---")
    st.caption("Period: Jul – Dec 2025")

dff = df.copy()
if sel_t != "All Types": dff = dff[dff["machine_type"] == sel_t]
if sel_s != "All Sites":  dff = dff[dff["site"] == sel_s]

def kcard(color, val, lbl, sub=""):
    return f'<div class="kcard {color}"><div class="kval">{val}</div><div class="klbl">{lbl}</div>{"<div class=ksub>"+sub+"</div>" if sub else ""}</div>'

def wchart(fig, h=340):
    fig.update_layout(plot_bgcolor="white",paper_bgcolor="white",font_color="#1a1a2e",
                      height=h,margin=dict(t=15,b=20,l=10,r=10))
    return fig

# ─── PAGE 1: OVERVIEW ────────────────────────────────────────────
if page == "📋  Overview":
    st.markdown('<div class="topbar"><h1>⛏️ Operations Overview</h1><p>Kgosi Mining Solutions &nbsp;·&nbsp; July – December 2025</p></div>', unsafe_allow_html=True)

    bd = dff[dff["breakdown"]==1]
    idle_waste = dff["idle_hours"].sum()*35*14.5*0.35
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.markdown(kcard("red",    f"P{dff['repair_cost_bwp'].sum()/1e6:.1f}M", "Spent on Repairs",      "Jul–Dec 2025"), unsafe_allow_html=True)
    c2.markdown(kcard("orange", f"P{dff['fuel_cost_bwp'].sum()/1e6:.1f}M",   "Total Fuel Costs",      "Jul–Dec 2025"), unsafe_allow_html=True)
    c3.markdown(kcard("red",    f"P{idle_waste/1e3:.0f}K",                    "Fuel Wasted on Idle",   "Zero production benefit"), unsafe_allow_html=True)
    c4.markdown(kcard("red",    f"{dff['breakdown'].sum()}",                   "Breakdowns",            f"Avg P{bd['repair_cost_bwp'].mean():,.0f} each" if len(bd) else ""), unsafe_allow_html=True)
    c5.markdown(kcard("green",  f"{(risk['risk_level']=='Low').sum()} / 80",  "Machines Healthy",      f"{(risk['risk_level']!='Low').sum()} need attention"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔍 What This Report Found")
    f1,f2,f3 = st.columns(3)
    with f1:
        st.markdown('<div class="ar"><b>🔴 Breakdowns Are Too Expensive</b><br><br>Every unplanned breakdown costs <b>P450,000–P600,000</b>. If we service machines on time, the same job costs only <b>P80,000</b>. We are paying 6× more than necessary.</div>', unsafe_allow_html=True)
    with f2:
        st.markdown('<div class="ao"><b>🟠 Fuel Is Being Wasted Every Day</b><br><br>Machines are being left running while not working. A small number of operators are responsible for most of this waste. This money goes nowhere.</div>', unsafe_allow_html=True)
    with f3:
        st.markdown('<div class="ao"><b>🟠 Machines Running Past Safe Limits</b><br><br>Several machines have been recorded at temperatures and vibration levels above safe thresholds. This is a safety risk and leads directly to expensive breakdowns.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="ccard"><div class="ctitle">📅 Monthly Repair Costs vs Fuel Costs</div><div class="csub">See which months had the most incidents</div>', unsafe_allow_html=True)
    mo = dff.groupby(dff["date"].dt.to_period("M")).agg(Repairs=("repair_cost_bwp","sum"),Fuel=("fuel_cost_bwp","sum")).reset_index()
    mo["Month"] = mo["date"].astype(str)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Repair Costs",x=mo["Month"],y=mo["Repairs"],marker_color="#e74c3c",text=mo["Repairs"].apply(lambda x:f"P{x/1e3:.0f}K"),textposition="outside"))
    fig.add_trace(go.Bar(name="Fuel Costs",  x=mo["Month"],y=mo["Fuel"],   marker_color="#f39c12",text=mo["Fuel"].apply(lambda x:f"P{x/1e6:.1f}M"),  textposition="outside"))
    fig.update_layout(barmode="group",xaxis_title="Month",yaxis_title="Cost (BWP)",legend=dict(orientation="h",y=1.1))
    st.plotly_chart(wchart(fig,380), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── PAGE 2: COSTS ────────────────────────────────────────────────
elif page == "💸  Costs & Repairs":
    st.markdown('<div class="topbar"><h1>💸 Repair Costs & Breakdown Report</h1><p>Which machines are breaking and what it is costing the company</p></div>', unsafe_allow_html=True)
    bd = dff[dff["breakdown"]==1]
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("red",    f"{len(bd)}",                            "Total Breakdowns",    "Past 6 months"), unsafe_allow_html=True)
    c2.markdown(kcard("red",    f"P{bd['repair_cost_bwp'].sum():,.0f}",  "Total Repair Bill",   "Jul–Dec 2025"), unsafe_allow_html=True)
    c3.markdown(kcard("orange", f"P{bd['repair_cost_bwp'].mean():,.0f}", "Average Per Breakdown","Per incident"), unsafe_allow_html=True)
    c4.markdown(kcard("blue",   "P80,000",                               "Cost if Planned",     "6× cheaper than emergency"), unsafe_allow_html=True)
    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">Which Machines Break the Most?</div><div class="csub">Haul Trucks and Excavators cause the highest repair bills</div>', unsafe_allow_html=True)
        bt = dff.groupby("machine_type").agg(Breakdowns=("breakdown","sum"),Cost=("repair_cost_bwp","sum")).sort_values("Cost",ascending=True).reset_index()
        bt["Label"] = bt["Cost"].apply(lambda x:f"P{x/1e3:.0f}K")
        fig = px.bar(bt,x="Cost",y="machine_type",orientation="h",color="Breakdowns",
                     color_continuous_scale=["#ffd6d6","#e74c3c"],text="Label",labels={"Cost":"Total Repair Cost","machine_type":""})
        fig.update_traces(textposition="outside")
        st.plotly_chart(wchart(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="ccard"><div class="ctitle">Machine Readings: Healthy vs Just Before a Breakdown</div><div class="csub">Every breakdown was preceded by clear warning signs that went unnoticed</div>', unsafe_allow_html=True)
        cdf = pd.DataFrame({
            "Reading": ["Engine Temperature","Shaking (Vibration)","Oil Dirt Level"],
            "Normal Machine": [78, 2.6, 1.6],
            "Just Before Breakdown": [122, 5.6, 5.3],
        })
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Normal Machine",        x=cdf["Reading"],y=cdf["Normal Machine"],       marker_color="#27ae60"))
        fig2.add_trace(go.Bar(name="Just Before Breakdown", x=cdf["Reading"],y=cdf["Just Before Breakdown"],marker_color="#e74c3c"))
        fig2.update_layout(barmode="group",legend=dict(orientation="h",y=1.1))
        st.plotly_chart(wchart(fig2), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📋 Every Breakdown — Full List")
    show = bd[["date","machine_id","machine_type","site","repair_cost_bwp","days_since_maintenance","operator_id"]].copy()
    show["date"]=""+show["date"].astype(str)
    show["repair_cost_bwp"]=show["repair_cost_bwp"].apply(lambda x:f"P{x:,.0f}")
    show["days_since_maintenance"]=show["days_since_maintenance"].apply(lambda x:f"{x} days")
    show.columns=["Date","Machine","Type","Site","Repair Cost","Days Since Last Service","Operator"]
    st.dataframe(show.sort_values("Date",ascending=False).reset_index(drop=True),use_container_width=True)
    st.markdown('<div class="ar"><b>💡 Key Takeaway:</b> Every machine that broke down had warning signs days beforehand. These breakdowns were preventable. Planned servicing costs <b>P80,000</b>. Emergency repairs cost <b>P450,000–P600,000</b>.</div>', unsafe_allow_html=True)

# ─── PAGE 3: FUEL ────────────────────────────────────────────────
elif page == "⛽  Fuel Usage":
    st.markdown('<div class="topbar"><h1>⛽ Fuel Usage & Waste Report</h1><p>How much fuel is being used — and how much is being wasted</p></div>', unsafe_allow_html=True)
    idle_waste = dff["idle_hours"].sum()*35*14.5*0.35
    idle_pct   = dff["idle_hours"].sum()/dff["hours_today"].sum()*100
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("blue",   f"P{dff['fuel_cost_bwp'].sum()/1e6:.2f}M","Total Fuel Spend",          "Jul–Dec 2025"), unsafe_allow_html=True)
    c2.markdown(kcard("red",    f"P{idle_waste:,.0f}",                     "Wasted on Idle Machines",   "Zero production"), unsafe_allow_html=True)
    c3.markdown(kcard("orange", f"{idle_pct:.1f}%",                        "Of Machine Time Was Idle",  "Machines on, doing nothing"), unsafe_allow_html=True)
    c4.markdown(kcard("orange", f"{dff['idle_hours'].sum():,.0f} hrs",     "Total Idle Hours",          "Across full fleet"), unsafe_allow_html=True)
    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">Fuel Spend by Machine Type</div><div class="csub">Haul Trucks use the most — even small idle reductions on them save a lot</div>', unsafe_allow_html=True)
        fc = dff.groupby("machine_type")["fuel_cost_bwp"].sum().sort_values(ascending=False).reset_index()
        fc["Label"] = fc["fuel_cost_bwp"].apply(lambda x:f"P{x/1e6:.2f}M")
        fig = px.bar(fc,x="machine_type",y="fuel_cost_bwp",color="fuel_cost_bwp",
                     color_continuous_scale=["#ffd6a0","#e67e22"],text="Label",
                     labels={"fuel_cost_bwp":"Fuel Cost","machine_type":""})
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)
        st.plotly_chart(wchart(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="ccard"><div class="ctitle">Working Time vs Idle Time by Site</div><div class="csub">Red portions = machines running but not producing anything</div>', unsafe_allow_html=True)
        sh = dff.groupby("site").agg(Working=("active_hours","sum"),Idle=("idle_hours","sum")).reset_index()
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Working",x=sh["site"],y=sh["Working"],marker_color="#27ae60"))
        fig2.add_trace(go.Bar(name="Idle",   x=sh["site"],y=sh["Idle"],   marker_color="#e74c3c"))
        fig2.update_layout(barmode="stack",legend=dict(orientation="h",y=1.1))
        st.plotly_chart(wchart(fig2), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 👷 Which Operators Leave Machines Running?")
    st.caption("Ranked by total idle hours — these operators are responsible for the most wasted fuel")
    op = dff.groupby("operator_id").agg(idle_hrs=("idle_hours","sum"),shifts=("record_id","count")).reset_index()
    op["Fuel Wasted"]=( op["idle_hrs"]*35*14.5*0.35).round(0)
    op = op.sort_values("idle_hrs",ascending=False)
    top15 = op.head(15)
    fig3 = px.bar(top15,x="operator_id",y="idle_hrs",color="Fuel Wasted",
                  color_continuous_scale=["#fcd5a5","#c0392b"],
                  text=top15["Fuel Wasted"].apply(lambda x:f"P{x:,.0f}"),
                  labels={"idle_hrs":"Total Idle Hrs","operator_id":"Operator"})
    fig3.update_traces(textposition="outside"); fig3.update_layout(showlegend=False)
    st.plotly_chart(wchart(fig3,360), use_container_width=True)
    op_s = op.head(10).copy()
    op_s["Fuel Wasted"]=op_s["Fuel Wasted"].apply(lambda x:f"P{x:,.0f}")
    op_s.columns=["Operator","Total Idle Hrs","Shifts","Fuel Wasted"]
    st.dataframe(op_s.reset_index(drop=True), use_container_width=True)
    st.markdown('<div class="ao"><b>💡 Action Needed:</b> The top 5 operators account for the majority of idle hours. A policy enforcing machine switch-off when idle for more than 10 minutes would recover most of this cost.</div>', unsafe_allow_html=True)

# ─── PAGE 4: SAFETY ───────────────────────────────────────────────
elif page == "⚠️  Safety Alerts":
    st.markdown('<div class="topbar"><h1>⚠️ Machine Safety Status</h1><p>Machines recorded operating outside safe limits</p></div>', unsafe_allow_html=True)
    rc = dff["safety_risk"].value_counts()
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("red",    f"{rc.get('Critical',0):,}","Critical Alerts",   "Must stop immediately"), unsafe_allow_html=True)
    c2.markdown(kcard("orange", f"{rc.get('High',0):,}",    "High Risk",         "Service within 48 hours"), unsafe_allow_html=True)
    c3.markdown(kcard("blue",   f"{rc.get('Medium',0):,}",  "Worth Monitoring",  "Keep an eye on these"), unsafe_allow_html=True)
    c4.markdown(kcard("green",  f"{rc.get('Low',0):,}",     "Operating Safely",  "No action needed"), unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📏 What Do the Alert Levels Mean?")
    e1,e2,e3 = st.columns(3)
    with e1: st.markdown('<div class="ar"><b>🔴 CRITICAL</b><br>Temperature above 115°C or severe shaking. <b>Stop this machine now.</b> Running it risks injury and a major breakdown.</div>', unsafe_allow_html=True)
    with e2: st.markdown('<div class="ao"><b>🟠 HIGH RISK</b><br>Temperature above 105°C or high shaking. <b>Book it for service within 48 hours.</b> It will deteriorate fast if ignored.</div>', unsafe_allow_html=True)
    with e3: st.markdown('<div class="ag"><b>🟢 SAFE</b><br>All readings within normal range. <b>Continue normal operations.</b> Check again at next scheduled inspection.</div>', unsafe_allow_html=True)
    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">Safety Incidents Per Week</div><div class="csub">Number of shifts where a machine was in Critical or High Risk condition</div>', unsafe_allow_html=True)
        wk = dff[dff["safety_risk"].isin(["Critical","High"])].copy()
        wk["week"] = wk["date"].dt.to_period("W").astype(str)
        wk_c = wk.groupby("week").size().reset_index(name="Incidents")
        fig = px.area(wk_c,x="week",y="Incidents",color_discrete_sequence=["#e74c3c"])
        fig.update_traces(fill="tozeroy",fillcolor="rgba(231,76,60,.15)")
        st.plotly_chart(wchart(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="ccard"><div class="ctitle">Safety Incidents by Site</div><div class="csub">Which locations have the most machines running outside safe limits</div>', unsafe_allow_html=True)
        sr = dff[dff["safety_risk"].isin(["Critical","High"])].groupby(["site","safety_risk"]).size().reset_index(name="Count")
        fig2 = px.bar(sr,x="site",y="Count",color="safety_risk",barmode="stack",
                      color_discrete_map={"Critical":"#e74c3c","High":"#e67e22"},
                      labels={"site":"Site","Count":"Incidents","safety_risk":"Risk Level"})
        fig2.update_layout(legend=dict(orientation="h",y=1.1))
        st.plotly_chart(wchart(fig2), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🔴 Machines Needing Immediate Attention")
    latest_all = dff.sort_values("date").groupby("machine_id").last().reset_index()
    danger = latest_all[latest_all["safety_risk"].isin(["Critical","High"])].copy()
    if len(danger)==0:
        st.success("✅ No machines currently in Critical or High state.")
    else:
        danger["Action"] = danger["safety_risk"].map({"Critical":"⛔ Stop & inspect NOW","High":"⚠️ Service within 48 hrs"})
        danger["engine_temp_c"] = danger["engine_temp_c"].apply(lambda x:f"{x:.1f}°C")
        danger["vibration"]     = danger["vibration"].apply(lambda x:f"{x:.2f}")
        show = danger[["machine_id","machine_type","site","engine_temp_c","vibration","safety_risk","Action"]].copy()
        show.columns=["Machine","Type","Site","Engine Temp","Vibration","Risk","Action Required"]
        st.dataframe(show.reset_index(drop=True),use_container_width=True)

# ─── PAGE 5: STAFF ────────────────────────────────────────────────
elif page == "👷  Staff Report":
    st.markdown('<div class="topbar"><h1>👷 Staff & Operator Performance</h1><p>How operators are handling company equipment</p></div>', unsafe_allow_html=True)
    op = dff.groupby("operator_id").agg(shifts=("record_id","count"),idle_hrs=("idle_hours","sum"),breakdowns=("breakdown","sum"),avg_temp=("engine_temp_c","mean")).reset_index()
    op["fuel_wasted"]=(op["idle_hrs"]*35*14.5*0.35).round(0)
    worst = op.sort_values("idle_hrs",ascending=False).iloc[0]
    c1,c2,c3 = st.columns(3)
    c1.markdown(kcard("blue",  f"{len(op)}",                 "Total Operators",       "Active Jul–Dec 2025"), unsafe_allow_html=True)
    c2.markdown(kcard("red",   worst["operator_id"],          "Most Idle Hours",        f"{worst['idle_hrs']:.0f} hrs total"), unsafe_allow_html=True)
    c3.markdown(kcard("red",   f"P{op['fuel_wasted'].sum():,.0f}","Fuel Wasted by Staff","Across all operators"), unsafe_allow_html=True)
    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">Operators with the Most Idle Time</div><div class="csub">These operators leave machines running when not in use — each idle hour costs money</div>', unsafe_allow_html=True)
        top = op.sort_values("idle_hrs",ascending=False).head(15)
        fig = px.bar(top,x="operator_id",y="idle_hrs",color="fuel_wasted",
                     color_continuous_scale=["#ffe5b4","#c0392b"],
                     text=top["fuel_wasted"].apply(lambda x:f"P{x:,.0f}"),
                     labels={"idle_hrs":"Total Idle Hrs","operator_id":"Operator"})
        fig.update_traces(textposition="outside"); fig.update_layout(showlegend=False)
        st.plotly_chart(wchart(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="ccard"><div class="ctitle">Breakdowns Recorded During Each Operator\'s Shift</div><div class="csub">Not always the operator\'s fault — but patterns help identify training needs</div>', unsafe_allow_html=True)
        bd_op = op[op["breakdowns"]>0].sort_values("breakdowns",ascending=False)
        if len(bd_op)==0: st.info("No breakdown data for selected filter.")
        else:
            fig2 = px.bar(bd_op,x="operator_id",y="breakdowns",color="breakdowns",
                          color_continuous_scale=["#ffd6d6","#e74c3c"],text="breakdowns",
                          labels={"breakdowns":"Breakdowns","operator_id":"Operator"})
            fig2.update_traces(textposition="outside"); fig2.update_layout(showlegend=False)
            st.plotly_chart(wchart(fig2), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📋 Full Operator Summary Table")
    op_s = op.sort_values("idle_hrs",ascending=False).reset_index(drop=True); op_s.index+=1
    op_s["fuel_wasted"]=op_s["fuel_wasted"].apply(lambda x:f"P{x:,.0f}")
    op_s["avg_temp"]=op_s["avg_temp"].apply(lambda x:f"{x:.1f}°C")
    op_s.columns=["Operator","Shifts","Idle Hrs","Breakdowns on Shift","Avg Engine Temp","Fuel Wasted"]
    st.dataframe(op_s, use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align:center;color:#aaa;font-size:.78rem'>Kgosi Mining Solutions · Operations Dashboard · Prepared by Data Analytics Team · 2026</div>", unsafe_allow_html=True)