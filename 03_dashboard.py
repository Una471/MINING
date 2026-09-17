"""
KGOSI MINING SOLUTIONS - OPERATIONS DASHBOARD
Simple, clear report for management staff. No technical jargon.
Run: streamlit run 03_dashboard.py --server.port 8501
"""

import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

BASE_DIR = Path(__file__).resolve().parent


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@500;600;700;800&family=Stack+Sans+Text:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#f5f6fa;color:#15151f;}
.topbar{background:linear-gradient(135deg,#15151f,#20202c);color:white;padding:1.4rem 2rem;border-radius:12px;margin-bottom:1.5rem;}
.topbar h1{margin:0;font-size:1.5rem;font-weight:700;}
.topbar p{margin:.3rem 0 0 0;opacity:.6;font-size:.85rem;}
.kcard{background:white;border-radius:12px;padding:1.2rem 1.4rem;box-shadow:0 2px 8px rgba(0,0,0,.07);border-left:5px solid #e0e0e0;}
.kcard.red{border-left-color:#e74c3c;} .kcard.orange{border-left-color:#e67e22;}
.kcard.green{border-left-color:#27ae60;} .kcard.blue{border-left-color:#e19a3b;}
.kval{font-size:1.9rem;font-weight:700;line-height:1.1;}
.klbl{font-size:.72rem;text-transform:uppercase;letter-spacing:1.5px;color:#888;margin-top:.3rem;}
.ksub{font-size:.78rem;color:#666;margin-top:.3rem;}
.ccard{background:white;border-radius:12px;padding:1.2rem 1.4rem;box-shadow:0 2px 8px rgba(0,0,0,.07);margin-bottom:1rem;}
.ctitle{font-size:.95rem;font-weight:600;color:#15151f;margin-bottom:.2rem;}
.csub{font-size:.78rem;color:#888;margin-bottom:.7rem;}
.ar{background:#fdf2f2;border:1px solid #f5c6cb;border-radius:8px;padding:.9rem;margin-bottom:.5rem;}
.ao{background:#fff8f0;border:1px solid #fcd5a5;border-radius:8px;padding:.9rem;margin-bottom:.5rem;}
.ag{background:#f0faf4;border:1px solid #b7dfca;border-radius:8px;padding:.9rem;margin-bottom:.5rem;}
section[data-testid="stSidebar"]{background:#15151f!important;}
section[data-testid="stSidebar"] *{color:white!important;}
#MainMenu,footer,header{visibility:hidden;}
/* Professional analytics console */
:root{--dash-bg:#0d0d14;--dash-side:#15151f;--dash-card:#1a1a24;--dash-card-2:#20202c;--dash-line:#2c2c3a;--dash-text:#f5f5f7;--dash-muted:#9a9aaa;--dash-accent:#e19a3b;--dash-soft:#f1c47f}
html,body,[class*="css"],.stApp{font-family:'Stack Sans Text','Red Hat Display','Segoe UI',sans-serif!important;background:var(--dash-bg)!important;color:var(--dash-text)!important}.stApp{background:radial-gradient(circle at 86% 0%,rgba(225,154,59,.08),transparent 30%),var(--dash-bg)!important}.block-container{max-width:1500px;padding:1.25rem 2rem 3rem!important}h1,h2,h3,h4,p,label,span{color:var(--dash-text)}h1,h2,h3,h4{font-family:'Red Hat Display','Segoe UI',sans-serif!important;letter-spacing:-.025em}
section[data-testid="stSidebar"]{width:228px!important;background:var(--dash-side)!important;border-right:1px solid var(--dash-line)!important}section[data-testid="stSidebar"]>div{padding:1.3rem .85rem!important}section[data-testid="stSidebar"] h3{font-size:1.05rem!important;margin:.2rem .55rem 0!important;color:#fff!important}section[data-testid="stSidebar"] p{color:var(--dash-muted)!important;font-size:.72rem!important}section[data-testid="stSidebar"] hr{border-color:var(--dash-line)!important;margin:1rem 0!important}section[data-testid="stSidebar"] div[role="radiogroup"]{gap:.3rem}section[data-testid="stSidebar"] div[role="radiogroup"] label{padding:.65rem .7rem!important;border-radius:7px!important;background:transparent!important;margin:0!important;transition:background .16s ease}section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{background:var(--dash-card-2)!important}section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){background:var(--dash-accent)!important}section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{color:#101018!important;font-weight:700!important}section[data-testid="stSidebar"] div[role="radiogroup"] label>div:first-child{display:none}section[data-testid="stSidebar"] [data-baseweb="select"]>div{background:var(--dash-card)!important;border-color:var(--dash-line)!important;color:#fff!important;border-radius:7px!important}section[data-testid="stSidebar"] svg{fill:var(--dash-muted)!important}
.topbar{position:relative;background:transparent!important;border:0!important;border-bottom:1px solid var(--dash-line)!important;border-radius:0!important;box-shadow:none!important;padding:.4rem 0 1rem!important;margin-bottom:1.1rem!important}.topbar:before{content:'ANALYTICS';display:block;color:var(--dash-accent);font-size:.58rem;letter-spacing:.18em;font-weight:700;margin-bottom:.45rem}.topbar h1{font-size:1.65rem!important;color:#fff!important}.topbar p{color:var(--dash-muted)!important;opacity:1!important;font-size:.73rem!important}
.kcard{min-height:118px;background:var(--dash-card)!important;border:1px solid var(--dash-line)!important;border-left:1px solid var(--dash-line)!important;border-top:3px solid var(--dash-accent)!important;border-radius:8px!important;box-shadow:none!important;padding:1rem 1.05rem!important;color:var(--dash-text)!important}.kcard.red{border-top-color:#ff6b6b!important}.kcard.orange{border-top-color:#f4a261!important}.kcard.green{border-top-color:#59d98e!important}.kcard.blue,.kcard.gold{border-top-color:var(--dash-accent)!important}.kval{font-family:'Red Hat Display','Segoe UI',sans-serif!important;font-size:1.75rem!important;color:#fff!important;font-variant-numeric:tabular-nums}.klbl{color:#d7d7df!important;font-size:.62rem!important;letter-spacing:.1em!important}.ksub{color:var(--dash-muted)!important;font-size:.66rem!important}
.ccard{background:var(--dash-card)!important;border:1px solid var(--dash-line)!important;border-radius:8px!important;box-shadow:none!important;padding:1rem!important}.ctitle{color:#fff!important;font-size:.86rem!important}.csub{color:var(--dash-muted)!important;font-size:.68rem!important}.ar,.ao,.ag{background:var(--dash-card)!important;border:1px solid var(--dash-line)!important;border-left:3px solid var(--dash-accent)!important;border-radius:7px!important;color:#dcdce4!important;line-height:1.5!important}.ar{border-left-color:#ff6b6b!important}.ao{border-left-color:#f4a261!important}.ag{border-left-color:#59d98e!important}.ar *,.ao *,.ag *{color:inherit!important}.ar b,.ao b,.ag b{color:#fff!important}
[data-testid="stPlotlyChart"]{background:var(--dash-card)!important;border:1px solid var(--dash-line);border-radius:8px;padding:.35rem}[data-testid="stDataFrame"]{border:1px solid var(--dash-line);border-radius:8px;overflow:hidden}.stSelectbox label p,.stMultiSelect label p,.stSlider label p{color:#d7d7df!important}.stAlert{background:var(--dash-card-2)!important;border-color:var(--dash-line)!important}.stAlert *{color:#eeeef3!important}hr{border-color:var(--dash-line)!important}#MainMenu,footer,header{visibility:hidden}@media(max-width:900px){.block-container{padding:1rem!important}.kcard{min-height:auto}section[data-testid="stSidebar"]{width:250px!important}}
section[data-testid='stSidebar'] h3:before{content:'';display:inline-block;width:9px;height:9px;background:var(--dash-accent);transform:rotate(45deg);margin-right:.55rem;border-radius:2px}.modebar{display:none!important}[data-testid='stPlotlyChart']:hover{border-color:rgba(255,255,255,.2)}[data-testid='stDataFrame']{background:var(--dash-card)!important}
/* Reference dashboard rebuild */
:root{--canvas:#0c0c13;--sidebar:#171720;--panel:#1b1b25;--panel-hover:#20202c;--stroke:#2b2b38;--ink:#f7f7fa;--muted:#a8a8b7}
html,body,.stApp,[class*="css"]{font-family:"Stack Sans Text","Segoe UI",Arial,sans-serif!important}.stApp{background:var(--canvas)!important}.block-container{max-width:1440px!important;padding:1.65rem 2.25rem 3rem!important}
section[data-testid="stSidebar"]{width:205px!important;background:var(--sidebar)!important;border-right:1px solid var(--stroke)!important}section[data-testid="stSidebar"]>div{padding:2.1rem 1rem!important}section[data-testid="stSidebar"] h3{font-family:"Stack Sans Text","Segoe UI",sans-serif!important;font-size:1.12rem!important;font-weight:720!important;line-height:1.18!important;letter-spacing:-.02em!important;margin:1.8rem .45rem .3rem!important}section[data-testid="stSidebar"] h3:before{width:8px!important;height:8px!important;margin-right:.55rem!important;border-radius:1px!important}section[data-testid="stSidebar"] p{font-size:.75rem!important;line-height:1.45!important;color:#aaaaba!important}section[data-testid="stSidebar"] hr{margin:1.15rem .25rem!important;border-color:var(--stroke)!important}section[data-testid="stSidebar"] div[role="radiogroup"]{gap:.28rem!important}section[data-testid="stSidebar"] div[role="radiogroup"] label{min-height:39px!important;padding:.6rem .72rem!important;border-radius:7px!important}section[data-testid="stSidebar"] div[role="radiogroup"] label p{font-size:.76rem!important;line-height:1.15!important;color:#bcbccc!important}section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){background:var(--dash-accent)!important;box-shadow:0 5px 18px color-mix(in srgb,var(--dash-accent) 22%,transparent)!important}section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{color:#fff!important;font-weight:700!important}section[data-testid="stSidebar"] [data-baseweb="select"]>div{min-height:42px!important;border-radius:7px!important}
.topbar{padding:.1rem 0 1rem!important;margin:0 0 1.2rem!important;border-bottom:1px solid var(--stroke)!important}.topbar:before{display:none!important}.topbar h1{font-family:"Stack Sans Text","Segoe UI",sans-serif!important;font-size:1.65rem!important;font-weight:680!important;letter-spacing:-.035em!important;line-height:1.15!important}.topbar p{font-size:.78rem!important;line-height:1.5!important;margin-top:.5rem!important;color:var(--muted)!important}
[data-testid="stHorizontalBlock"]{gap:.78rem!important}.kcard{min-height:128px!important;display:flex!important;flex-direction:column!important;justify-content:center!important;padding:1.05rem 1.1rem!important;background:var(--panel)!important;border:1px solid var(--stroke)!important;border-top:1px solid var(--stroke)!important;border-radius:9px!important;position:relative!important;overflow:hidden!important}.kcard:before{content:"";position:absolute;inset:0 auto 0 0;width:3px;background:var(--dash-accent)}.kcard.red:before{background:#ff6969}.kcard.orange:before{background:#f0a34a}.kcard.green:before{background:#48cf8b}.kval{font-family:"Stack Sans Text","Segoe UI",sans-serif!important;font-size:1.85rem!important;font-weight:690!important;line-height:1!important;letter-spacing:-.045em!important}.klbl{margin-top:.7rem!important;font-size:.72rem!important;font-weight:680!important;line-height:1.25!important;letter-spacing:0!important;text-transform:none!important;color:#ededf2!important}.ksub{margin-top:.32rem!important;font-size:.68rem!important;line-height:1.35!important;color:var(--muted)!important}
.ccard{padding:1rem 1.05rem!important;margin:0 0 .7rem!important;background:var(--panel)!important;border:1px solid var(--stroke)!important;border-radius:9px 9px 0 0!important}.ctitle{font-size:.88rem!important;font-weight:680!important;line-height:1.3!important;letter-spacing:-.01em!important}.csub{margin-top:.35rem!important;font-size:.7rem!important;line-height:1.4!important;color:var(--muted)!important}[data-testid="stPlotlyChart"]{margin-top:-.72rem!important;padding:.35rem!important;background:var(--panel)!important;border:1px solid var(--stroke)!important;border-top:0!important;border-radius:0 0 9px 9px!important}.modebar{display:none!important}
h1,h2,h3,h4{font-family:"Stack Sans Text","Segoe UI",sans-serif!important}h2{font-size:1.35rem!important;font-weight:680!important;letter-spacing:-.025em!important;margin-top:1.4rem!important}p,li,label,[data-testid="stMarkdownContainer"]{line-height:1.5}.ar,.ao,.ag{padding:1rem!important;border-radius:8px!important;font-size:.76rem!important;line-height:1.55!important;background:var(--panel)!important}.stDataFrame,[data-testid="stDataFrame"]{font-size:.78rem!important;background:var(--panel)!important;border-color:var(--stroke)!important}.stAlert{border-radius:8px!important}.stSelectbox label p,.stMultiSelect label p,.stSlider label p{font-size:.72rem!important;text-transform:none!important;letter-spacing:0!important}
@media(max-width:900px){section[data-testid="stSidebar"]{width:245px!important}.block-container{padding:1rem!important}[data-testid="stHorizontalBlock"]{gap:.55rem!important}.kcard{min-height:105px!important}}
/* Single viewport dashboard proportions */
.block-container{max-width:none!important;padding:.8rem 1.55rem 1.3rem!important}.topbar{padding:0 0 .65rem!important;margin:0 0 .72rem!important}.topbar h1{font-size:1.38rem!important;line-height:1.1!important}.topbar p{font-size:.7rem!important;margin-top:.32rem!important}.topbar a,.topbar svg,a.header-anchor,[data-testid="stHeaderActionElements"]{display:none!important}
[data-testid="stHorizontalBlock"]{gap:.62rem!important}.kcard{min-height:88px!important;padding:.72rem .82rem!important;border-radius:8px!important}.kval{font-size:1.48rem!important}.klbl{font-size:.65rem!important;margin-top:.46rem!important}.ksub{font-size:.59rem!important;margin-top:.2rem!important}.ccard{padding:.68rem .8rem!important;margin:0 0 .55rem!important;min-height:48px!important}.ctitle{font-size:.75rem!important}.csub{font-size:.61rem!important;margin-top:.2rem!important}[data-testid="stPlotlyChart"]{margin-top:-.57rem!important;padding:.15rem!important}h2{font-size:1.12rem!important;margin:.75rem 0 .5rem!important}.ar,.ao,.ag{padding:.68rem .75rem!important;font-size:.67rem!important;line-height:1.4!important;margin-bottom:.35rem!important}hr{margin:.72rem 0!important}
section[data-testid="stSidebar"]{width:184px!important}section[data-testid="stSidebar"]>div{padding:1rem .75rem!important}section[data-testid="stSidebar"] h3{font-size:.93rem!important;margin:1rem .38rem .18rem!important}section[data-testid="stSidebar"] p{font-size:.62rem!important}section[data-testid="stSidebar"] hr{margin:.72rem .2rem!important}section[data-testid="stSidebar"] div[role="radiogroup"]{gap:.16rem!important}section[data-testid="stSidebar"] div[role="radiogroup"] label{min-height:32px!important;padding:.42rem .58rem!important}section[data-testid="stSidebar"] div[role="radiogroup"] label p{font-size:.64rem!important}section[data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(1) p:before{content:"▦";margin-right:.5rem}section[data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(2) p:before{content:"◫";margin-right:.5rem}section[data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(3) p:before{content:"▤";margin-right:.5rem}section[data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(4) p:before{content:"◎";margin-right:.5rem}section[data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(5) p:before{content:"⌁";margin-right:.5rem}section[data-testid="stSidebar"] [data-baseweb="select"]>div{min-height:34px!important;font-size:.65rem!important}
[data-testid="stDataFrame"]{font-size:.68rem!important}@media(max-width:900px){.block-container{padding:.75rem!important}section[data-testid="stSidebar"]{width:235px!important}}
.csub{display:none!important}
/* Reference composition final */
.block-container{padding:1.35rem 2rem 2rem!important}.topbar{padding:.2rem 0 .8rem!important;margin-bottom:1rem!important}.topbar h1{font-size:1.65rem!important}.topbar p{font-size:.78rem!important}.kcard{min-height:112px!important;padding:1rem 1.05rem!important;border:0!important;border-radius:9px!important;background:#1c1c27!important}.kcard:before{display:none!important}.kval{font-size:1.72rem!important}.klbl{font-size:.73rem!important;margin-top:.65rem!important}.ksub{font-size:.66rem!important}.ccard{min-height:auto!important;padding:.85rem 1rem!important;border:0!important;border-radius:9px 9px 0 0!important;background:#1c1c27!important}.ctitle{font-size:.86rem!important}[data-testid="stPlotlyChart"]{border:0!important;border-radius:0 0 9px 9px!important;background:#1c1c27!important;padding:.25rem .6rem!important}section[data-testid="stSidebar"]{width:220px!important}section[data-testid="stSidebar"]>div{padding:1.5rem 1rem!important}section[data-testid="stSidebar"] h3{font-size:1.05rem!important}section[data-testid="stSidebar"] p{font-size:.7rem!important}section[data-testid="stSidebar"] div[role="radiogroup"] label{min-height:38px!important;padding:.58rem .7rem!important}section[data-testid="stSidebar"] div[role="radiogroup"] label p{font-size:.72rem!important}section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){background:#f5f5f7!important;box-shadow:none!important}section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{color:#14141d!important}div[data-testid="stVerticalBlock"]{gap:.55rem!important}[data-testid="stExpander"]{border:1px solid #2b2b38!important;background:#171720!important;border-radius:8px!important}
/* Accessible colour and interaction */
.kcard{transition:transform .16s ease,background .16s ease!important;border-top:2px solid var(--dash-accent)!important}.kcard:hover{transform:translateY(-2px)!important;background:#22222e!important}.kcard.red{border-top-color:#ff6b72!important}.kcard.orange{border-top-color:#f3b64b!important}.kcard.green{border-top-color:#4fcf91!important}.kcard.blue,.kcard.gold{border-top-color:var(--dash-accent)!important}[data-testid="stPlotlyChart"]{transition:background .16s ease!important}[data-testid="stPlotlyChart"]:hover{background:#1e1e2a!important}.stSelectbox [data-baseweb="select"]>div:focus-within{border-color:var(--dash-accent)!important}
/* Power BI KPI cards */
.kcard{min-height:108px!important;display:flex!important;flex-direction:column!important;justify-content:flex-start!important;background:#191922!important;border:1px solid #30303c!important;border-radius:5px!important;padding:.9rem 1rem .82rem!important;box-shadow:0 1px 2px rgba(0,0,0,.16)!important;transform:none!important;transition:background .12s ease,border-color .12s ease!important}.kcard:hover{transform:none!important;background:#1d1d27!important;border-color:#414152!important}.kcard:before,.kcard:after{display:none!important}.klbl{order:1!important;display:flex!important;align-items:center!important;gap:.48rem!important;margin:0!important;color:#c9c9d3!important;font-size:.7rem!important;font-weight:560!important;line-height:1.25!important;letter-spacing:0!important;text-transform:none!important}.klbl:before{content:"";width:6px;height:6px;flex:0 0 6px;border-radius:50%;background:var(--dash-accent)}.kcard.red .klbl:before{background:#f06b72}.kcard.orange .klbl:before{background:#e9aa49}.kcard.green .klbl:before{background:#4bc589}.kcard.blue .klbl:before,.kcard.gold .klbl:before{background:var(--dash-accent)}.kval{order:2!important;margin:.5rem 0 0!important;color:#f8f8fb!important;font-family:"Stack Sans Text","Segoe UI",sans-serif!important;font-size:1.72rem!important;font-weight:650!important;line-height:1!important;letter-spacing:-.035em!important;font-variant-numeric:tabular-nums!important;white-space:nowrap!important}.ksub{order:3!important;margin-top:auto!important;padding-top:.5rem!important;color:#8f8f9e!important;font-size:.61rem!important;font-weight:450!important;line-height:1.2!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
.cross-app-link{position:fixed;top:1rem;right:1.7rem;z-index:9999;display:inline-flex;align-items:center;justify-content:center;padding:.55rem .85rem;background:#f5f5f7;color:#15151f!important;border:1px solid #f5f5f7;border-radius:5px;font:600 .72rem "Stack Sans Text","Segoe UI",sans-serif;text-decoration:none!important;box-shadow:0 2px 8px rgba(0,0,0,.18)}.cross-app-link:hover{background:var(--dash-accent);border-color:var(--dash-accent);color:#fff!important}</style>
""", unsafe_allow_html=True)

def load():
    df   = pd.read_csv(BASE_DIR / "equipment_data.csv", parse_dates=["date"])
    risk = pd.read_csv(BASE_DIR / "risk_scores.csv")
    return df, risk

df, risk = load()

with st.sidebar:
    st.markdown("###  Kgosi Mining")
    st.markdown("Operations Dashboard")
    st.markdown("---")
    page = st.radio("Go to", [
        "  Overview",
        "  Costs & Repairs",
        "  Fuel Usage",
        "  Safety Alerts",
        "  Staff Report",
    ])
    st.markdown("---")
    sel_t = st.selectbox("Filter: Machine Type", ["All Types"] + sorted(df["machine_type"].unique().tolist()))
    sel_s = st.selectbox("Filter: Site",         ["All Sites"] + sorted(df["site"].unique().tolist()))
    st.markdown("---")
    st.caption("Period: Jul  to  Dec 2025")

dff = df.copy()
if sel_t != "All Types": dff = dff[dff["machine_type"] == sel_t]
if sel_s != "All Sites":  dff = dff[dff["site"] == sel_s]

def kcard(color, val, lbl, sub=""):
    return f'<div class="kcard {color}"><div class="klbl">{lbl}</div><div class="kval">{val}</div>{"<div class=ksub>"+sub+"</div>" if sub else ""}</div>'

def wchart(fig, h=230):
    palette = ['#E2A63A','#D36D48','#6C83A8','#56B78B']
    for i, trace in enumerate(fig.data):
        if trace.type == "bar":
            point_count = len(trace.x) if trace.x is not None else len(trace.y)
            trace.marker.color = ([palette[j % len(palette)] for j in range(point_count)]
                                  if len(fig.data) == 1 else palette[i % len(palette)])
            trace.marker.line = dict(width=0)
            trace.opacity = 0.94
            trace.hovertemplate = "%{x}<br><b>%{y}</b><extra></extra>"
        elif trace.type in ("scatter", "scattergl"):
            trace.line.color = palette[i % len(palette)]
            trace.line.width = 2.5
            if getattr(trace, "marker", None):
                trace.marker.color = palette[i % len(palette)]
                trace.marker.size = 6
        elif trace.type == "pie":
            trace.marker.colors = palette
            trace.textinfo = "percent"
            trace.textposition = "outside"
    fig.update_layout(plot_bgcolor="#1b1b25", paper_bgcolor="#1b1b25", font_color="#d8d8e2",
                      font=dict(family="Stack Sans Text, Segoe UI, sans-serif", size=11), height=h,
                      margin=dict(t=12,b=18,l=8,r=8), coloraxis_showscale=False, hovermode="closest",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                                  font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
                      hoverlabel=dict(bgcolor="#272735", bordercolor="#3a3a4a", font=dict(color="#ffffff",size=12)))
    fig.update_xaxes(showgrid=False, linecolor="#343443", tickfont=dict(color="#a8a8b7",size=10), title=None, automargin=True, zeroline=False)
    fig.update_yaxes(gridcolor="#2b2b38", linecolor="#343443", tickfont=dict(color="#a8a8b7",size=10), title=None, automargin=True, zeroline=False)
    return fig

#  PAGE 1: OVERVIEW
if page == "  Overview":
    st.markdown('<div class="topbar"><h1> Operations Overview</h1><p>Kgosi Mining Solutions  |  July  to  December 2025</p></div>', unsafe_allow_html=True)

    bd = dff[dff["breakdown"]==1]
    idle_waste = dff["idle_hours"].sum()*35*14.5*0.35
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.markdown(kcard("red",    f"P{dff['repair_cost_bwp'].sum()/1e6:.1f}M", "Spent on Repairs",      "Jul to Dec 2025"), unsafe_allow_html=True)
    c2.markdown(kcard("orange", f"P{dff['fuel_cost_bwp'].sum()/1e6:.1f}M",   "Total Fuel Costs",      "Jul to Dec 2025"), unsafe_allow_html=True)
    c3.markdown(kcard("red",    f"P{idle_waste/1e3:.0f}K",                    "Fuel Wasted on Idle",   "Zero production benefit"), unsafe_allow_html=True)
    c4.markdown(kcard("red",    f"{dff['breakdown'].sum()}",                   "Breakdowns",            f"Avg P{bd['repair_cost_bwp'].mean():,.0f} each" if len(bd) else ""), unsafe_allow_html=True)
    c5.markdown(kcard("green",  f"{(risk['risk_level']=='Low').sum()} / 80",  "Machines Healthy",      f"{(risk['risk_level']!='Low').sum()} need attention"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="ccard"><div class="ctitle"> Monthly Repair Costs vs Fuel Costs</div><div class="csub">See which months had the most incidents</div>', unsafe_allow_html=True)
    mo = dff.groupby(dff["date"].dt.to_period("M")).agg(Repairs=("repair_cost_bwp","sum"),Fuel=("fuel_cost_bwp","sum")).reset_index()
    mo["Month"] = mo["date"].astype(str)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Repair Costs",x=mo["Month"],y=mo["Repairs"],marker_color="#e74c3c",text=mo["Repairs"].apply(lambda x:f"P{x/1e3:.0f}K"),textposition="outside"))
    fig.add_trace(go.Bar(name="Fuel Costs",  x=mo["Month"],y=mo["Fuel"],   marker_color="#f1c47f",text=mo["Fuel"].apply(lambda x:f"P{x/1e6:.1f}M"),  textposition="outside"))
    fig.update_layout(barmode="group",xaxis_title="Month",yaxis_title="Cost (BWP)",legend=dict(orientation="h",y=1.1))
    st.plotly_chart(wchart(fig, 245), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

#  PAGE 2: COSTS
elif page == "  Costs & Repairs":
    st.markdown('<div class="topbar"><h1> Repair Costs & Breakdown Report</h1><p>Which machines are breaking and what it is costing the company</p></div>', unsafe_allow_html=True)
    bd = dff[dff["breakdown"]==1]
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("red",    f"{len(bd)}",                            "Total Breakdowns",    "Past 6 months"), unsafe_allow_html=True)
    c2.markdown(kcard("red",    f"P{bd['repair_cost_bwp'].sum():,.0f}",  "Total Repair Bill",   "Jul to Dec 2025"), unsafe_allow_html=True)
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
    st.markdown("###  Every Breakdown: Full List")
    show = bd[["date","machine_id","machine_type","site","repair_cost_bwp","days_since_maintenance","operator_id"]].copy()
    show["date"]=""+show["date"].astype(str)
    show["repair_cost_bwp"]=show["repair_cost_bwp"].apply(lambda x:f"P{x:,.0f}")
    show["days_since_maintenance"]=show["days_since_maintenance"].apply(lambda x:f"{x} days")
    show.columns=["Date","Machine","Type","Site","Repair Cost","Days Since Last Service","Operator"]
    st.dataframe(show.sort_values("Date",ascending=False).reset_index(drop=True),use_container_width=True)
    st.markdown('<div class="ar"><b> Key Takeaway:</b> Every machine that broke down had warning signs days beforehand. These breakdowns were preventable. Planned servicing costs <b>P80,000</b>. Emergency repairs cost <b>P450,000 to P600,000</b>.</div>', unsafe_allow_html=True)

#  PAGE 3: FUEL
elif page == "  Fuel Usage":
    st.markdown('<div class="topbar"><h1> Fuel Usage & Waste Report</h1><p>How much fuel is being used: and how much is being wasted</p></div>', unsafe_allow_html=True)
    idle_waste = dff["idle_hours"].sum()*35*14.5*0.35
    idle_pct   = dff["idle_hours"].sum()/dff["hours_today"].sum()*100
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("blue",   f"P{dff['fuel_cost_bwp'].sum()/1e6:.2f}M","Total Fuel Spend",          "Jul to Dec 2025"), unsafe_allow_html=True)
    c2.markdown(kcard("red",    f"P{idle_waste:,.0f}",                     "Wasted on Idle Machines",   "Zero production"), unsafe_allow_html=True)
    c3.markdown(kcard("orange", f"{idle_pct:.1f}%",                        "Of Machine Time Was Idle",  "Machines on, doing nothing"), unsafe_allow_html=True)
    c4.markdown(kcard("orange", f"{dff['idle_hours'].sum():,.0f} hrs",     "Total Idle Hours",          "Across full fleet"), unsafe_allow_html=True)
    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">Fuel Spend by Machine Type</div><div class="csub">Haul Trucks use the most: even small idle reductions on them save a lot</div>', unsafe_allow_html=True)
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
    st.markdown("###  Which Operators Leave Machines Running?")
    st.caption("Ranked by total idle hours: these operators are responsible for the most wasted fuel")
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
    st.markdown('<div class="ao"><b> Action Needed:</b> The top 5 operators account for the majority of idle hours. A policy enforcing machine switch-off when idle for more than 10 minutes would recover most of this cost.</div>', unsafe_allow_html=True)

#  PAGE 4: SAFETY
elif page == "  Safety Alerts":
    st.markdown('<div class="topbar"><h1> Machine Safety Status</h1><p>Machines recorded operating outside safe limits</p></div>', unsafe_allow_html=True)
    rc = dff["safety_risk"].value_counts()
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("red",    f"{rc.get('Critical',0):,}","Critical Alerts",   "Must stop immediately"), unsafe_allow_html=True)
    c2.markdown(kcard("orange", f"{rc.get('High',0):,}",    "High Risk",         "Service within 48 hours"), unsafe_allow_html=True)
    c3.markdown(kcard("blue",   f"{rc.get('Medium',0):,}",  "Worth Monitoring",  "Keep an eye on these"), unsafe_allow_html=True)
    c4.markdown(kcard("green",  f"{rc.get('Low',0):,}",     "Operating Safely",  "No action needed"), unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("###  What Do the Alert Levels Mean?")
    e1,e2,e3 = st.columns(3)
    with e1: st.markdown('<div class="ar"><b> CRITICAL</b><br>Temperature above 115C or severe shaking. <b>Stop this machine now.</b> Running it risks injury and a major breakdown.</div>', unsafe_allow_html=True)
    with e2: st.markdown('<div class="ao"><b> HIGH RISK</b><br>Temperature above 105C or high shaking. <b>Book it for service within 48 hours.</b> It will deteriorate fast if ignored.</div>', unsafe_allow_html=True)
    with e3: st.markdown('<div class="ag"><b> SAFE</b><br>All readings within normal range. <b>Continue normal operations.</b> Check again at next scheduled inspection.</div>', unsafe_allow_html=True)
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
    st.markdown("###  Machines Needing Immediate Attention")
    latest_all = dff.sort_values("date").groupby("machine_id").last().reset_index()
    danger = latest_all[latest_all["safety_risk"].isin(["Critical","High"])].copy()
    if len(danger)==0:
        st.success(" No machines currently in Critical or High state.")
    else:
        danger["Action"] = danger["safety_risk"].map({"Critical":" Stop & inspect NOW","High":" Service within 48 hrs"})
        danger["engine_temp_c"] = danger["engine_temp_c"].apply(lambda x:f"{x:.1f}C")
        danger["vibration"]     = danger["vibration"].apply(lambda x:f"{x:.2f}")
        show = danger[["machine_id","machine_type","site","engine_temp_c","vibration","safety_risk","Action"]].copy()
        show.columns=["Machine","Type","Site","Engine Temp","Vibration","Risk","Action Required"]
        st.dataframe(show.reset_index(drop=True),use_container_width=True)

#  PAGE 5: STAFF
elif page == "  Staff Report":
    st.markdown('<div class="topbar"><h1> Staff & Operator Performance</h1><p>How operators are handling company equipment</p></div>', unsafe_allow_html=True)
    op = dff.groupby("operator_id").agg(shifts=("record_id","count"),idle_hrs=("idle_hours","sum"),breakdowns=("breakdown","sum"),avg_temp=("engine_temp_c","mean")).reset_index()
    op["fuel_wasted"]=(op["idle_hrs"]*35*14.5*0.35).round(0)
    worst = op.sort_values("idle_hrs",ascending=False).iloc[0]
    c1,c2,c3 = st.columns(3)
    c1.markdown(kcard("blue",  f"{len(op)}",                 "Total Operators",       "Active Jul to Dec 2025"), unsafe_allow_html=True)
    c2.markdown(kcard("red",   worst["operator_id"],          "Most Idle Hours",        f"{worst['idle_hrs']:.0f} hrs total"), unsafe_allow_html=True)
    c3.markdown(kcard("red",   f"P{op['fuel_wasted'].sum():,.0f}","Fuel Wasted by Staff","Across all operators"), unsafe_allow_html=True)
    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">Operators with the Most Idle Time</div><div class="csub">These operators leave machines running when not in use: each idle hour costs money</div>', unsafe_allow_html=True)
        top = op.sort_values("idle_hrs",ascending=False).head(15)
        fig = px.bar(top,x="operator_id",y="idle_hrs",color="fuel_wasted",
                     color_continuous_scale=["#ffe5b4","#c0392b"],
                     text=top["fuel_wasted"].apply(lambda x:f"P{x:,.0f}"),
                     labels={"idle_hrs":"Total Idle Hrs","operator_id":"Operator"})
        fig.update_traces(textposition="outside"); fig.update_layout(showlegend=False)
        st.plotly_chart(wchart(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="ccard"><div class="ctitle">Breakdowns Recorded During Each Operator\'s Shift</div><div class="csub">Not always the operator\'s fault: but patterns help identify training needs</div>', unsafe_allow_html=True)
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
    st.markdown("###  Full Operator Summary Table")
    op_s = op.sort_values("idle_hrs",ascending=False).reset_index(drop=True); op_s.index+=1
    op_s["fuel_wasted"]=op_s["fuel_wasted"].apply(lambda x:f"P{x:,.0f}")
    op_s["avg_temp"]=op_s["avg_temp"].apply(lambda x:f"{x:.1f}C")
    op_s.columns=["Operator","Shifts","Idle Hrs","Breakdowns on Shift","Avg Engine Temp","Fuel Wasted"]
    st.dataframe(op_s, use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align:center;color:#aaa;font-size:.78rem'>Kgosi Mining Solutions | Operations Dashboard | Prepared by Data Analytics Team | 2026</div>", unsafe_allow_html=True)
