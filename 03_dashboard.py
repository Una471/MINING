
PAGE_TITLE="Kgosi Mining | Operations"
ACCENT="#176b4a"; ACCENT_DARK="#0d4b35"; ACCENT2="#c78d4a"; SOFT="#e9f3ee"
OVERVIEW_URL="https://una471.github.io/portfolio/projects/mining/overview.html"; OVERVIEW_LABEL="Overview"; SOFTWARE_URL="https://machinery-system.streamlit.app/?view=software"; 
HERO_IMAGE="mining-hero.webp"; SEARCH_TEXT="Search machines, operators, sites or reports..."

import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import base64

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title=PAGE_TITLE, page_icon=None, layout="wide", initial_sidebar_state="expanded")

def _img_data(name):
    p = ROOT / "assets" / name
    if not p.exists():
        return ""
    mime = "image/webp" if p.suffix.lower()==".webp" else "image/png"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()

HERO = _img_data(HERO_IMAGE)

STYLE = f"""
<style>
:root{{--bg:#e7e8ea;--shell:#f7f7f6;--panel:#fff;--line:#e7e7e5;--ink:#2d2e30;--muted:#85888d;--accent:{ACCENT};--accent2:{ACCENT2};--soft:{SOFT};--danger:#d75555;--warn:#c88a32;--good:#16865c;}}
html,body,[class*="css"],.stApp{{font-family:"Segoe UI Variable","Segoe UI",Arial,sans-serif!important;color:var(--ink)!important}}
.stApp{{background:var(--bg)!important}}
header[data-testid="stHeader"]{{display:none!important}} #MainMenu,footer,[data-testid="stToolbar"]{{display:none!important}}
.block-container{{max-width:1480px!important;margin:18px auto!important;padding:14px 18px 24px!important;background:var(--shell)!important;border:1px solid #d9d9da!important;border-radius:22px!important;box-shadow:0 2px 10px rgba(40,40,45,.06)!important}}
section[data-testid="stSidebar"]{{width:248px!important;background:#f5f5f4!important;border-right:1px solid #dededc!important}}
section[data-testid="stSidebar"]>div{{padding:26px 16px 18px!important}}
section[data-testid="stSidebar"] h2{{font-size:1.02rem!important;margin:.2rem 8px .1rem!important;letter-spacing:-.02em!important}}
section[data-testid="stSidebar"] .stCaption,section[data-testid="stSidebar"] p{{font-size:.71rem!important;color:#85888b!important}}
section[data-testid="stSidebar"] hr{{border:0!important;border-top:1px solid #ddd!important;margin:1rem 8px!important}}
section[data-testid="stSidebar"] div[role="radiogroup"]{{gap:.05rem!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label{{min-height:38px!important;padding:.56rem .78rem!important;border-radius:8px!important;margin:0!important;background:transparent!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label>div:first-child{{display:none!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label p{{font-size:.76rem!important;color:#74777a!important;font-weight:500!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){{background:var(--soft)!important;box-shadow:inset 3px 0 0 var(--accent)!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{{color:#252726!important;font-weight:700!important}}
section[data-testid="stSidebar"] [data-baseweb="select"]>div{{min-height:39px!important;background:#fff!important;border:1px solid #dededc!important;border-radius:9px!important}}
section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p{{font-size:.68rem!important;color:#85888b!important;font-weight:500!important}}
.utilitybar{{height:58px;display:flex;align-items:center;gap:12px;background:#f0f0ef;border:1px solid #ededeb;border-radius:14px;padding:8px 12px;margin:0 0 10px}}
.searchbox{{width:min(340px,42vw);height:38px;background:#fff;border:1px solid #ececea;border-radius:20px;color:#999b9d;font-size:.72rem;display:flex;align-items:center;padding:0 14px}}
.searchbox:before{{content:'⌕';font-size:1.03rem;color:#717476;margin-right:8px}} .utility-spacer{{flex:1}} .utility-icon{{width:36px;height:36px;background:#fff;border:1px solid #ececea;border-radius:50%;display:grid;place-items:center;color:#6e7270;font-size:.72rem}} .user-chip{{display:flex;align-items:center;gap:8px}} .avatar{{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:var(--accent);color:#fff;font-size:.66rem;font-weight:700}} .user-name{{font-size:.72rem;font-weight:700;color:#2f3130}} .user-role{{font-size:.61rem;color:#949695;margin-top:3px}}
.hero{{position:relative;min-height:110px;overflow:hidden;border:1px solid var(--line);border-radius:14px;background:#fff;margin-bottom:10px;padding:18px 20px}} .hero:after{{content:'';position:absolute;inset:0 0 0 52%;background-image:linear-gradient(90deg,rgba(255,255,255,.98),rgba(255,255,255,.35)),url('{HERO}');background-size:cover;background-position:center;opacity:.42}} .hero>*{{position:relative;z-index:1}} .hero h1{{font-size:1.48rem!important;line-height:1.05!important;letter-spacing:-.035em!important;margin:0!important;color:#2c2e2f!important}} .hero p{{font-size:.74rem!important;color:#85888b!important;margin:.45rem 0 0!important;max-width:670px;line-height:1.35}}
.section-title{{font-size:.82rem;font-weight:700;color:#343637;margin:.2rem 0 .6rem}} .kcard{{height:112px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:.9rem .9rem .75rem;display:flex;flex-direction:column}} .kcard.primary{{background:linear-gradient(145deg,{ACCENT_DARK},{ACCENT});border-color:{ACCENT};}} .klabel{{font-size:.68rem;font-weight:700;color:#3d3f40;line-height:1.15;min-height:26px}} .kcard.primary .klabel{{color:#e8f6f0}} .kvalue{{font-size:1.72rem;font-weight:700;letter-spacing:-.045em;line-height:1;margin-top:.35rem;color:#292b2c;white-space:nowrap}} .kcard.primary .kvalue{{color:#fff}} .ksub{{font-size:.62rem;color:#16865c;margin-top:auto;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}} .kcard.primary .ksub{{color:#d8f5e8}}
.panel-title{{font-size:.79rem;font-weight:700;color:#343637;margin:0 0 .1rem}} .panel-sub{{font-size:.63rem;color:#949698;margin:0 0 .35rem}}
[data-testid="stPlotlyChart"]{{background:#fff!important;border:1px solid var(--line)!important;border-radius:14px!important;padding:.35rem .45rem .2rem!important;box-shadow:none!important}}
[data-testid="stDataFrame"],[data-testid="stTable"]{{border:1px solid var(--line)!important;border-radius:12px!important;overflow:hidden!important;background:#fff!important}}
div[data-testid="stVerticalBlock"]{{gap:.58rem!important}} div[data-testid="stHorizontalBlock"]{{gap:.65rem!important}}
.stButton>button{{height:34px!important;border-radius:18px!important;border:1px solid var(--accent)!important;background:#fff!important;color:var(--accent)!important;font-size:.69rem!important;font-weight:650!important}}
.side-promo{{height:160px;margin:1rem .1rem 0;border-radius:13px;padding:1rem;display:flex;align-items:flex-end;background:linear-gradient(180deg,rgba(15,25,20,.1),rgba(15,25,20,.72)),url('{HERO}');background-size:cover;background-position:center;color:#fff}} .side-promo strong{{display:block;font-size:.9rem;line-height:1.14;margin-bottom:.4rem;color:#fff}} .side-promo span{{font-size:.63rem;color:#e5eee9;line-height:1.3}}
.small-note{{font-size:.64rem;color:#8f9294}} .status-pill{{display:inline-block;padding:.16rem .48rem;border-radius:999px;background:#edf6f1;color:#1a7655;font-size:.62rem;font-weight:700}}
@media(max-width:1000px){{.block-container{{margin:0!important;border-radius:0!important;padding:10px!important}}section[data-testid="stSidebar"]{{width:232px!important}}.hero:after{{display:none}}.kvalue{{font-size:1.45rem}}}}
.sidebar-brand{{display:flex;align-items:center;gap:10px;margin:0 4px 18px;padding:0 4px 17px;border-bottom:1px solid #d9d9d7}}
.sidebar-brand>span{{display:grid;width:36px;height:36px;place-items:center;border-radius:7px;background:var(--accent);color:#fff;font-size:.66rem;font-weight:800;letter-spacing:.02em}}
.sidebar-brand strong{{display:block;color:var(--ink);font-size:.88rem;line-height:1.15}}
.sidebar-brand small{{display:block;margin-top:3px;color:var(--muted);font-size:.61rem}}
div[data-testid="stTextInput"]{{max-width:520px}}
div[data-testid="stTextInput"] input{{height:38px!important;border:1px solid #ececea!important;border-radius:20px!important;background:#fff!important;color:var(--ink)!important;font-size:.72rem!important}}
div[data-testid="stTextInput"] input:focus{{border-color:var(--accent)!important;box-shadow:0 0 0 2px color-mix(in srgb,var(--accent) 18%,transparent)!important}}
.profile-chip{{height:40px;display:flex;align-items:center;justify-content:flex-end;gap:8px;padding-right:4px}}
.profile-chip>span{{display:grid;width:31px;height:31px;place-items:center;border-radius:50%;background:var(--accent);color:#fff;font-size:.61rem;font-weight:800}}
.profile-chip strong{{display:block;font-size:.65rem;color:var(--ink)}}
.profile-chip small{{display:block;margin-top:2px;font-size:.57rem;color:var(--muted)}}
/* Cohesive project-specific dashboard finish */
.stApp{{background:color-mix(in srgb,var(--soft) 46%,#dfe3e5)!important}}
.block-container{{background:color-mix(in srgb,var(--soft) 28%,#f7f7f6)!important;border-color:color-mix(in srgb,var(--accent) 12%,#d9d9da)!important}}
section[data-testid="stSidebar"]{{background:color-mix(in srgb,var(--soft) 72%,#f4f4f2)!important;border-right-color:color-mix(in srgb,var(--accent) 14%,#d8d8d6)!important}}
section[data-testid="stSidebar"] [data-baseweb="select"]>div{{background:color-mix(in srgb,var(--soft) 35%,#fff)!important;border-color:color-mix(in srgb,var(--accent) 18%,#d7d7d5)!important;color:var(--ink)!important}}
section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p{{color:color-mix(in srgb,var(--ink) 70%,var(--muted))!important;font-weight:650!important}}
.hero{{min-height:126px!important;background-image:linear-gradient(90deg,rgba(18,23,22,.86),rgba(18,23,22,.62) 52%,rgba(18,23,22,.25)),url('{HERO}')!important;background-size:cover!important;background-position:center!important;border-color:color-mix(in srgb,var(--accent) 18%,#d6d6d4)!important}}
.hero:after{{display:none!important}}
.hero h1{{color:#fff!important;text-shadow:0 1px 8px rgba(0,0,0,.24)}}
.hero p{{color:rgba(255,255,255,.88)!important}}
.kcard,.kcard.primary{{height:108px!important;background:color-mix(in srgb,var(--soft) 24%,#fff)!important;border:1px solid color-mix(in srgb,var(--accent) 15%,#dededc)!important;border-top:3px solid color-mix(in srgb,var(--accent) 72%,#fff)!important}}
.kcard.primary .klabel,.kcard .klabel{{color:color-mix(in srgb,var(--ink) 82%,var(--accent))!important}}
.kcard.primary .kvalue,.kcard .kvalue{{color:var(--ink)!important}}
.kcard.primary .ksub,.kcard .ksub{{color:color-mix(in srgb,var(--accent) 68%,var(--muted))!important}}
[data-testid="stPlotlyChart"]{{background:color-mix(in srgb,var(--soft) 15%,#fff)!important;border-color:color-mix(in srgb,var(--accent) 12%,#dededc)!important}}
[data-testid="stDataFrame"],[data-testid="stTable"]{{background:color-mix(in srgb,var(--soft) 15%,#fff)!important;border-color:color-mix(in srgb,var(--accent) 12%,#dededc)!important}}
.panel-title{{margin:.48rem 0 .08rem!important;color:var(--ink)!important}}
.panel-sub{{margin:0 0 .42rem!important;color:var(--muted)!important}}
.modebar{{display:none!important}}
.side-promo{{display:none!important}}
.sidebar-brand{{border-bottom-color:color-mix(in srgb,var(--accent) 18%,#d7d7d5)!important}}
.sidebar-brand>span{{background:transparent!important;color:var(--accent)!important;width:38px;height:38px;border-radius:0!important}}
.sidebar-brand.health>span{{position:relative;font-size:0}}
.sidebar-brand.health>span:before,.sidebar-brand.health>span:after{{content:'';position:absolute;width:19px;height:28px;border-radius:100% 0 100% 0;background:var(--accent);transform:rotate(-35deg);left:3px;top:5px}}
.sidebar-brand.health>span:after{{left:16px;transform:scaleX(-1) rotate(-35deg);background:var(--accent2)}}
.sidebar-brand.mining>span{{font-size:0;border-left:3px solid var(--accent2)!important;transform:skewX(-12deg);position:relative}}
.sidebar-brand.mining>span:before{{content:'≡';font-size:2rem;font-weight:900;line-height:1;color:var(--accent2);position:absolute;left:6px;top:0}}
.sidebar-brand.loan>span{{border:2px solid var(--accent)!important;border-radius:50%!important;font-size:.58rem!important;font-weight:800!important}}
.sidebar-brand.retail>span{{display:none!important}}
.sidebar-brand.retail strong{{font-weight:850!important;letter-spacing:.07em!important;text-transform:uppercase}}
.sidebar-brand.tourism>span{{display:none!important}}
.sidebar-brand.tourism>div{{border-left:4px solid var(--accent2);padding-left:10px}}
/* Image-backed navigation and high-contrast light report */
section[data-testid="stSidebar"]>div:first-child{{min-height:100vh!important;padding:10px 14px 18px!important;background-image:linear-gradient(rgba(12,22,20,.78),rgba(12,22,20,.88)),url('{HERO}')!important;background-size:cover!important;background-position:center!important}}
section[data-testid="stSidebar"] h1,section[data-testid="stSidebar"] h2,section[data-testid="stSidebar"] h3,section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] .stCaption{{color:rgba(255,255,255,.88)!important}}
section[data-testid="stSidebar"] hr{{border-top-color:rgba(255,255,255,.22)!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label p{{color:rgba(255,255,255,.76)!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{{background:rgba(255,255,255,.10)!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){{background:rgba(255,255,255,.16)!important;box-shadow:inset 3px 0 0 color-mix(in srgb,var(--accent2) 70%,#fff)!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{{color:#fff!important}}
section[data-testid="stSidebar"] [data-baseweb="select"]>div{{background:rgba(255,255,255,.92)!important;border-color:rgba(255,255,255,.34)!important;color:#202523!important}}
section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p{{color:#fff!important}}
.sidebar-brand{{margin:0 2px 12px!important;padding:0 2px 12px!important;border-bottom-color:rgba(255,255,255,.24)!important}}
.sidebar-brand strong{{color:#fff!important;text-shadow:0 1px 6px rgba(0,0,0,.35)}}
.sidebar-brand small{{color:rgba(255,255,255,.72)!important}}
.sidebar-brand>span{{color:#fff!important}}
.sidebar-brand.loan>span{{border-color:#fff!important}}
.sidebar-brand.health>span:before{{background:#fff!important}}
.sidebar-brand.health>span:after{{background:color-mix(in srgb,var(--accent2) 72%,#fff)!important}}
.sidebar-brand.mining>span{{border-left-color:var(--accent2)!important}}
section[data-testid="stSidebarCollapseButton"] button{{color:#fff!important;background:rgba(0,0,0,.18)!important}}
.kcard,.kcard.primary{{border:0!important;border-top:0!important;background:linear-gradient(140deg,color-mix(in srgb,var(--accent) 88%,#21302b),color-mix(in srgb,var(--accent2) 62%,var(--accent)))!important;box-shadow:0 3px 10px rgba(24,34,31,.12)!important}}
.kcard .klabel,.kcard.primary .klabel{{color:rgba(255,255,255,.84)!important}}
.kcard .kvalue,.kcard.primary .kvalue{{color:#fff!important;text-shadow:0 1px 5px rgba(0,0,0,.18)}}
.kcard .ksub,.kcard.primary .ksub{{color:rgba(255,255,255,.76)!important}}
[data-testid="stPlotlyChart"]{{background:#fff!important;border:1px solid color-mix(in srgb,var(--accent) 10%,#d9dddb)!important}}
[data-testid="stDataFrame"]{{background:#fff!important;border:1px solid color-mix(in srgb,var(--accent) 12%,#d5d9d7)!important}}
[data-testid="stDataFrame"] button{{color:#26312c!important}}
/* Exact software-brand lockup and sidebar action */
section[data-testid="stSidebar"] [data-testid="stSidebarContent"]{{padding-top:0!important}}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"]{{padding-top:8px!important}}
.sidebar-brand{{margin-top:0!important;align-items:center!important}}
.sidebar-brand.loan>span{{display:none!important}}
.sidebar-brand.loan strong{{font-weight:780!important;letter-spacing:-.02em}}
.sidebar-brand.retail strong{{font-weight:900!important;letter-spacing:.09em!important}}
.sidebar-brand.tourism strong{{letter-spacing:-.025em!important}}
.sidebar-brand.mining>span:before{{content:''!important;position:absolute!important;left:7px!important;top:7px!important;width:28px!important;height:3px!important;background:var(--accent2)!important;box-shadow:-2px 9px 0 var(--accent2),-5px 18px 0 var(--accent2)!important}}
section[data-testid="stSidebar"] .stLinkButton a{{min-height:38px!important;border:1px solid rgba(255,255,255,.55)!important;background:rgba(255,255,255,.15)!important;color:#fff!important;border-radius:7px!important;font-weight:750!important}}
section[data-testid="stSidebar"] .stLinkButton a:hover{{background:#fff!important;color:var(--accent)!important}}
/* Top-aligned identity and report actions */
.sidebar-brand{{position:relative!important;left:-24px!important;top:-6px!important;width:calc(100% + 24px)!important;margin-bottom:2px!important;padding:8px 0 12px 8px!important}}
.report-actions-spacer{{flex:1}}
div[data-testid="stHorizontalBlock"]:has(#top_overview){{margin:0 0 .1rem!important}}
.stButton>button,.stLinkButton>a{{font-weight:700!important}}
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)

def kcard(label, value, sub="", primary=False):
    return f'<div class="kcard {"primary" if primary else ""}"><div class="klabel">{label}</div><div class="kvalue">{value}</div><div class="ksub">{sub}</div></div>'

def sidebar_brand(mark, name, tag):
    st.markdown(f'<div class="sidebar-brand {mark.lower()}"><span>{mark}</span><div><strong>{name}</strong><small>{tag}</small></div></div>', unsafe_allow_html=True)

def _open_overview():
    st.session_state["active_report_page"] = OVERVIEW_LABEL

def _open_section():
    selected = st.session_state.get("section_nav")
    if selected:
        st.session_state["active_report_page"] = selected

def sidebar_navigation(options):
    st.radio("Go to", options, index=None, key="section_nav", on_change=_open_section, label_visibility="collapsed")
    return st.session_state.get("active_report_page", OVERVIEW_LABEL)

def utilitybar(role):
    spacer, overview_col, software_col = st.columns([6, 1.05, 1.25])
    with overview_col:
        st.link_button("Overview", OVERVIEW_URL, use_container_width=True)
    with software_col:
        st.link_button("Open software", SOFTWARE_URL, use_container_width=True)
    return ""

def apply_search(frame, query):
    if not query or frame.empty:
        return frame
    matches = frame.astype(str).apply(lambda column: column.str.contains(query, case=False, regex=False, na=False)).any(axis=1)
    return frame.loc[matches]


def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def panel_head(title, sub=""):
    st.markdown(f'<div class="panel-title">{title}</div><div class="panel-sub">{sub}</div>', unsafe_allow_html=True)

def chart_style(fig, height=270, legend=True):
    fig.update_layout(height=height, margin=dict(l=12,r=12,t=22,b=10), paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", font=dict(family="Segoe UI, Arial",size=11,color="#303634"), showlegend=legend, legend=dict(orientation="h",yanchor="bottom",y=1.01,xanchor="right",x=1,font=dict(size=9)), hoverlabel=dict(bgcolor="#2f3332",font=dict(color="#fff",size=10)), coloraxis_showscale=False)
    fig.update_xaxes(showgrid=False,linecolor="#cfd5d2",tickfont=dict(size=10,color="#424946"),title_font=dict(size=9),zeroline=False)
    fig.update_yaxes(gridcolor="#e2e6e4",linecolor="#cfd5d2",tickfont=dict(size=10,color="#424946"),title_font=dict(size=9),zeroline=False)
    return fig

@st.cache_data
def load_data():
    eq=pd.read_csv(ROOT/"equipment_data.csv",parse_dates=["date"])
    risk=pd.read_csv(ROOT/"risk_scores.csv")
    return eq,risk
eq,risk=load_data()
with st.sidebar:
    sidebar_brand("KM", "KGOSI MINING", "Fleet intelligence & maintenance")
    st.divider()
    page=st.radio("Go to",["Overview","Costs & Repairs","Fuel Usage","Safety Alerts","Staff Report"],index=0,label_visibility="collapsed")
    st.divider()
    machine_types=["All Machine Types"]+sorted(eq.machine_type.dropna().unique().tolist())
    sites=["All Sites"]+sorted(eq.site.dropna().unique().tolist())
    machine_sel=st.selectbox("Machine Type",machine_types,index=0)
    site_sel=st.selectbox("Site",sites,index=0)
    st.divider(); st.caption("Period: Jul to Dec 2025")
    st.markdown('<div class="side-promo"><div><strong>Efficient operations. Stronger tomorrow.</strong><span>Fleet health, cost discipline and safer mining.</span></div></div>',unsafe_allow_html=True)

df=eq.copy()
if machine_sel!="All Machine Types": df=df[df.machine_type==machine_sel]
if site_sel!="All Sites": df=df[df.site==site_sel]
search_query=utilitybar("Operations Manager")
df=apply_search(df,search_query)

def money(x):
    return f"P{x/1e6:.1f}M" if abs(x)>=1e6 else (f"P{x/1e3:.0f}K" if abs(x)>=1e3 else f"P{x:,.0f}")

def mining_overview():
    hero("Operational Overview","Key metrics across fleet cost, maintenance, safety and people. Filters default to the full operation.")
    fuel=df.fuel_cost_bwp.sum(); repair=df.repair_cost_bwp.sum(); breakdowns=int(df.breakdown.sum())
    waste=(df.fuel_cost_bwp*(df.idle_hours/df.hours_today.replace(0,np.nan))).fillna(0).sum()
    machines=df.machine_id.nunique(); risky=set(risk.loc[risk.risk_level.isin(["High","Critical"]),"machine_id"]); healthy=max(machines-len(set(df.machine_id)&risky),0)
    maint=int(df.groupby('machine_id').maintenance_due.max().sum()); safety=int((df.safety_risk.astype(str).str.lower()=="high").sum())
    util=(df.active_hours.sum()/df.hours_today.sum()*100) if df.hours_today.sum() else 0
    cols=st.columns(7)
    vals=[("Fleet Fuel Cost",money(fuel),"Operating fuel spend"),("Repair Cost",money(repair),"Breakdown & repair spend"),("Fuel Waste",money(waste),"Estimated idle fuel cost"),("Breakdowns",f"{breakdowns:,}","Recorded events"),("Machines Healthy",f"{healthy}/{machines}",f"{machines-healthy} need attention"),("Maintenance Due",f"{maint}","Machines flagged"),("Fleet Utilization",f"{util:.0f}%","Active hours / total hours")]
    for i,(c,v,s) in enumerate(vals): cols[i].markdown(kcard(c,v,s,i==0),unsafe_allow_html=True)
    c1,c2,c3=st.columns([1.35,1,1])
    monthly=df.assign(month=df.date.dt.to_period('M').astype(str)).groupby('month').agg(repair=('repair_cost_bwp','sum'),fuel=('fuel_cost_bwp','sum')).reset_index()
    with c1:
        panel_head("Monthly Repair Cost vs Fuel Cost","Cost movement across the selected fleet")
        long=monthly.melt('month',var_name='metric',value_name='amount')
        fig=px.bar(long,x='month',y='amount',color='metric',barmode='group',color_discrete_map={'repair':ACCENT,'fuel':ACCENT2},labels={'month':'','amount':'BWP','metric':''})
        st.plotly_chart(chart_style(fig,255),use_container_width=True)
    with c2:
        panel_head("Breakdowns by Machine Type","Where failures are concentrated")
        b=df[df.breakdown==1].groupby('machine_type').size().sort_values(ascending=True).reset_index(name='count')
        fig=px.bar(b,x='count',y='machine_type',orientation='h',color_discrete_sequence=[ACCENT],labels={'machine_type':'','count':'Breakdowns'})
        st.plotly_chart(chart_style(fig,255,False),use_container_width=True)
    with c3:
        panel_head("Safety Alerts by Site","High-risk operating records")
        s=df.assign(high=df.safety_risk.astype(str).str.lower().eq('high').astype(int)).groupby('site').high.sum().sort_values(ascending=True).reset_index()
        fig=px.bar(s,x='high',y='site',orientation='h',color_discrete_sequence=["#7da995"],labels={'site':'','high':'Alerts'})
        st.plotly_chart(chart_style(fig,255,False),use_container_width=True)
    st.markdown('<div class="section-title">Machine Risk & Service Status</div>',unsafe_allow_html=True)
    table=risk[['machine_id','machine_type','site','cumulative_hours','days_since_maintenance','risk_level','safety_risk']].copy()
    if machine_sel!="All Machine Types": table=table[table.machine_type==machine_sel]
    if site_sel!="All Sites": table=table[table.site==site_sel]
    table.columns=['Machine ID','Type','Site','Hours','Days Since Service','Risk Level','Safety Risk']
    st.dataframe(table.sort_values(['Risk Level','Days Since Service'],ascending=[True,False]).head(12),use_container_width=True,hide_index=True,height=300)

def costs_page():
    hero("Costs & Repairs","Track maintenance spend, repair concentration and machines driving avoidable cost.")
    c1,c2,c3,c4=st.columns(4)
    repair=df.repair_cost_bwp.sum(); fuel=df.fuel_cost_bwp.sum(); costly=df.groupby('machine_id').repair_cost_bwp.sum().sort_values(ascending=False)
    for i,(a,b,c) in enumerate([("Repair Spend",money(repair),"Selected view"),("Fuel Spend",money(fuel),"Selected view"),("Avg Repair / Machine",money(repair/max(df.machine_id.nunique(),1)),"Across fleet"),("Costliest Machine",costly.index[0] if len(costly) else '—',money(costly.iloc[0]) if len(costly) else 'No cost')]): [c1,c2,c3,c4][i].markdown(kcard(a,b,c,i==0),unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        panel_head("Repair Cost by Machine Type")
        x=df.groupby('machine_type').repair_cost_bwp.sum().sort_values().reset_index(); fig=px.bar(x,x='repair_cost_bwp',y='machine_type',orientation='h',color_discrete_sequence=[ACCENT]); st.plotly_chart(chart_style(fig,300,False),use_container_width=True)
    with c2:
        panel_head("Top Machines by Repair Cost")
        x=df.groupby('machine_id').repair_cost_bwp.sum().nlargest(10).sort_values().reset_index(); fig=px.bar(x,x='repair_cost_bwp',y='machine_id',orientation='h',color_discrete_sequence=[ACCENT2]); st.plotly_chart(chart_style(fig,300,False),use_container_width=True)

def fuel_page():
    hero("Fuel Usage","Monitor fuel consumption, idle waste and efficiency across sites and equipment classes.")
    c1,c2,c3=st.columns(3); total=df.fuel_litres.sum(); idle=df.idle_hours.sum(); eff=df.fuel_litres.sum()/max(df.active_hours.sum(),1)
    for i,(a,b,c) in enumerate([("Fuel Used",f"{total/1e3:.1f}K L","Selected view"),("Idle Hours",f"{idle:,.0f}","Operational idle time"),("Litres / Active Hour",f"{eff:.1f} L","Fuel intensity")]): [c1,c2,c3][i].markdown(kcard(a,b,c,i==0),unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        x=df.groupby('site').fuel_cost_bwp.sum().sort_values().reset_index(); fig=px.bar(x,x='fuel_cost_bwp',y='site',orientation='h',color_discrete_sequence=[ACCENT]); st.plotly_chart(chart_style(fig,310,False),use_container_width=True)
    with c2:
        x=df.groupby('machine_type').agg(fuel=('fuel_litres','sum'),active=('active_hours','sum')).reset_index(); x['lph']=x.fuel/x.active.replace(0,np.nan); fig=px.bar(x.sort_values('lph'),x='lph',y='machine_type',orientation='h',color_discrete_sequence=[ACCENT2]); st.plotly_chart(chart_style(fig,310,False),use_container_width=True)

def safety_page():
    hero("Safety Alerts","Surface high-risk operating records, breakdown exposure and site-level safety signals.")
    x=df.groupby(['site','safety_risk']).size().reset_index(name='records'); fig=px.bar(x,x='site',y='records',color='safety_risk',barmode='stack',color_discrete_map={'Low':'#9cc3b2','Medium':'#d4aa69','High':'#d05a4f'}); st.plotly_chart(chart_style(fig,320),use_container_width=True)
    high=df[df.safety_risk.astype(str).str.lower().eq('high')][['date','machine_id','machine_type','site','operator_id','engine_temp_c','vibration','breakdown']].sort_values('date',ascending=False).head(20); st.dataframe(high,use_container_width=True,hide_index=True,height=310)

def staff_page():
    hero("Staff Report","Compare operator activity, utilisation and incident exposure across the selected operation.")
    op=df.groupby('operator_id').agg(active_hours=('active_hours','sum'),total_hours=('hours_today','sum'),breakdowns=('breakdown','sum'),fuel=('fuel_litres','sum')).reset_index(); op['utilization_pct']=op.active_hours/op.total_hours.replace(0,np.nan)*100
    st.dataframe(op.sort_values('utilization_pct',ascending=False).head(30),use_container_width=True,hide_index=True,height=520)

{"Overview":mining_overview,"Costs & Repairs":costs_page,"Fuel Usage":fuel_page,"Safety Alerts":safety_page,"Staff Report":staff_page}[page]()
